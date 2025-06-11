import streamlit as st
import pandas as pd


@st.cache_data
def load_original() -> pd.DataFrame:
    return pd.read_csv("./data/original.csv")


@st.cache_data
def load_clean() -> pd.DataFrame:
    df = pd.read_csv("./data/clean.csv")
    df["date"] = pd.to_datetime(df["date"])

    return df
