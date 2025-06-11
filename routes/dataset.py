import streamlit as st

from routes.utils.load_dataset import load_clean, load_original

###############
# Content     #
###############

st.header("Dataset")
st.info(
    """
    #### Dataset Cleaning
    1. The columns where also renamed to be more descriptive.
    2. Whitespaces where removed from `agency` and `description`.
    3. Special characters where removed from `vendor_name`.
    3. The columns of date and modified date were split into multiple columns that contain `year`, `month`, `day`, `hour`, `minute`, `second`  and `weekday` .\n
    The reason is that the isolation forest works better with numerical data.
""",
)


tabs = st.tabs(["Original", "Cleaned"])

with tabs[0]:
    st.metric(label="Original Dataset Columns", value=load_original().shape[1])
    original_df = load_original()
    st.dataframe(original_df)
with tabs[1]:
    st.metric(label="Cleaned Dataset Columns", value=load_clean().shape[1])
    clean_df = load_clean()
    st.dataframe(clean_df)
