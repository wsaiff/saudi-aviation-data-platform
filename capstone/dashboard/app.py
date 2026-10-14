import sys
from pathlib import Path

CAPSTONE_DIR = Path(__file__).resolve().parents[1]
if str(CAPSTONE_DIR) not in sys.path:
    sys.path.insert(0, str(CAPSTONE_DIR))

import streamlit as st

from components.sidebar import render_sidebar
from components.styles import inject_css


st.set_page_config(
    page_title="Saudi Aviation | Data Platform",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

pages = {
    "Overview": st.Page(
        "pages/overview.py",
        title="Overview",
        icon=":material/dashboard:",
        default=True,
    ),
    "Airport explorer": st.Page(
        "pages/airport_explorer.py",
        title="Airport explorer",
        icon=":material/travel_explore:",
    ),
    "Data coverage": st.Page(
        "pages/data_coverage.py",
        title="Data coverage",
        icon=":material/analytics:",
    ),
    "About & sources": st.Page(
        "pages/about.py",
        title="About & sources",
        icon=":material/info:",
    ),
}

page = st.navigation(list(pages.values()), position="hidden")
render_sidebar(pages)
page.run()
