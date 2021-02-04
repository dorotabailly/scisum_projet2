from collections import OrderedDict
from streamlit.logger import get_logger
import streamlit as st
from scisum.application.dashboards.translation import translate
from scisum.application.dashboards.summarization import summarization
from scisum.application.dashboards.summarization import title_generation
#from scisum.application.dashboards.title_generation import title_generation 
from scisum.application.dashboards.tags import tags_recovering
from scisum.application.dashboards.intro import intro


LOGGER = get_logger(__name__)

# Dictionary of dashboard
DASHBOARDS = OrderedDict(
    [
        ("—", (intro, None)),
        ("Summarization application", (summarization,""" Summerize the scientific press release of your choice """,),),
        ("Translation application", (translate,""" Translate any text from english to frensh""",),),
        ("Title generation", (title_generation,""" Generate the title for a scientific press release of your choice """,),),
        ("Tags generation", (tags_recovering, """ Generate tags for a scientific press release of your choice """,),)
      ]
)


def run():
    db_name = st.sidebar.selectbox("Choose an app", list(DASHBOARDS.keys()), 0)
    dashboard = DASHBOARDS[db_name][0]

    if db_name == "—":
        pass
    else:
        st.markdown("# %s" % db_name)
        description = DASHBOARDS[db_name][1]
        if description:
            st.write(description)
        # Clear everything from the intro page.
        for i in range(10):
            st.empty()

    dashboard()


if __name__ == "__main__":
    run()