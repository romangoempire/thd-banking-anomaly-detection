import streamlit as st


st.set_page_config(layout="wide")
st.title("Anomaly Detection")

pages = {
    "Pages": [
        st.Page("routes/dataset.py", title="Dataset"),
        st.Page("routes/agency.py", title="Agency"),
    ]
}

pg = st.navigation(pages)
pg.run()
