import os
import logging
import pickle

# DIR PATHS
CODE_DIR =  os.path.dirname(__file__)
REPO_DIR = os.path.abspath(os.path.join(CODE_DIR, '../'))
DATA_DIR = os.path.join(REPO_DIR, 'data')
IMG_DIR = os.path.join(REPO_DIR, 'images')
MODELS_DIR = os.path.join(REPO_DIR, "models")
LOGO_PATH =  os.path.join(IMG_DIR, "bart_sci.jpeg")
MAXPLANK_LOGO_PATH =  os.path.join(IMG_DIR, "max-planck-institute-tubingen.jpeg")
STANFORD_LOGO_PATH =  os.path.join(IMG_DIR, "stanford_logo.jpeg")

LOGS_DIR = os.path.join(REPO_DIR, 'logs')


def enable_logging(log_filename, logging_level=logging.DEBUG):
    """Set loggings parameters.

    Parameters
    ----------
    log_filename: str
    logging_level: logging.level

    """
    with open(os.path.join(LOGS_DIR, log_filename), 'a') as file:
        file.write('\n')
        file.write('\n')

    LOGGING_FORMAT = '[%(asctime)s][%(levelname)s][%(module)s] - %(message)s'
    LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    logging.basicConfig(
        format=LOGGING_FORMAT,
        datefmt=LOGGING_DATE_FORMAT,
        level=logging_level,
        filename=os.path.join(LOGS_DIR, log_filename)
    )

#FILES KEYS
FILENAME = "filename"
PATH = "path"
TITLES = "titles"
SUMMARIES = "summaries" 
TEXTS = 'texts'
LABELS = 'labels'
DATES = "date"
TAGS = 'tags'
DROP_FIRST = "Drop first colummn"
DOWNLOAD= "Download information"
TOKENIZER = "tokenizer"

#STANFORD NEWS FILE
STANFORD_COLS = ["Title","Summary","Content","Date"]
STANFORD ={
    FILENAME : "stanford_articles.csv", 
    TITLES : STANFORD_COLS[0], # Titles
    SUMMARIES : STANFORD_COLS[1], # Summaries
    TEXTS : STANFORD_COLS[2], # Texts
    DATES : STANFORD_COLS[3], # Dates
    DROP_FIRST : True,

}
STANFORD[PATH] = os.path.join(DATA_DIR, STANFORD[FILENAME])
STANFORD[DOWNLOAD] = {STANFORD[FILENAME] : '1dCi9lASh3VS4T36mBM8UNv3OxxFHuoUl'}

#MAX PLANCK NEWS FILE
MAXPLANCK_COLS = ["title","date","summary","content","references","tags"]
MAXPLANCK ={
    FILENAME : "complete_articles_max_planck.csv", 
    TITLES : MAXPLANCK_COLS[0],
    SUMMARIES : MAXPLANCK_COLS[2],
    TEXTS : MAXPLANCK_COLS[3],
    LABELS : MAXPLANCK_COLS[5],
    DATES : MAXPLANCK_COLS[1],
    DROP_FIRST : True
     
    
}
MAXPLANCK[PATH] = os.path.join(DATA_DIR, MAXPLANCK[FILENAME])
MAXPLANCK[DOWNLOAD] = {MAXPLANCK[FILENAME] : '1XMYRdNZ8ZYkFLH0CeyJVxUXb-ZHkypt9'}


#HAL FILE
HAL_COLS = ["title","summary","tags"]
HAL ={
    FILENAME : "hal_summaries.csv", 
    TITLES : HAL_COLS[0],
    SUMMARIES : HAL_COLS[1],
    TAGS : HAL_COLS[2],
    DROP_FIRST : False,
}

HAL[PATH] = os.path.join(DATA_DIR, HAL[FILENAME])
HAL[DOWNLOAD] = {HAL[FILENAME] : '1SC3iEokTutMMTNgpNDLWRDfMNErBYI1M'}

DATASETS = {"Stanford": STANFORD,
    "Max Planck":MAXPLANCK,
    "HAL": HAL,
    }

