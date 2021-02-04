import streamlit as st
import time
#from scisum.infrastructure.utils import fetch_data
from scisum.infrastructure.dataloader import DataLoader
from scisum.config import TEXT_SPLIT_MAX_LENGTH, DATASETS,  TASKS
from scisum.config import BART_MP_TITLE, BART_SCISUM
from scisum.config import FILENAME, PATH, TOKENIZER
from scisum.config import CLASSIF_MODEL_NAME, CLASSIF_MODEL_PATH
from scisum.domain.model import SummerizationModel, TagsRecoveringModel
from scisum.domain.postprocessing import Postprocessor, postprocess_tags
from scisum.domain.translate import translate_text

from scisum.application.utils.display import ExampleDisplayer
from scisum.application.utils.utils import HASH_FUNCS, HTML_WRAPPER
from scisum.application.utils.data_loader import load_data


@st.cache(hash_funcs=HASH_FUNCS)
def fetch_summerization_model():

    model_name = BART_SCISUM[PATH]
    tokenizer_name = BART_SCISUM[TOKENIZER]
    framework = "pt" 
    text_split_max_length = TEXT_SPLIT_MAX_LENGTH

    return SummerizationModel(model_name=model_name, tokenizer_name=tokenizer_name,framework=framework, text_split_max_length=text_split_max_length)

@st.cache(hash_funcs=HASH_FUNCS)
def fetch_title_model():

    print("model:\n",BART_MP_TITLE[PATH])
    model_name = BART_MP_TITLE[PATH]
    tokenizer_name = BART_MP_TITLE[TOKENIZER]
    framework = "pt" 
    text_split_max_length = TEXT_SPLIT_MAX_LENGTH

    return SummerizationModel(model_name=model_name, tokenizer_name=tokenizer_name,framework=framework, text_split_max_length=text_split_max_length)

@st.cache(hash_funcs=HASH_FUNCS)
def fetch_summarization_utils():
    return ExampleDisplayer(), Postprocessor(verbose=False)


"""def load_data(dataset, task, progress_bar ):

    start = time.time()

    if task==TASKS[0]:
        (
            texts,
            summaries,
        ) = DataLoader(dataset).get_task_data(task, type_dataset)

        duration = f"{(time.time() - start):.2f}"
        st.write("Time to load data : " + duration + " seconds")
        progress_bar.progress(30)

        return texts, summaries

    if task==TASKS[1]:
        (
            summaries,
            titles,
        ) = DataLoader(dataset).get_task_data(task, type_dataset)

        duration = f"{(time.time() - start):.2f}"
        st.write("Time to load data : " + duration + " seconds")
        progress_bar.progress(30)

        return summaries, titles

    if task==TASKS[2]:
        summaries = DataLoader(dataset).get_task_data(task=task)

        duration = f"{(time.time() - start):.2f}"
        st.write("Time to load data : " + duration + " seconds")
        progress_bar.progress(30)

        return summaries"""


def title_generation():
    summarization(task=TASKS[1])

def summarization(task=TASKS[0]):
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    # Load model
    status_text.text("Load model")
    st.write("## Load Model 🔮 ")
    start = time.time()
    if task == TASKS[0]:
        model = fetch_summerization_model()
    elif task == TASKS[1]:
        model = fetch_title_model()
    else:
        raise ValueError(f"Invalid mode of summarisation. Please choose between {MODE}")
    
    duration = f"{(time.time() - start):.2f}"
    st.write(f"Time to load model  : {duration} seconds")
    progress_bar.progress(60)
    # Choose input
    dataset, text, summary = load_data(status_text, progress_bar, task)
    progress_bar.progress(60)

    # Summarize
    status_text.text("Summarizing")
    st.write("## Summarizing ... ⏳")
    if task == TASKS[0]:
        ratio = st.sidebar.slider("Ratio", 0.1, 1.0)
    else:
        ratio = None
    st.write("### Original text")
    st.write(text)
    _summarize(text, task, model, ratio, verbose = True)

    #Print Reference & original text
    exampleDisplayer, postProcessor = fetch_summarization_utils()
    if dataset in DATASETS.keys():
        st.write("### Reference summary")
        html = exampleDisplayer.display_simple(summary, jupyter=False)
        st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)
    st.write("### Original text")
    html = exampleDisplayer.display_simple(text, jupyter=False)
    st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)
    progress_bar.progress(100)
    status_text.text("Complete")
    st.button("Re-run")


