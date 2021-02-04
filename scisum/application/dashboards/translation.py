import streamlit as st

#from scisum.application.utils.data_loader import load_data
from scisum.domain.translate import translate_text
from scisum.application.utils.utils import  HTML_WRAPPER
from scisum.config import TASKS
from scisum.application.utils.data_loader import load_data




def translate():
    task = TASKS[3]
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    
    #Choose input
    dataset, text, _ = load_data(status_text, progress_bar, task=task)
     # Translate
    status_text.text("Translating")
    st.write("## Translating ... ⏳")
    st.write("### Original text")
    st.write(text)
    st.write("### Translated text")
    trsl_text = translate_text(text)
    st.write(HTML_WRAPPER.format(trsl_text), unsafe_allow_html=True)