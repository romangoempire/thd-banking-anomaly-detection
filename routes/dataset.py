import streamlit as st

from routes.utils.load_dataset import load_clean, load_original

###############
# Content     #
###############

st.header("Dataset")

tabs = st.tabs(["Original", "Cleaned"])

with tabs[0]:
    original_df = load_original()
    st.dataframe(original_df)
with tabs[1]:
    # TODO: Add text to explain what steps where done
    clean_df = load_clean()
    st.dataframe(clean_df)
