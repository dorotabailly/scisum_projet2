"""Performs tokenization.

Classes
-------
Tokenizer

"""

from transformers import BartTokenizer
from typing import List, Tuple


class Tokenizer:
    """
    Attributes
    ----------
    max_length: int
        Length of texts used to split the text
    """

    def __init__(self, tokenizer_name: str, text_split_max_length: int):
        self.text_split_max_length = text_split_max_length
        self.tokenizer = self.load_tokenizer(tokenizer_name)

    def load_tokenizer(self, model: str):
        """
        Parameters
        ----------
        model: str
            model from which we want to load the tokenizer

        Returns
        -------
        tokenizer: transformers.PreTrainedTokenizer
            The tokenizer
        """
        tokenizer = BartTokenizer.from_pretrained(model, truncation=True)
        return tokenizer

    def tokenize(self, text):
        return self.tokenizer.tokenize(text)

    def split_text(self, text: str,) -> List[Tuple]:
        """
        Parameters
        ----------
        text: str
            Text to split

        Returns
        -------
        text_split: list
            List of tuple for each split of the text
            First element is the text part and second element is the number of tokens for this split
        """
        # Code from Florian's project
        tokenized_text = self.tokenizer.encode(text, add_special_tokens=False)
        n_tokens = len(tokenized_text)
        text_split = []
        batch = []
        total_tokens_in_batches = 0
        for idx, token in enumerate(tokenized_text):
            batch.append(token)
            if ((idx > 0) and (((idx + 1) % (self.text_split_max_length)== 0) or (idx == (n_tokens - 1)))) or (
                (idx == 0) and (n_tokens == 1)
            ):
                len_batch = len(batch)
                total_tokens_in_batches += len_batch
                batch = self.tokenizer.decode(batch)
                text_split.append((batch, len_batch))
                batch = []
        assert n_tokens == total_tokens_in_batches
        return text_split



