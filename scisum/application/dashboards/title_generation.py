import streamlit as st

from scisum.application.utils.utils import HASH_FUNCS, HTML_WRAPPER
from scisum.application.utils.data_loader import load_data
from scisum.config import MODEL_NAME, TOKENIZER_NAME, TEXT_SPLIT_MAX_LENGTH, DATASETS, TASKS
from scisum.domain.model import SummerizationModel
from scisum.application.utils.display import ExampleDisplayer
from scisum.domain.postprocessing import Postprocessor


import time

@st.cache(hash_funcs=HASH_FUNCS)
def fetch_title_model():
    model_name, tokenizer_name,framework, text_split_max_length = MODEL_NAME, TOKENIZER_NAME, "pt", TEXT_SPLIT_MAX_LENGTH
    return SummerizationModel(model_name=model_name, tokenizer_name=tokenizer_name,framework=framework, text_split_max_length=text_split_max_length)


@st.cache(hash_funcs=HASH_FUNCS)
def fetch_summarization_utils():
    return ExampleDisplayer(), Postprocessor(verbose=False)

def title_generation():
    task = TASKS[1]
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    # Load model
    status_text.text("Load model")
    st.write("## Load Model 🔮 ")
    start = time.time()
    model = fetch_title_model()
    duration = f"{(time.time() - start):.2f}"
    st.write(f"Time to load model  : {duration} seconds")
    progress_bar.progress(60)

    # Choose input
    """dataset_options = list(DATASETS.keys())+["Text input"]
    dataset = st.sidebar.selectbox("Choose a dataset",dataset_options)
    if dataset in DATASETS.keys():
        status_text.text("Load Data")
        st.write(f"## Load {dataset} Data 📥 ")
        summaries, titles = load_data(DATASETS[dataset], progress_bar, task)
        status_text.text("Select an article")
        st.write("## Select an article 📰 ")
        text_number = st.number_input("Article number", value=1)
        text = summaries.iloc[text_number]

    elif dataset == "Text input":
        status_text.text("Enter input")
        st.write("## Enter input ⌨️ ")
        text = st.text_input("Input text", "Gotta see both sides of the story.")
    progress_bar.progress(60)"""
    dataset, text, title = load_data(status_text, progress_bar, task)

    if not model: 
        model = fetch_title_model()
    verbose=True
    translate = False
    #st.write("## Generating ... ⏳")
    ratio = st.sidebar.slider("Ratio", 0.1, 1.0)  
    st.write("### Original lead paragraph")
    st.write(text)
    
    if verbose:
        duration = f"{(time.time() - start):.2f}"
        st.write("Time to summarise  : " + duration + " seconds")
    progress_bar.progress(60)

    # Post-processing
    status_text.text("Results")
    start = time.time()
    candidate = model.generate_title(text)
    duration = f"{(time.time() - start):.2f}"
    st.write("Time to generate  : " + duration + " seconds")
    progress_bar.progress(60)
    st.write("## Results 🔎")
    if verbose:
        status_text.text("Post-processing")
        st.write("## Post-processing 🔎")
    exampleDisplayer, postProcessor = fetch_summarization_utils()

    start = time.time()
    candidate_post_process = postProcessor.transform(text, candidate)
    duration = f"{(time.time() - start):.2f}"

    st.write("Time to post-process  : " + duration + " seconds")
    st.write("### Generated title")

    #html = exampleDisplayer.display_simple(candidate, jupyter=False)
    html = exampleDisplayer.display_simple(candidate_post_process, jupyter=False)
    st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)
    
    if dataset in DATASETS.keys():
        st.write("### Original title")
        html = exampleDisplayer.display_simple(title, jupyter=False)
        st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)
    if translate :
        candidate_post_process = translate_text(candidate_post_process)
    if verbose:
        duration = f"{(time.time() - start):.2f}"
        st.write("Time to post-process  : " + duration + " seconds")
    st.write("### Generated summary")

    st.write("### Original lead paragraph")
    html = exampleDisplayer.display_simple(text, jupyter=False)
    if translate:
        html = candidate_post_process
    else :
        html = exampleDisplayer.display_simple(candidate_post_process, jupyter=False)
    st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)
    progress_bar.progress(100)
    status_text.text("Complete")
    st.button("Re-run")