SUBDATASET_PARTS=["train", "eval", "all"]
# PARAMETRES FOR SPLIT TRAIN/TEST
MP_FRACTION = 0.03 
MP_RAND_STATE = 42 


#MODELS
#MODEL_NAME = "./BartScisum_1"
#MODEL_NAME = "sshleifer/distilbart-cnn-6-6"
#TOKENIZER_NAME = "sshleifer/distilbart-cnn-6-6"


BART_SCISUM = {
    FILENAME: "bartscisum",
    DOWNLOAD: {
        'training_args.bin': '12hNb8hTUEjjbyYJRfoM9JAg09S0OonRF',
        'pytorch_model.bin': '1l3nIjuoGCS8N_jfGyaZnt58eIAMiG-Ts',
        'config.json': '1K6T5su6_ZFVnYoXbaq0kG7vuFArrTVTM',
     },
}
BART_SCISUM[PATH] = os.path.join(MODELS_DIR, BART_SCISUM[FILENAME])
BART_SCISUM[TOKENIZER] = "sshleifer/distilbart-cnn-6-6"


TAGS_SCISUM = {
    FILENAME: "tags_best_model",
    DOWNLOAD: {
        'config.json': '1bflpXNu7y5wlVcAyysgR4kJ7mPEGXOYj',
        'merges.txt': '1yMLJXm57QpWQsWTAsiuklHzdAO9cjlgl',
        'model_args.json': '1ewSFzdtsTbr-lK_nUqGNYAhmn-s8Scbu',
        'pytorch_model.bin': '1Cwfg2jSmZe46rXVqmEjFyyQ8z0DtOBQf',
        'special_tokens_map.json': '1BfOL6w_1OZO-6PibPfpg1tg_stFI1fYD',
        'tokenizer_config.json': '1Gg67XSg8B2QbZ5ZF12x0n8GtRXwMcNXj',
        'training_args.bin': '1cG20C1UDkdzXjP6bVD2vHqTxAvzoo1z9',
        'vocab.json': '1cu8ZzY_ZtEQh4KqhUablkhRCP2x8FYlf'
    },
}

TAGS_DICT = {
    'chim': 'Chemistry',
    'info': 'Computer Science',
    'math': 'Mathematics',
    'phys': 'Physics',
    'scco': 'Cognitive Neuroscience',
    'sde': 'Environmental Science',
    'sdv': 'Life Science',
    'shs': 'Human and Social Science',
    'spi': 'Engineering Sciance'
}



BART_MP_TITLE = {
    FILENAME: "distilbart-xsum-6-6",
    DOWNLOAD: {
        'training_args.bin': '1xaXfjd8tgSub6jCEa_Ek5LYdUn-DaGdm',
        'pytorch_model.bin': '1uGdbQqAAmIKXbdtldwGhokaJNPW_ZICs',
        'config.json': '1ty725DDUJq9P0wZJ-Xfcclaq8FUA8HoQ',
     },
}

BART_MP_TITLE[PATH] = os.path.join(MODELS_DIR, BART_MP_TITLE[FILENAME])
BART_MP_TITLE[TOKENIZER] = "sshleifer/distilbart-cnn-6-6"

MODELS = {"Bartscisum": BART_SCISUM,
    "distilbart-xsum-6-6": BART_MP_TITLE,
    "Tagsscisum": TAGS_SCISUM,
}


TEXT_SPLIT_MAX_LENGTH = 1000
MIN_TITLE = 1
MAX_TITLE = 15

# MODEL FOR TAGS
CLASSIF_MODEL_NAME = "roberta"
CLASSIF_MODEL_PATH = os.path.join(MODELS_DIR, 'tags_best_model')
CUDA = False

# MULTI LABEL BINARIZER INVERSION FOR TAGS RECOVERING
with open(os.path.join(REPO_DIR, 'models/mlb.pkl'), 'rb') as f:
    MLB = pickle.load(f)


#I-TRANSLATE
ITRANSLATE_K = 'd2aefeac9dc661bc98eebd6cc12f0b82'
URL_ITRANSLATE_API = "https://web-api.itranslateapp.com/v3/texts/translate"

TASKS = ["summary_generation", "title_generation", "tags_recovering", "translation" ]

