import pandas as pd
from scisum.config import STANFORD, TEXTS, SUMMARIES, PATH

'''
def fetch_data(source=STANFORD):
    """ Util to fetch data from csv """
    df = pd.read_csv(source[PATH])
    texts = df[source[TEXTS]]
    summaries = df[source[SUMMARIES]]
    return texts, summaries
'''