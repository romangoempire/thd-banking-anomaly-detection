import os
import pandas as pd

import streamlit as st
import plotly.express as px

from routes.utils.load_dataset import load_clean


@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)


df = load_clean()


st.subheader("Evaluation")

results = os.listdir("./data/anomalies")
selected_result = st.selectbox("Select a result", results)
anomaly_df = load_data(f"./data/anomalies/{selected_result}")


df = pd.merge(df, anomaly_df[["id", "anomaly"]], on="id", how="left")

df["anomaly"] = df["anomaly"].apply(lambda x: x == -1)


tabs = st.tabs(["Analysis", "Dataset"])

with tabs[0]:
    # percentage of transactions per agency
    with st.container(border=True):
        cols = st.columns(2)
        with cols[0]:
            st.metric("Total Anomalies", len(df[df["anomaly"]]))
        with cols[1]:
            st.metric(
                "Total Compromised Agencies",
                len(df[df["anomaly"]].groupby("agency").size()),
            )

    percentage_transactions_per_agency = (
        df.groupby("agency").size().reset_index(name="count")
    )
    percentage_transactions_per_agency["percentage"] = (
        percentage_transactions_per_agency["count"] / len(df) * 100
    )

    total_anomalies = len(df[df["anomaly"]])
    percentage_transactions_per_agency_with_anomalies = (
        df[df["anomaly"]].groupby("agency").size().reset_index(name="count")
    )
    percentage_transactions_per_agency_with_anomalies["percentage"] = (
        percentage_transactions_per_agency_with_anomalies["count"]
        / total_anomalies
        * 100
    )

    merged = pd.merge(
        percentage_transactions_per_agency,
        percentage_transactions_per_agency_with_anomalies,
        on="agency",
        how="left",
        suffixes=("_all", "_anomalies"),
    )

    # only show agencies with anomalies
    merged = merged[merged["count_anomalies"].notna()]

    merged = merged.sort_values(by="percentage_all", ascending=True)
    fig = px.bar(
        merged,
        x=["percentage_all", "percentage_anomalies"],
        y="agency",
        barmode="group",
        title="Percentage of Transactions per Agency",
        labels={"value": "Percentage", "variable": "Type"},
    )
    st.plotly_chart(fig)

    agencies_with_anomalies = (
        df[df["anomaly"]].groupby("agency").size().reset_index(name="count")
    )
    agencies_with_anomalies = agencies_with_anomalies.sort_values(
        by="count", ascending=False
    )

    agency = st.selectbox(
        "Select an agency", agencies_with_anomalies["agency"].unique()
    )

    agency_df = df[df["agency"] == agency]

    with st.expander("Dataset"):
        st.dataframe(agency_df[df["anomaly"]])

    fig = px.scatter(
        agency_df,
        x="date",
        y="amount",
        color="anomaly",
        color_discrete_map={True: "red", False: "blue"},
        title="Amount Over Time",
        labels={"amount": "Amount", "date": "Date"},
    )
    st.plotly_chart(fig)


with tabs[1]:
    st.dataframe(anomaly_df)
