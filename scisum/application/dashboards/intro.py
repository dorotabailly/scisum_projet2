from pathlib import Path

import streamlit as st

from scisum.config import LOGO_PATH, STANFORD_LOGO_PATH, MAXPLANK_LOGO_PATH
from scisum.application.utils.utils import card, get_image
from scisum.infrastructure.news_parser import MaxPlanckScraper, StanfordScraper
from scisum.application.dashboards.summarization import _summarize


def intro():
    st.sidebar.success("Select an application above.")
    # Insert logo
    image = get_image(LOGO_PATH)
    st.image(image, use_column_width=False)
    st.write("# Welcome to Scisum Streamlit App! 👋")

    st.markdown("""👈 Select an application from the dropdown on the left""")
    st.markdown("""👇 Or just explore the potential of the app with the lastest news""")


    st.markdown("""---""")
    image = get_image(MAXPLANK_LOGO_PATH)
    st.image(image, use_column_width=False)
    st.markdown("## What's the lastest news in Max Planck Institute?")
    mp_article = MaxPlanckScraper().get_last_article()
    st.write(card(mp_article["title"], mp_article["summary"], mp_article["url"]), unsafe_allow_html=True)
    if st.button('Summarize this article', key="Sum1"):
        with st.spinner('Generating...'):
            _summarize(mp_article["content"], translate=True)
    
    st.markdown("""---""")
    image = get_image(STANFORD_LOGO_PATH, basewidth=250)
    st.image(image, use_column_width=False)
    st.markdown("## ... And in Stanford?")
    st_article = StanfordScraper().get_last_article()
    st.write(card(st_article["title"], st_article["summary"], st_article["url"]), unsafe_allow_html=True)

    if st.button('Summarize this article', key="Sum2"):
        with st.spinner('Generating...'):
            _summarize(st_article["content"], translate=True)