import streamlit as st


COLORS = {
    "background": "#071827",
    "sidebar": "#061525",
    "card": "#0D2940",
    "card_hover": "#12344D",
    "border": "#1B4058",

    "text": "#F5F7FA",
    "muted": "#9BAEC0",

    "blue": "#20A8E0",
    "cyan": "#27C4D9",
    "green": "#21C79A",
    "purple": "#8B6FF5",
    "orange": "#F59E0B",
    "pink": "#E85D9E",
}


def inject_css():
    st.markdown(
        f"""
        <style>

        /* =========================
           Global
        ========================= */

        .stApp {{
            background: {COLORS["background"]};
            color: {COLORS["text"]};
        }}

        header[data-testid="stHeader"] {{
            background: {COLORS["background"]};
        }}

        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 100%;
        }}

        h1, h2, h3, p {{
            font-family: Inter, Arial, sans-serif;
        }}


        /* =========================
           Sidebar
        ========================= */

        section[data-testid="stSidebar"] {{
            background: {COLORS["sidebar"]};
            border-right: 1px solid {COLORS["border"]};
        }}

        section[data-testid="stSidebar"] > div {{
            padding-top: 1.5rem;
        }}

        section[data-testid="stSidebar"] .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}


        /* =========================
           Page Header
        ========================= */
        .page-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 2rem;
            margin-bottom: 1.5rem;
        }}

        .page-title {{
            color: {COLORS["text"]};
            font-size: 2rem;
            font-weight: 750;
            line-height: 1.15;
            margin: 0;
        }}

        .page-subtitle {{
            color: {COLORS["muted"]};
            font-size: 0.92rem;
            margin-top: 0.45rem;
            line-height: 1.5;
        }}

        .snapshot-badge {{
            display: flex;
            align-items: center;
            gap: 0.7rem;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 12px;
            padding: 0.65rem 0.9rem;
            min-width: 150px;
        }}

        .snapshot-icon {{
            font-size: 1.25rem;
        }}

        .snapshot-label {{
            display: block;
            color: {COLORS["muted"]};
            font-size: 0.68rem;
        }}

        .snapshot-date {{
            display: block;
            color: {COLORS["text"]};
            font-size: 0.78rem;
            font-weight: 600;
            margin-top: 0.15rem;
        }}


        /* =========================
           KPI Cards
        ========================= */

        .kpi-card {{
            background: {COLORS["card"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 12px;
            padding: 1rem;
            min-height: 105px;
            box-sizing: border-box;
        }}

        .kpi-icon {{
            width: 38px;
            height: 38px;
            border-radius: 9px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            margin-bottom: 0.65rem;
        }}

        .kpi-title {{
            color: {COLORS["muted"]};
            font-size: 0.72rem;
            font-weight: 500;
            margin-bottom: 0.15rem;
        }}

        .kpi-value {{
            color: {COLORS["text"]};
            font-size: 1.45rem;
            font-weight: 750;
            line-height: 1.1;
        }}

        .kpi-subtitle {{
            color: {COLORS["muted"]};
            font-size: 0.65rem;
            margin-top: 0.2rem;
        }}


        /* =========================
           Content Cards
        ========================= */

        .content-card {{
            background: {COLORS["card"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 12px;
            padding: 1rem;
            box-sizing: border-box;
        }}

        .card-title {{
            color: {COLORS["text"]};
            font-size: 0.88rem;
            font-weight: 650;
            margin-bottom: 0.7rem;
        }}

        .card-description {{
            color: {COLORS["muted"]};
            font-size: 0.72rem;
        }}


        /* =========================
           Insight Card
        ========================= */

        .insight-card {{
            background: {COLORS["card"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 12px;
            padding: 0.9rem;
            display: flex;
            gap: 0.75rem;
            align-items: flex-start;
        }}

        .insight-icon {{
            width: 38px;
            height: 38px;
            border-radius: 50%;
            background: rgba(32,168,224,0.15);
            color: {COLORS["blue"]};
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }}

        .insight-value {{
            color: {COLORS["text"]};
            font-size: 0.9rem;
            font-weight: 700;
        }}

        .insight-description {{
            color: {COLORS["muted"]};
            font-size: 0.68rem;
            line-height: 1.4;
            margin-top: 0.2rem;
        }}


        /* =========================
           Sidebar Brand
        ========================= */

        .brand {{
            display: flex;
            align-items: center;
            gap: 0.7rem;
            padding: 0.2rem 0.25rem 1.5rem 0.25rem;
        }}

        .brand-icon {{
            width: 40px;
            height: 40px;
            border-radius: 10px;
            background: rgba(32,168,224,0.12);
            display: flex;
            align-items: center;
            justify-content: center;
            color: {COLORS["cyan"]};
            font-size: 1.4rem;
        }}

        .brand-name {{
            color: {COLORS["text"]};
            font-size: 0.9rem;
            font-weight: 700;
            line-height: 1.2;
        }}

        .brand-subtitle {{
            color: {COLORS["muted"]};
            font-size: 0.62rem;
            margin-top: 0.15rem;
        }}


        /* =========================
           Sidebar Data Source
        ========================= */

        .source-card {{
            background: rgba(255,255,255,0.045);
            border: 1px solid {COLORS["border"]};
            border-radius: 11px;
            padding: 0.8rem;
            margin-top: 1.5rem;
        }}

        .source-title {{
            color: {COLORS["text"]};
            font-size: 0.68rem;
            font-weight: 650;
        }}

        .source-text {{
            color: {COLORS["muted"]};
            font-size: 0.62rem;
            line-height: 1.5;
            margin-top: 0.2rem;
        }}


        /* =========================
           Streamlit cleanup
        ========================= */

        div[data-testid="stMetric"] {{
            background: transparent;
        }}

        button[kind="secondary"] {{
            border-radius: 8px;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )