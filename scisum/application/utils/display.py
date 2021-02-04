from rouge import Rouge
from spacy import displacy
from typing import List, Tuple
import spacy
import numpy as np


def compute_aggregate(texts, agg_function=np.mean):
    return agg_function([len(text.split(" ")) for text in texts])


class ExampleDisplayer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def display_all(
        self, candidates: List[Tuple], reference: str, initial_text: str, with_score=True,
    ):
        """ Nicely-ish displayed

        Parameters
        ----------
        candidates: List[Tuple]
            model_name, summary
        """
        print(f"Length of initial text: {len(initial_text)}")
        rouge = Rouge()
        m = "Reference summary:"
        doc = self.nlp(reference)
        displacy.render(doc, style="ent", jupyter=True)



        for model_name, summary in candidates:
            decrease = int((len(summary) - len(initial_text)) / len(initial_text) * 100)
            m = f"{model_name} summary (decrease of {decrease}%):"
            print(m)
            print("-" * len(m))
            if with_score:
                rouge_score = rouge.get_scores(summary, reference)
                print(rouge_score)
                print("\n")
            doc = self.nlp(summary)
            displacy.render(doc, style="ent", jupyter=True)
            print("\n")

    def display_simple(self, text, jupyter=True, no_tags=False):
        if no_tags:
            return text
        else:
            doc = self.nlp(text)
            return displacy.render(doc, style="ent", jupyter=jupyter)
