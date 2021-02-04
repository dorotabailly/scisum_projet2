import streamlit as st

import time
from scisum.config import CLASSIF_MODEL_NAME, CLASSIF_MODEL_PATH, TASKS
from scisum.domain.model import TagsRecoveringModel
from scisum.domain.postprocessing import postprocess_tags
from scisum.application.utils.utils import HASH_FUNCS, HTML_WRAPPER
from scisum.application.utils.data_loader import load_data

@st.cache(hash_funcs=HASH_FUNCS)
def fetch_tags_model():
    model = TagsRecoveringModel(model_name=CLASSIF_MODEL_NAME, model_path=CLASSIF_MODEL_PATH)
    return model


def tags_recovering():

    task = TASKS[2]
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    # Load model
    status_text.text("Load model")
    st.write("## Load Model 🔮")
    start = time.time()
    model = fetch_tags_model()
    duration = f"{(time.time() - start):.2f}"
    st.write(f"Time to load model  : {duration} seconds")
    progress_bar.progress(25)

    # Choose input
    dataset, text, target = load_data(status_text, progress_bar, task)

    # Recover tags
    status_text.text("Recovering tags")
    st.write("## Recovering tags ... ⏳")
    st.write("### Original text")
    st.write(text)
    start = time.time()
    #ici
    print("Je suis là")
    print(text)
    candidate = model.generate_tags(text)
    print("Je suis passé !")
    duration = f"{(time.time() - start):.2f}"
    st.write("Time to generate tags  : " + duration + " seconds")
    progress_bar.progress(75)

    # Post-processing
    status_text.text("Results")
    st.write("## Results 🔎")
    tags = ', '.join(candidate[0])
    processed_tags = postprocess_tags(tags)
    st.write(f"Tags  : {processed_tags}")

    progress_bar.progress(100)
    status_text.text("Complete")
    st.button("Re-run")
