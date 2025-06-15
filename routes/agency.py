import pandas as pd
import plotly.express as px
import streamlit as st

from routes.utils.load_dataset import load_clean

st.subheader("Agency Analysis")

df = load_clean()

agencies = df["agency"].unique()

agency = st.selectbox("Select an agency", agencies)
agency_transactions: pd.DataFrame = pd.DataFrame(df[df["agency"] == agency])

st.subheader(agency)


tabs = st.tabs(["Analysis", "Dataset"])
with tabs[0]:
    with st.container(border=True):
        cols = st.columns(5)
        with cols[0]:
            st.metric(
                label="Total Transactions",
                value=int(agency_transactions["amount"].count()),
            )

        with cols[1]:
            st.metric(
                label="Average Amount in USD",
                value=round(float(agency_transactions["amount"].mean()), 2),
            )

        with cols[2]:
            st.metric(
                label="Median Amount in USD",
                value=round(float(agency_transactions["amount"].median()), 2),
            )

        with cols[3]:
            st.metric(
                label="Smallest Amount in USD",
                value=round(float(agency_transactions["amount"].min()), 2),
            )

        with cols[4]:
            st.metric(
                label="Largest Amount in USD",
                value=round(float(agency_transactions["amount"].max()), 2),
            )

    with st.container():
        st.subheader("Settings")
        cols = st.columns(2, vertical_alignment="bottom")
        with cols[0]:
            log_scale = st.toggle("Log Scale", value=False)
        with cols[1]:
            year = st.selectbox(
                "Select Year",
                options=[None] + sorted(agency_transactions["d_year"].unique()),
            )

        if year is not None:
            agency_transactions = pd.DataFrame(
                agency_transactions[agency_transactions["d_year"] == year]
            )

    st.divider()
    st.subheader("Transaction Amount Overview")

    transaction_per_day = (
        agency_transactions.groupby("date")["amount"].sum().reset_index()
    )
    fig = px.bar(
        transaction_per_day,
        x="date",
        y="amount",
        labels={"date": "Date", "amount": "Total Amount"},
        title="Total Amount per Date",
    )
    st.plotly_chart(fig)

    cols = st.columns(2)
    with cols[0]:
        fig = px.violin(
            agency_transactions,
            y="amount",
            box=True,
            points="all",
            labels={"amount": "Transaction Amount"},
            title="Transaction Amount Distribution",
        )
        st.plotly_chart(fig)

        fig = px.histogram(
            agency_transactions,
            nbins=100,
            x="amount",
            log_y=log_scale,
            labels={"amount": "Transaction Amount"},
            title="Transaction Amount Distribution",
        )
        st.plotly_chart(fig)

    with cols[1]:
        agency_transactions = agency_transactions.sort_values(by="date")
        agency_transactions["cumulative_amount"] = agency_transactions[
            "amount"
        ].cumsum()

        fig = px.line(
            agency_transactions,
            x="date",
            y="cumulative_amount",
            log_y=log_scale,
            labels={"date": "Date", "cumulative_amount": "Total Spend"},
            title="Cumulative Spend Over Time",
        )
        st.plotly_chart(fig, use_container_width=True)

        show_outlier = st.toggle("Show Outliers", value=False)

        if show_outlier:
            lower_threshold = agency_transactions["amount"].quantile(0.01)
            upper_threshold = agency_transactions["amount"].quantile(0.99)

            agency_transactions["is_outlier"] = (
                agency_transactions["amount"] < lower_threshold
            ) | (agency_transactions["amount"] > upper_threshold)

            fig = px.scatter(
                agency_transactions,
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
                agency_transactions,
                x="date",
                y="amount",
                log_y=log_scale,
                title="Transactions Over Time",
                labels={"date": "Date", "amount": "Amount"},
            )
            st.plotly_chart(plot)

    st.divider()

    st.subheader("Time Overview")

    cols = st.columns(3)
    with cols[0]:
        st.bar_chart(
            agency_transactions.groupby("d_year")["amount"].sum().reset_index(),
            x="d_year",
            y="amount",
        )

        fig = px.density_heatmap(
            agency_transactions,
            x="d_year",
            y="d_weekday",
            nbinsx=25,
            nbinsy=7,
            color_continuous_scale="Viridis",
            labels={"d_year": "Year", "d_weekday": "Day of Week"},
            title="Transaction Count by Year and Weekday",
        )
        st.plotly_chart(fig, use_container_width=True)

    with cols[1]:
        st.bar_chart(
            agency_transactions.groupby("d_month")["amount"].sum().reset_index(),
            x="d_month",
            y="amount",
        )

        fig = px.density_heatmap(
            agency_transactions,
            x="d_month",
            y="d_weekday",
            nbinsx=12,
            nbinsy=7,
            color_continuous_scale="Viridis",
            labels={"d_month": "Month", "d_weekday": "Day of Week"},
            title="Transaction Count by Month and Weekday",
        )
        st.plotly_chart(fig, use_container_width=True)

    with cols[2]:
        st.bar_chart(
            agency_transactions.groupby("d_day")["amount"].sum().reset_index(),
            x="d_day",
            y="amount",
        )

        fig = px.density_heatmap(
            agency_transactions,
            x="d_day",
            y="d_weekday",
            nbinsx=31,
            nbinsy=7,
            color_continuous_scale="Viridis",
            labels={"d_day": "Day of Month", "d_weekday": "Day of Week"},
            title="Transaction Count by Day and Weekday",
        )
        st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(
        agency_transactions.groupby("d_weekday")["amount"].sum().reset_index(),
        x="d_weekday",
        y="amount",
        width=500,
        labels={"d_weekday": "Day of Week", "amount": "Total Amount"},
        title="Transaction Amount by Day of Week",
    )
    st.plotly_chart(fig, use_container_width=False)

    st.divider()

    st.subheader("Vendor Overview")

    with st.container(border=True):
        cols = st.columns(2)
        with cols[0]:
            st.metric(
                "Total Vendor Province States",
                len(agency_transactions["vendor_state_province"].unique()),
            )
        with cols[1]:
            st.metric("Total Vendors", len(agency_transactions["vendor_name"].unique()))

    plot = px.bar(
        agency_transactions.groupby("vendor_state_province")["amount"]
        .sum()
        .reset_index(),
        x="vendor_state_province",
        y="amount",
        log_y=log_scale,
        title="Vendor State Province Amount Distribution",
        labels={"vendor_state_province": "State Province", "amount": "Amount"},
    )
    st.plotly_chart(plot)

with tabs[1]:
    year = st.selectbox("Year", [None] + sorted(agency_transactions["d_year"].unique()))
    if year:
        agency_transactions = pd.DataFrame(
            agency_transactions[agency_transactions["d_year"] == year]
        )
    st.dataframe(agency_transactions, height=1000)