def _summarize(text, task = TASKS[0], model = None, ratio = 0.1, verbose = False, translate = False):

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    start = time.time()

    if not model and task == TASKS[0]: 
        print("_"*80)
        print(TASKS[0])
        model = fetch_summerization_model()
        candidate = model.summarise(text, ratio, 0, tolerance=20)
    elif not model and task == TASKS[1]:
        print("_"*80)
        print(TASKS[1])
        model = fetch_title_model()
    
    if task == TASKS[0]: 
        candidate = model.summarise(text, ratio, 0, tolerance=20)
    elif task == TASKS[1]:
        candidate = model.generate_title(text)


    if verbose:
        duration = f"{(time.time() - start):.2f}"
        st.write("Time to summarise  : " + duration + " seconds")
    progress_bar.progress(60)

    # Post-processing
    if verbose:
        status_text.text("Post-processing")
        st.write("## Post-processing 🔎")
    exampleDisplayer, postProcessor = fetch_summarization_utils()

    start = time.time()
    candidate_post_process = postProcessor.transform(text, candidate)
    if translate :
        candidate_post_process = translate_text(candidate_post_process)
    if verbose:
        duration = f"{(time.time() - start):.2f}"
        st.write("Time to post-process  : " + duration + " seconds")
    st.write("### Generated summary")

    if translate:
        html = candidate_post_process
    else :
        html = exampleDisplayer.display_simple(candidate_post_process, jupyter=False)
    st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)

    
"""def title_generation():
    task = "title_generation"
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
    status_text.text("Choose the dataset")
    st.write(f"## Choose the dataset 📥 ")

    dataset_options = list(DATASETS.keys())+["Text input"]
    dataset = st.sidebar.selectbox("Choose a dataset",dataset_options)

    train_options = list(["Train", "Test"])
    type_dataset = st.sidebar.selectbox("Choose between train and test set",train_options)

    # load data
    if (dataset in DATASETS.keys()) and (type_dataset in train_options):
        status_text.text("Load Data")
        st.write(f"## Load {dataset} Data 📥 ")

        print("\ninside title_generation before data_load()\n")
        print('\ndataset', dataset)
        print('\n',"type_dataset", type_dataset)
        print("dataset", DATASETS[dataset],'\n')

        #summaries, titles = load_data(DATASETS[dataset], task, progress_bar)
        summaries, titles = load_data(DATASETS[dataset], task, type_dataset, progress_bar)

        print("\ninside title_generation() apres data_load\n")
        print(dataset)
        print(task)
        print(type_dataset)
        print("summaries exemple:", summaries.iloc[0],'\n')
        print("titles exemple:",titles.iloc[0],'\n')

        status_text.text("Select an article")
        st.write("## Select an article 📰 ")
        text_number = st.number_input("Article number", value=1)
        text = summaries.iloc[text_number]

    elif dataset == "Text input":
        status_text.text("Enter input")
        st.write("## Enter input ⌨️ ")
        text = st.text_input("Input text", "Gotta see both sides of the story.")

    progress_bar.progress(60)
    if not model: 
        model = fetch_summerization_model()

    #status_text.text("Summarizing")
    #st.write("## Generating ... ⏳")
    #ratio = st.sidebar.slider("Ratio", 0.1, 1.0)  

    st.write("### Original lead paragraph")
    st.write(text)
    candidate = model.summarise(text, ratio, 0, tolerance=20)
    
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
        html = exampleDisplayer.display_simple(titles.iloc[text_number], jupyter=False)
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
    st.button("Re-run")"""


"""def tags_recovering():
    task = "tags_recovering"
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    # Load model
    status_text.text("Load model")
    st.write("## Load Model 🔮 ")
    start = time.time()
    #ici
    model = fetch_tags_model()
    duration = f"{(time.time() - start):.2f}"
    st.write(f"Time to load model  : {duration} seconds")
    progress_bar.progress(25)

    # Choose input
    dataset_options = list(DATASETS.keys()) +["Text input"]
    dataset = st.sidebar.selectbox("Choose a dataset",dataset_options)

    # TODO à completer ou à laisser
    type_dataset = "train"


    if dataset in DATASETS.keys():
        status_text.text("Load Data")
        st.write(f"## Load {dataset} Data 📥 ")
        #ici
        summaries = load_data(DATASETS[dataset],task,type_dataset, progress_bar)
        status_text.text("Select an article")
        st.write("## Select an article 📰 ")
        text_number = st.number_input("Article number", value=1)
        text = summaries.iloc[text_number]

    elif dataset == "Text input":
        status_text.text("Enter input")
        st.write("## Enter input ⌨️ ")
        text = st.text_input("Input text", "Gotta see both sides of the story.")
    progress_bar.progress(50)

    # Recover tags
    status_text.text("Recovering tags")
    st.write("## Recovering tags ... ⏳")
    st.write("### Original text")
    st.write(text)
    start = time.time()
    #ici
    candidate = model.generate_tags(text)

    duration = f"{(time.time() - start):.2f}"
    st.write("Time to generate tags  : " + duration + " seconds")
    progress_bar.progress(75)

    # Post-processing
    status_text.text("Results")
    st.write("## Results 🔎")
    tags = ', '.join(candidate[0])
    cleaned_tags = postprocess_tags(tags)
    st.write(f"Tags  : {cleaned_tags}")

    progress_bar.progress(100)
    status_text.text("Complete")
    st.button("Re-run")
"""
