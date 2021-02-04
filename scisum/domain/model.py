"""This module performs predictions on text files.

Classes
-------
SummerizationModel
TagsRecoveringModel

"""

from transformers import pipeline
from simpletransformers.classification import MultiLabelClassificationModel
import numpy as np
from scisum.domain.tokenizer import Tokenizer
from scisum.config import TEXT_SPLIT_MAX_LENGTH, MIN_TITLE, MAX_TITLE
from scisum.config import CLASSIF_MODEL_NAME, CLASSIF_MODEL_PATH, CUDA, MLB
import logging


class SummerizationModel:
    """Wrapper to perform both summarization and title generation. We allow ourselves to centralize everything here
    as it relies on the same model.

    Attributes
    ----------
    model_name: str
        Name of the model
    tokenizer_name: str
        Name of the tokenizer
    framework: str
        Framework to leverage (pt or tf)
    text_split_max_length: int
        text_split_max_length - attribute of the Tokenizer class, used to split_text 
    tolerance : int
        tolerance around ratio text /summary in number of words

    """

    def __init__(self, model_name: str, tokenizer_name:str, framework: str, text_split_max_length: int, tolerance: int = 5):
        self.tokenizer = Tokenizer(tokenizer_name=tokenizer_name, text_split_max_length=text_split_max_length)
        self.abstractive_model = pipeline("summarization", model=model_name, tokenizer=tokenizer_name, framework=framework)
        self.tolerance = tolerance

    
    def summarise(self, text: str, ratio: float, summarize_only_first_split: int, tolerance: int):
        """Summarise a text.

        Parameters
        ----------
        text: str
            Text to summarise
        ratio: float
            Ratio text / summary
        summarize_only_first_split : int
            Summarize only first split if True (1)
        tolerance: int
            tolerance around ratio text /summary in number of words

        Returns
        -------
        candidate: str
            Summary of the text
        """
        text_split = self.tokenizer.split_text(text)
        if summarize_only_first_split:
            max_length = (ratio * text_split[0][1]) + tolerance
            min_length = (ratio * text_split[0][1]) - tolerance

            candidate = self.abstractive_model(text_split[0][0], max_length=max_length, min_length=min_length)
        else:
            candidate = []
            for split in text_split:
                max_length = round(ratio * split[1]) + tolerance 
                min_length = max(1, round(ratio * split[1]) - tolerance)
                res = self.abstractive_model(split[0], max_length=max_length, min_length=min_length)
                print(res)
                candidate.append(res)
            candidate = "\n".join([c[0]["summary_text"] for c in candidate])
        return candidate

    

    def generate_title(self, text: str, min_title=MIN_TITLE, max_title=MAX_TITLE):
        """Generate title from a lead paragraph.

        Parameters
        ----------
        text: str
            Text of the lead paragraph
        min_title: int
            Min length of the title
        max_title: int
            Max length of the title

        Returns
        -------
        candidate : str
            Title of the text
        """

        candidate = self.abstractive_model(text, max_length=max_title, min_length=min_title)
        return candidate[0]['summary_text']

class TagsRecoveringModel:
    """Perform tags recovering task.

    Attributes
    ----------
    model_name: str
        Generic name of the model
    model_path: str
        Path to the trained model

    """

    def __init__(self, model_name: str = CLASSIF_MODEL_NAME, model_path: str = CLASSIF_MODEL_PATH):
        self.candidate = MultiLabelClassificationModel(model_name, model_path, use_cuda=CUDA, num_labels=9)

    def generate_tags(self, text: str):
        """Generate tags from title and summary.

        Parameters
        ---------
        text: str
            Text of the lead paragraph.
        
        Returns
        -------
        predicted_tags: list
            List of tuple containing predicted tags.
        """
        tags_predictions = self.candidate.predict([text])[0]
        print('un truc')
        predicted_tags = MLB.inverse_transform(np.array(tags_predictions))
        return predicted_tags


if __name__=="__main__":

    from scisum.config import TEXT_SPLIT_MAX_LENGTH,  MLB
    from scisum.infrastructure.dataloader import DataLoader

    from scisum.config import BART_MP_TITLE, BART_SCISUM
    from scisum.config import FILENAME, PATH, TOKENIZER

    from scisum.config import MAXPLANCK, STANFORD
    

    texts, summaries= DataLoader(MAXPLANCK).get_task_data(task='summary_generation', type_dataset="train")
    summaries, titles = DataLoader(MAXPLANCK).get_task_data(task='title_generation', type_dataset="train")

    print("model:\n",BART_MP_TITLE[PATH])
    model_name = BART_MP_TITLE[PATH]
    tokenizer_name = BART_MP_TITLE[TOKENIZER]
    framework = "pt" 
    text_split_max_length = TEXT_SPLIT_MAX_LENGTH
 
    #model_tit = SummerizationModel(model_name=model_name, tokenizer_name=tokenizer_name,framework=framework, text_split_max_length=text_split_max_length)
    #text = summaries.iloc[0]
    #tit = model_tit.generate_title(text)
    #print("title:\n",tit,'\n')
    #print("original title:\n",titles.iloc[0],'\n')
    

    '''
    print("model:\n",BART_SCISUM[PATH])
    model_name = BART_SCISUM[PATH]
    tokenizer_name = BART_SCISUM[TOKENIZER]
    framework = "pt" 
    text_split_max_length = TEXT_SPLIT_MAX_LENGTH

    model_sum = SummerizationModel(model_name=model_name, tokenizer_name=tokenizer_name,framework=framework, text_split_max_length=text_split_max_length)
    
    text = texts.iloc[0]
    summ = model_sum.summarise(text, 0.1, 0, 15)
    print("\n summary:\n",summ,'\n')
    '''
    
    model_tags = TagsRecoveringModel(model_name=CLASSIF_MODEL_NAME, model_path=CLASSIF_MODEL_PATH)
    text = summaries.iloc[1]
    tags = model_tags.generate_tags(text)
    print("tags:\n",tags,'\n')
    

    
    
  
