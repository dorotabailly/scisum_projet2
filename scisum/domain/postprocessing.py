"""Post processing utils module.

Classes
-------
Postprocessor

"""

from sklearn.base import TransformerMixin
from spacy.attrs import POS, ENT_TYPE, IS_ALPHA, DEP, LEMMA, LOWER, IS_PUNCT, IS_DIGIT, IS_SPACE, IS_STOP
from spacy.tokens import Doc
from typing import Dict, List

import logging
import numpy as np
import re
import spacy

from scisum.config import TAGS_DICT


def remove_duplicate_spaces(text: str) -> str:
    text = text.lstrip()
    text = re.sub(" +", " ", text)
    return text


def remove_leading_the(entity: str) -> str:
    """Remove leading the

    Parameters
    ----------
    entity: str
        Entity potentially carrying leading the

    Returns
    -------
    text_wo_leading_the: str
        Text freed from leading the
    """
    text_wo_leading_the = re.sub(r"^[Tt]he\s", "", entity)
    return text_wo_leading_the


def apply_abbreviations(summary: str, abbreviations: Dict) -> str:
    for expression_to_abbreviate, abbreviation in abbreviations.items():
        summary = re.sub(expression_to_abbreviate, abbreviation, summary)
    return summary


def clean_output_no_token_edit(summary: str) -> str:
    """Clean ouput to be nice to read. Does not change the token sequence. Only edits each token.

    Parameters
    ----------
    summary: str
        Raw summary to clean

    Returns
    -------
    summary: str
        Clean summary, ready to be read
    """
    summary = re.sub(r"\s*\.*\s*\n", " . ", summary)
    summary = re.sub(r"\s+$", "", summary)  # Remove ending space
    summary = " . ".join(
        [subsummary[0].upper() + subsummary[1:] for subsummary in summary.split(" . ")]
    )  # Leading capital letter
    return summary


def clean_output_token_edit(summary: str) -> str:
    summary = re.sub(r"(\s+)([\.,])", r"\2", summary)  # hello [.,] hi --> hello[.,] hi
    summary = re.sub(r"([A-Za-z])(\')([A-Za-z])", r"\1 \2 \3", summary)
    summary = re.sub(r"([A-Za-z])(\s*)(\')(\s*)(s)(\s+)", r"\1\3\5\6", summary)  # s' of possession
    summary = re.sub(r"n\s+\'\s+t", "n't", summary)  # Negation: couldn' t --> couldn't
    summary = re.sub(r"\sn\'t", "n't", summary)  # Negation: couldn' t --> couldn't
    summary = re.sub(r"([A-Za-z]+)(\s+)(\')(\s+)(ll)", r"\1\3\4\5", summary)  # Future: he ' ll --> he'll
    return summary


def is_abbrev(abbrev, text):
    abbrev = re.sub(r"^the ", "", abbrev.lower())
    text = re.sub(r"^the ", "", text.lower())
    pattern = r"(|.*\s)".join(abbrev)
    return re.match("^" + pattern, text) is not None


def apply_capital_words(summary: str, capital_words: List) -> str:
    for capital_word in capital_words:
        summary = re.sub(fr"(^|\s+)({capital_word.lower()})", fr"\1{capital_word}", summary)
    return summary

def postprocess_tags(tags):
    """Clean tags values.
    
    Parameters
    ----------
    tags: str
        Tags

    Returns
    -------
    cleaned_tags: str
        Cleaned tags
    """
    cleaned_tags = tags
    for tag, clean_tag in TAGS_DICT.items():
        cleaned_tags = cleaned_tags.replace(tag, clean_tag)
    return cleaned_tags



class Postprocessor(TransformerMixin):
    def __init__(self, verbose: bool = False):
        self.nlp = spacy.load("en_core_web_sm")
        self.verbose = verbose

    def _retrieve_abbreviations(self, text: str) -> Dict:
        """Retrieve potential abbreviations in plain text

        Parameters
        ----------
        text: str
            Text to be browsed

        Returns
        -------
        abbreviations: Dict
        """
        try:
            doc = self.nlp(text)
            abbreviations = {}
            for span_a in doc.ents:  # Naming wrt spaCy API
                entity_a = span_a.text
                if span_a.label_ not in ["GPE", "ORG"]:
                    continue
                for span_b in doc.ents:
                    entity_b = span_b.text
                    if entity_a == entity_b:
                        continue
                    if is_abbrev(entity_b, entity_a):
                        entity_bb = remove_leading_the(entity_b)
                        entity_aa = remove_leading_the(entity_a)
                        abbreviations[entity_aa] = entity_bb

            if self.verbose:
                print(f"\nCandidate abbreviations: {abbreviations}\n")
        except BaseException as e:
            logging.warning(e)
            return {}

        return abbreviations

    def _remove_compounds(self, summary: str) -> str:
        doc = self.nlp(summary)

        entities = [ent.text for ent in doc.ents]

        compound_idx_to_remove = []
        compunds_to_remove = []
        for idx, token in enumerate(doc):
            if (token.dep_ == "compound") and (not any([token.text.lower() in entity.lower() for entity in entities])):
                compound_idx_to_remove.append(idx)
                compunds_to_remove.append(token.text)

        if self.verbose:
            print(f"\nCompounds to remove: {compunds_to_remove}\n")

        list_attr = [
            LOWER,
            POS,
            ENT_TYPE,
            IS_ALPHA,
            DEP,
            LEMMA,
            LOWER,
            IS_PUNCT,
            IS_DIGIT,
            IS_SPACE,
            IS_STOP,
        ]
        np_array = doc.to_array(list_attr)
        mask_to_del = np.ones(len(np_array), np.bool)
        mask_to_del[compound_idx_to_remove] = 0

        np_array_2 = np_array[mask_to_del]
        doc2 = Doc(doc.vocab, words=[t.text for t in doc if t.i not in compound_idx_to_remove])
        doc2.from_array(list_attr, np_array_2)
        return doc2.text

    def _retrieve_capital_words(self, text: str):
        """
        """
        doc = self.nlp(text)
        capital_words = []
        for token in doc:
            if (len(token.text) > 3) and (token.is_title) and (not token.is_sent_start):
                capital_words.append(token.text)
        return set(capital_words)

    def transform(self, text: str, summary: str, format_text=True, abbreviate=True, remove_compounds=False,) -> str:
        """

        Parameters
        ----------
        summary: str
            Summary to postprocess

        Returns
        -------
        summary: str
            Postprocessed summary
        """
        try:
            if format_text:
                summary = clean_output_no_token_edit(summary)
                capital_words = self._retrieve_capital_words(text)
                summary = apply_capital_words(summary, capital_words)
                summary = clean_output_token_edit(summary)

            if abbreviate:
                abbreviations = self._retrieve_abbreviations(text)
                summary = apply_abbreviations(summary, abbreviations)

            if remove_compounds:
                summary = self._remove_compounds(summary)
            return summary
        except BaseException as e:
            logging.warning(e)
            return summary
