import streamlit as st


st.set_page_config(layout="wide")
st.title("Anomaly Detection")

pages = {
    "Pages": [
        st.Page("routes/dataset.py", title="Dataset"),
        st.Page("routes/agency.py", title="Agency"),
        st.Page("routes/province_state.py", title="Province State"),
    ]
}

pg = st.navigation(pages)
pg.run()
