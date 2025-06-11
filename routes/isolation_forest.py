from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.ensemble import IsolationForest

from routes.utils.load_dataset import load_clean, load_encoded

st.subheader("Isolation Forest")

df = load_encoded()
df_clean = load_clean()

X = df.drop(["id"], axis=1)

contamination = st.number_input(
    "Contamination",
    min_value=0.000,
    max_value=1.000,
    value=0.010,
    step=0.001,
    format="%.4f",
)

preds = st.session_state.get("predictions", None)

if st.button("Start Training"):
    preds = None
    with st.spinner("Training model..."):
        model = IsolationForest(contamination=contamination, random_state=0)
        model.fit(X)
        preds = model.predict(X)
        st.session_state["predictions"] = preds

if preds is not None:
    # Combine predictions with IDs
    results = df_clean.copy()
    results["anomaly"] = preds

    # Filter anomalies
    anomalies = results[results["anomaly"] == -1]
    st.dataframe(anomalies)

    if st.button("Save"):
        anomalies.to_csv(
            f"data/anomalies/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv",
            index=False,
        )
        st.success("Anomalies saved!")

    # plot scatter amount over time
