import streamlit as st
import pandas as pd


@st.cache_data
def load_original() -> pd.DataFrame:
    return pd.read_csv("./data/original.csv")


@st.cache_data
def load_clean() -> pd.DataFrame:
    df = pd.read_csv("./data/clean.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["modify_date"] = pd.to_datetime(df["modify_date"])
    return df


@st.cache_data
def load_encoded() -> pd.DataFrame:
    df = pd.read_csv("./data/encoded.csv")
    df.drop(columns=["date", "modify_date", "vendor_name", "description"], inplace=True)

    return df
