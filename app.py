import re

import requests
import streamlit as st

from apputil import *


QUOTES_URL = (
    "https://raw.githubusercontent.com/leontoddjohnson/datasets/"
    "main/text/inspiration_quotes.txt"
)


@st.cache_data
def load_quotes_corpus(url=QUOTES_URL):
    """Download the inspirational quotes and clean them into a corpus."""
    quotes_raw = requests.get(url, timeout=10).text
    quotes = quotes_raw.replace("\n", " ")
    quotes = re.split("[“”]", quotes)[1::2]
    corpus = " ".join(quotes)
    corpus = re.sub(r"\s+", " ", corpus)
    return corpus.strip()


st.write(
    '''
# Week 8: Markov Chain Text Generator

Each word in the corpus is a *state*. The next word is chosen at random
from the words that followed the current word in the corpus (the
**Markov property**).
'''
)

try:
    default_corpus = load_quotes_corpus()
except requests.RequestException:
    default_corpus = "Astrid is very kind, is she not?"

corpus = st.text_area("Corpus", value=default_corpus, height=200)

seed_term = st.text_input("Seed term (optional)", value="")
term_count = st.number_input(
    "Number of terms",
    min_value=1,
    max_value=500,
    value=15,
    step=1,
    format="%d",
)

if st.button("Generate"):
    if not corpus.strip():
        st.warning("Please provide a corpus of text.")
    else:
        text_gen = MarkovText(corpus)
        try:
            text = text_gen.generate(
                seed_term=seed_term.strip() or None,
                term_count=int(term_count),
            )
            st.write(text)
        except ValueError as err:
            st.error(str(err))
