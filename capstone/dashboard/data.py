import pandas as pd
import streamlit as st

#using dataset temporarily
AIRPORTS_URL = (
    "https://davidmegginson.github.io/ourairports-data/airports.csv"
)


@st.cache_data
def load_airports():
    airports = pd.read_csv(AIRPORTS_URL)
    return airports.loc[airports["iso_country"] == "SA"].copy()


def count_regions(saudi_airports):
    return (
        saudi_airports["iso_region"]
        .dropna()
        .nunique()
    )