import os
from datetime import datetime

import streamlit as st
from sklearn.ensemble import IsolationForest

from routes.utils.load_dataset import load_clean, load_encoded

st.subheader("Isolation Forest")

st.info(
    """
    The columns `agency` and `vendor_state_province where one-hot encoded, because the isolation forest can't work strings.`
    `description` and `description` where not used, because each of them has thousands of unique values.
    """
)


df = load_encoded()
df_clean = load_clean()

X = df.drop(["id"], axis=1)

contamination = st.number_input(
    "Contamination",
    min_value=0.000,
    max_value=1.000,
    value=0.001,
    step=0.001,
    format="%.4f",
)
max_samples = st.number_input(
    "Max Samples",
    min_value=1,
    max_value=1000,
    value=256,
    step=1,
)

n_estimators = st.number_input(
    "Number of Estimators",
    min_value=1,
    max_value=1000,
    value=100,
    step=1,
)

max_features = st.number_input(
    "Max Features",
    min_value=0.0,
    max_value=1.0,
    value=0.8,
    step=0.01,
)

preds = st.session_state.get("predictions", None)

if st.button("Start Training"):
    preds = None
    with st.spinner("Training model..."):
        model = IsolationForest(
            n_estimators=n_estimators,
            contamination=contamination,
            max_samples=max_samples,
            max_features=max_features,
        )
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
        os.makedirs("data/anomalies", exist_ok=True)
        anomalies.to_csv(
            f"data/anomalies/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv",
            index=False,
        )
        st.success("Anomalies saved! Go to Evaluation.")

    # plot scatter amount over time
