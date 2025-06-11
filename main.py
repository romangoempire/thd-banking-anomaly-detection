import streamlit as st


st.set_page_config(layout="wide")
st.title("Anomaly Detection")

pages = {
    "Analysis": [
        st.Page("routes/dataset.py", title="Dataset"),
        st.Page("routes/agency.py", title="Agency"),
        st.Page("routes/province_state.py", title="Province State"),
    ],
    "Training and Evaluation": [
        st.Page("routes/isolation_forest.py", title="Isolation Forest"),
        st.Page("routes/evaluation.py", title="Evaluation"),
    ],
}

pg = st.navigation(pages)
pg.run()
