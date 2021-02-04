import streamlit as st
from scisum.config import DATASETS
#from scisum.infrastructure.utils import fetch_data
import time
from scisum.infrastructure.dataloader import DataLoader



def load_data(status_text, progress_bar, task):
    # Choose input
    dataset_options = list(DATASETS.keys())+["Text input"]
    dataset = st.sidebar.selectbox("Choose a dataset",dataset_options)

    if dataset in DATASETS.keys():
        status_text.text("Load Data")
        st.write(f"## Load {dataset} Data 📥 ")
        start = time.time()
        data = DataLoader(DATASETS[dataset]).get_task_data(task=task)
        texts=data[0]
        duration = f"{(time.time() - start):.2f}"
        st.write("Time to load data : " + duration + " seconds")
        progress_bar.progress(30)
        #texts, summaries = _load_data(DATASETS[dataset], progress_bar)
        status_text.text("Select an article")
        st.write("## Select an article 📰 ")
        text_number = st.number_input("Article number", value=1)
        text = texts.iloc[text_number]
        target = data[1].iloc[text_number] if data[1] is not None else None
    elif dataset == "Text input":
        status_text.text("Enter input")
        st.write("## Enter input ⌨️ ")
        text = st.text_input("Input text", "Write your text here.")
        target = None
    return dataset, text, target

