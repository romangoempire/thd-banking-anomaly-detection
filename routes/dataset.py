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
    2. Whitespaces where removed in rows  `agency` and `description`.
    3. Special characters where removed from `vendor_name`.
    4. The columns of date and modified date were split into multiple columns that contain `year`, `month`, `day`, `hour`, `minute`, `second`  and `weekday` .\n The reason is that the isolation forest works better with numerical data. `d_` is used for the transaction date and `m_` for the last modified dates.
    5. `seconds` is the time between the transaction_date and last_modified date.
""",
)


tabs = st.tabs(["Original", "Cleaned"])

original_df = load_original()
clean_df = load_clean()

with tabs[0]:
    cols = st.columns(2)
    with cols[0]:
        st.metric(label="Original Dataset Columns", value=load_original().shape[1])
    with cols[1]:
        st.metric(label="Original Dataset Rows", value=load_original().shape[0])
    st.dataframe(original_df)

with tabs[1]:
    cols = st.columns(2)
    with cols[0]:
        st.metric(label="Cleaned Dataset Columns", value=load_clean().shape[1])
    with cols[1]:
        st.metric(label="Cleaned Dataset Rows", value=load_clean().shape[0])
    st.dataframe(clean_df)
