import pandas as pd

AIRPORTS_URL = (
    "https://davidmegginson.github.io/ourairports-data/airports.csv"
)


def load_airports():
    return pd.read_csv(AIRPORTS_URL)