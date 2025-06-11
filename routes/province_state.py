import pandas as pd
import plotly.express as px
import streamlit as st

from routes.utils.load_dataset import load_clean

st.subheader("Province State Analysis")

df = load_clean()


with st.container():
    st.subheader("Settings")
    log_scale = st.toggle("Log Scale")

with st.expander("All Vendor States", expanded=False):
    cols = st.columns(2)
    with cols[0]:
        sum_per_state = (
            df.groupby(["vendor_state_province"])
            .agg({"amount": "sum"})
            .reset_index()
            .sort_values(by="amount", ascending=True)
        )

        fig = px.bar(
            sum_per_state,
            x="amount",
            y="vendor_state_province",
            log_x=log_scale,
            labels={"amount": "Amount", "vendor_state_province": "Vendor State"},
            title="Amount by Vendor State",
            height=1000,
        )
        st.plotly_chart(fig)

    with cols[1]:
        # count of transactions by vendor state
        count_per_state = (
            df.groupby(["vendor_state_province"])
            .agg({"amount": "count"})
            .reset_index()
            .sort_values(by="amount", ascending=True)
        )

        fig = px.bar(
            count_per_state,
            x="amount",
            y="vendor_state_province",
            log_x=log_scale,
            labels={
                "amount": "Transaction Count",
                "vendor_state_province": "Vendor State",
            },
            title="Transaction Count by Vendor State",
            height=1000,
        )
        st.plotly_chart(fig)

st.subheader("Vendor State Analysis")
vendor_state = st.selectbox(
    "Vendor State", options=df["vendor_state_province"].unique()
)

vendor_state_transactions = pd.DataFrame(
    df[df["vendor_state_province"] == vendor_state]
)


transaction_per_day = (
    vendor_state_transactions.groupby("date")["amount"].sum().reset_index()
)
fig = px.bar(
    transaction_per_day,
    x="date",
    y="amount",
    log_y=log_scale,
    labels={"date": "Date", "amount": "Total Amount"},
    title="Total Amount per Date",
)
st.plotly_chart(fig)

with st.container(border=True):
    cols = st.columns(5)
    with cols[0]:
        st.metric(
            label="Total Transactions",
            value=int(vendor_state_transactions["amount"].count()),
        )

    with cols[1]:
        st.metric(
            label="Average Amount in USD",
            value=round(float(vendor_state_transactions["amount"].mean()), 2),
        )

    with cols[2]:
        st.metric(
            label="Median Amount in USD",
            value=round(float(vendor_state_transactions["amount"].median()), 2),
        )

    with cols[3]:
        st.metric(
            label="Smallest Amount in USD",
            value=round(float(vendor_state_transactions["amount"].min()), 2),
        )

    with cols[4]:
        st.metric(
            label="Largest Amount in USD",
            value=round(float(vendor_state_transactions["amount"].max()), 2),
        )

if vendor_state == "DC":
    st.warning("Dataset for DC is too large")
    st.stop()
cols = st.columns(2)
with cols[0]:
    fig = px.violin(
        vendor_state_transactions,
        y="amount",
        box=True,
        points="all",
        labels={"amount": "Transaction Amount"},
        title="Transaction Amount Distribution",
    )
    st.plotly_chart(fig)

    fig = px.histogram(
        vendor_state_transactions,
        nbins=100,
        x="amount",
        log_y=log_scale,
        labels={"amount": "Transaction Amount"},
        title="Transaction Amount Distribution",
    )
    st.plotly_chart(fig)

with cols[1]:
    vendor_state_transactions = vendor_state_transactions.sort_values(by="date")
    vendor_state_transactions["cumulative_amount"] = vendor_state_transactions[
        "amount"
    ].cumsum()

    fig = px.line(
        vendor_state_transactions,
        x="date",
        y="cumulative_amount",
        log_y=log_scale,
        labels={"date": "Date", "cumulative_amount": "Total Spend"},
        title="Cumulative Spend Over Time",
    )
    st.plotly_chart(fig, use_container_width=True)

    show_outlier = st.toggle("Show Outliers", value=False)

    if show_outlier:
        lower_threshold = vendor_state_transactions["amount"].quantile(0.01)
        upper_threshold = vendor_state_transactions["amount"].quantile(0.99)

        vendor_state_transactions["is_outlier"] = (
            vendor_state_transactions["amount"] < lower_threshold
        ) | (vendor_state_transactions["amount"] > upper_threshold)

        fig = px.scatter(
            vendor_state_transactions,
            x="date",
            y="amount",
            log_y=log_scale,
            color="is_outlier",
            color_discrete_map={True: "red"},
            title="Outlier Transactions Over Time (Both Directions)",
            labels={"is_outlier": "Outlier"},
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        plot = px.scatter(
            vendor_state_transactions,
            x="date",
            y="amount",
            log_y=log_scale,
            title="Transactions Over Time",
            labels={"date": "Date", "amount": "Amount"},
        )
        st.plotly_chart(plot)
