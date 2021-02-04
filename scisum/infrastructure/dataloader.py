"""This module loads data from a flat file.

Classes
-------
DataLoader

"""

import logging
import numpy as np
import pandas as pd
import os

from scisum.config import STANFORD, MAXPLANCK, HAL, DATA_DIR
from scisum.config import TEXTS, SUMMARIES, PATH, FILENAME, TITLES, TAGS, DROP_FIRST, TASKS, SUBDATASET_PARTS
from scisum.config import MP_FRACTION, MP_RAND_STATE


class DataLoader:   
    """Load data from a CSV file.
    
    Attributes
    ----------
    source : dict
        Dictionnary containing the main information about the csv file as defined in the config.py file.
    data : pandas.DataFrame
        Pandas DataFrame containing the whole data from the csv file

    """

    def __init__(self, source):
        
        self.source = source
        self.data = self.all_data

    @property
    def all_data(self):
        """Load data from the csv file.

        Returns
        -------
        df : pandas.DataFrame
           Dataset containing all columns from the csv file

        """        
        if self._check_file_extension():
            df = self._read_file()
            return df

    def get_task_data(self, task, type_dataset=SUBDATASET_PARTS[2]):
        """Load the columns used for a given task.

        Parameters
        ----------
        task : str
            Description of the task. One of summary_generation, title_generation, tags_recovering
        type_dataset : str
            Train or test set 
        
        Returns
        -------
        res : pandas.DataFrame or tuple of pandas.DataFrame objects depending on the task.
            Dataset(s) containing column(s) for the given task

        """    
        df = self.data.copy()

        if task in TASKS[0:2] :

            data_eval = df.sample(frac=MP_FRACTION, random_state=MP_RAND_STATE)
            data_train = df.drop(data_eval.index)   

            if type_dataset==SUBDATASET_PARTS[0] :
                df = data_train.copy() 
            elif type_dataset == SUBDATASET_PARTS[1]:
                df = data_eval.copy()

        if task==TASKS[0]:
            df = df.dropna(subset=[self.source[TEXTS],self.source[SUMMARIES]])
            texts = df[self.source[TEXTS]]
            summaries = df[self.source[SUMMARIES]]
            res = (texts, summaries) 
            return res

        if task==TASKS[1]:
            df = df.dropna(subset=[self.source[SUMMARIES],self.source[TITLES]])
            summaries = df[self.source[SUMMARIES]]
            titles = df[self.source[TITLES]]
            res = (summaries, titles)
            return res
        
        if task == TASKS[2]:
            df = self.data.copy()
            df = df.dropna(subset=[self.source[SUMMARIES]])
            summaries = df[self.source[SUMMARIES]]
            res = (summaries, None)
            return res
        
        if task == TASKS[3]:
            df = self.data.copy()
            df = df.dropna(subset=[self.source[TEXTS]])
            texts = df[self.source[TEXTS]]
            res = (texts, None)
            return res
        
    
    def _check_file_extension(self):
        logging.info('-'*20)
        logging.info('Check file extension ..')
        
        if self.source[FILENAME].endswith('.csv'):
            return True
        else:
            logging.info('.. ERROR: Extension must be .csv')
            raise FileExistsError('Extension must be .csv')

    def _read_file(self):
        logging.info('-'*20)
        logging.info('Load data ..')

        try:
            if self.source[DROP_FIRST]:
                index_col=0
            else:
                index_col=None
            df = pd.read_csv(self.source[PATH], index_col=index_col)
            logging.info('.. Done \n')
            return df

        except FileNotFoundError as error:
            logging.info('.. FileNotFoundError')
            raise FileNotFoundError('File not found')


if __name__=="__main__":

    dataloader = DataLoader(STANFORD)

    data = dataloader.data
    print(data.columns,'\n')

    '''
    texts, summaries = dataloader.get_task_data(task='summary_generation', type_dataset="train")
    print("summary generation - train")
    print(texts.iloc[0],'\n')
    print(summaries.iloc[0],'\n')  
    print(len, len(texts),'\n')
    '''
    '''
    texts, summaries = dataloader.get_task_data(task='summary_generation', type_dataset="test")  
    print("summary generation - test")
    print(texts.iloc[0],'\n')
    print(summaries.iloc[0],'\n')  
    print(len, len(texts),'\n')
    '''

    summaries, titles = dataloader.get_task_data(task='title_generation', type_dataset="train")  
    print("title generation - train")
    print(summaries.iloc[0],'\n')
    print(titles.iloc[0],'\n')
    print(len, len(summaries),'\n')

    summaries, titles = dataloader.get_task_data(task='title_generation', type_dataset="test")  
    print("title generation - test")
    print(summaries.iloc[0],'\n')
    print(titles.iloc[0],'\n')
    print(len, len(summaries),'\n')


    '''
    dataloader = DataLoader(HAL)

    data = dataloader.data
    print(data.columns,'\n')
    
    summaries, titles = dataloader.get_task_data(task='title_generation')
    print(summaries.iloc[0],'\n')
    print(titles.iloc[0],'\n')  
    
>>>>>>> scisum/infrastructure/dataloader.py
    from scisum.config import DATA_DIR
    
    path_f = os.path.join(DATA_DIR, HAL[FILENAME])
    print(path_f,'\n')
    df = pd.read_csv(path_f)
    print(df.head())
    '''

    