if __name__=="__main__":

    from scisum.config import TOKENIZER_NAME, MODEL_NAME
    text_input = "A simple ventilation system removes 90 percent of respiratory aerosols which potentially include coronavirus particles, from indoor air In future, it will be far easier to remove infectious aerosols from the air in classrooms and other spaces. Researchers at the Max Planck Institute for Chemistry have built a ventilation system that can be replicated using materials from a DIY store. A comprehensive school in Mainz has already tested the system. The Rhineland-Palatinate Ministry of Education is currently testing use of the system in other schools. A construction report is available online. As the Covid-19 crisis continues, schools are faced with a problem: how to properly ventilate classrooms during lessons. Working together with the Integrated Comprehensive School Mainz-Bretzenheim, researchers at the Max Planck Institute for Chemistry have now successfully tested an exhaust air system that can remove around 90 percent of artificially generated aerosol particles from classrooms under laboratory conditions. The principle behind this system is that every human being produces warm air that rises upwards. When this airflow is directed outside, it takes aerosol particles, and possible coronavirus particles, with it. The design is very simple and was implemented using DIY store materials worth about â‚¬ 200. A wide hood at two meter height, connected to a tube, hangs above each desk. All the tubes lead into a central duct, which in turn leads outside through a tilted window. A fan at the end of the duct ensures that the air is actively transported outside. Air inlet can be comprised of an open door or a second tilt-open window. The design is the brainchild of Frank Helleis, whose wife works as a teacher in Mainz. It was also through her that contact with the school was established. â€œIt sounded so simple and convincing that we immediately decided to get involved,â€ says Roland Wollowski, Headmaster at the Integrated Comprehensive School Mainz-Bretzenheim. This development quickly led to a prototype, which Frank Helleis and his colleagues assembled in a classroom using cardboard boxes with heat and aerosol sources as surrogates for pupils. Testing was done all summer and is going on ever since. Currently, the system is being validated in real school operations. â€œOur measurements have shown that the hood-based exhaust air system continuously removes over 90 percent of aerosols under laboratory conditions,â€ states Frank Helleis. Although the simple system also works without the funnel-shaped hoods above the individual desks, they increase the efficiency significantly. The physicist proved this with aerosol spectrometers and artificially generated aerosols. Based on the available measurement results, one can expect a substantial proportion of potentially infectious aerosol particles from breathing air to be removed under real teaching conditions as well.  Frank Helleis has deliberately designed the system for practical use. Due to its low material and operating costs, it could turn out to be a clever alternative to expensive filter systems and ventilation by shortly wide opening the windows. The modular system doesnâ€™t take up much space (only requiring a power socket and a tilting window or skylight), so itâ€™s also suitable for use in the likes of sports halls. Discussions as to whether the system can also be used at other schools in Rhineland-Palatinate are currently ongoing at the Rhineland-Palatinate Ministry of Education, which has already tested the functionality of the structure on site. â€œOur board of education, the City of Mainz, is also inspired by the project, and we are receiving constructive support in this respect,â€ reports Roland Wollowski. â€œWeâ€™re thrilled about the excellent cooperative relationship with the Max Planck Institute for Chemistry and have decided to kit out as many classrooms as possible over the coming weeks with the active assistance of the entire school community. Ventilation-related energy losses are also being reduced through this, which in turn benefits the climate.â€ At present, some manual skills are still needed to install the system, since the individual parts have to be assembled and mounted individually. Frank Helleis and his colleagues prepared a consturciton report to keep the barrier for replication as low as possible. The Mainz researchers are also in contact with companies that could produce individual molded parts for the design, making it even easier to recreate. Frank Helleis, who is known for being a creative inventor at the Max Planck Institute for Chemistry in Mainz, firmly believes that the system will remain in use after the pandemic. â€œOur system also solves the long-standing problem of CO2 in classrooms, because it not only transports aerosols outside. It also cuts CO2 accumulation, helping students to concentrate better on their lessons.â€ Of course, this can also be achieved by professional ventilation systems. With suitable designs and dimensions, such systems should have better properties but are hitherto not available in many schools. In the current pandemic and exceptional situation, numerous scientific institutions are actively trying to help solve pending problems. The makeshift ventilation system presented here resulted from a specific need for short-term and easily implementable measures to reduce the risk of Covid-19 infection through aerosol transmission in local schools. Because of very positive responses and increasing demand, the construction report was published. The report also points out that the documentation is of provisional nature and will be further supplemented as appropriate."
    text_input = "A simple ventilation system removes 90 percent of respiratory aerosols which potentially include coronavirus particles,"

    tok = Tokenizer(TOKENIZER_NAME, text_split_max_length=5)

    print("\n max_length_for_split (attribute of our class):", tok.text_split_max_length,'\n')

    print("\n tokenizer - max_len_single_sentence:", tok.tokenizer.max_len_single_sentence ,'\n')
    print("\n tokenizer - max_model_input_sizes:", tok.tokenizer.max_model_input_sizes ,'\n')
    print("\n tokenizer - model_max_length:", tok.tokenizer.model_max_length ,'\n')

    print("config of the tokenizer", tok.tokenizer,'\n')
    
    tokenized_text = tok.tokenizer.tokenize(text_input)
    print("tokenized_text\n :", tokenized_text)
    print(len(tokenized_text),'\n')

    tokenized_text = tok.tokenizer.encode(text_input)
    print("encoded text\n", tokenized_text)
    print("encoded text\n",len(tokenized_text),'\n')

    decoded_text = tok.tokenizer.decode(tokenized_text)
    print("decoded text\n:", decoded_text,'\n')
    print(decoded_text.split(),'\n')
    print("decoded text\n:",len(decoded_text.split()),'\n')

    tokenized_text = tok.tokenizer.encode(text_input, add_special_tokens=False)
    print("tokenized text without special tokens:\n", tokenized_text)
    print("tokenized text without special tokens:", len(tokenized_text),'\n')

    decoded_text = tok.tokenizer.decode(tokenized_text)
    print("decoded text\n:", decoded_text,'\n')
    print(decoded_text.split(),'\n')
    print("decoded text\n:",len(decoded_text.split()),'\n')


    tok = Tokenizer(TOKENIZER_NAME, text_split_max_length=5)    

    tokenized_text = tok.tokenizer.encode(text_input, add_special_tokens=False)
    print("tokenized text without special tokens:\n", tokenized_text)
    print("tokenized text without special tokens:", len(tokenized_text),'\n')

    res = tok.split_text(text_input)
    print(res)

 

