# Scisum

Projet N°2 - Computer Vision / NLP
This project aims to generate relevant summaries of scientific press release.

Copyright : 2020, Dorota Bailly & Robin & Antoine Meilliez & Robin Timsit

___

# Getting Started

## 1. Clone this repository

```
$ git clone <this project>
$ cd <this project>
```

## 2. Initialisation and setup of the environment

Run at start

```
$ source activate.sh
```
    
This command will : 
- Add the project directory to your PYTHONPATH
- Install the requiered dependencies
- Create (if necessary) the virtual environmnet
- Activate the virtual environment

## 3. Download databases and trained models

```
$ source download_files.sh
```

This command will download all files required to run the web app.
Files are heavy so, depending on your internet connection, it could take time.

## 4. Visualization with streamlit


If you want to use a web application to play with the model, run 

```
$ streamlit run scisum/application/app.py
```

# Project Organization
------------
    ├── activate.sh
    ├── download_files.sh       <- Bash script to download models and databases.
    ├── run.sh	<- Bash script to run web app.	
    ├── README.md          <- The top-level README for users and developers using this project.
    ├── data          <- Databases.
    │
    ├── models             <- Trained models.
    │   ├── bartscisum        <- Summarization model.
    │   ├── distilbart-xsum-6-6        <- Title generation model.
    │   ├── tags_best_model        <- Tags recovering model.
    │   ├── mlb.pkl        <- Multilabel binarizer.
    │
    ├── docs
    │   ├── build  
    │   ├── make.bat       
    │   └── Makefile
    │   └── source            
    │
    └── images        <- Images for web app.
    │
    ├─ poetry.lock            <- Requirements for developpers (needs poetry).
    ├─ pyproject.toml            <- Requirements for developpers (needs poetry). 
    │
    ├── scisum                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes scisum a Python module
    │   ├── config.py    <- User and developpers settings
    │   │
    │   ├── infrastructure           <- Scripts to load and clean data.
    │   │   └── dataloader.py
    │   │   └── file_downloader.py
    │   │   └── news_parser.py
    │   │   └── utils.py
    │   │
    │   ├── domain         <- Scripts to clean features and models
    │   │   ├── model.py
    │   │   └── postprocessing.py
    │   │   ├── tokenizer.py
    │   │   ├── translate.py
    │   │
    │   └── application  <- Web app scripts
    │   │   ├── app.py
    │   │   ├── dashboards
    │   │   ├── utils

--------
