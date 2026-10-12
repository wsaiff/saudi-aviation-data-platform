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
            padding-top: 0.5rem;
            padding-bottom: 1rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
            max-width: 100%;
        }}

        h1, h2, h3, p {{
            font-family: Inter, Arial, sans-serif;
        }}

        label[data-testid="stWidgetLabel"] p {{
            color: {COLORS["text"]};
        }}

        div[data-testid="stSelectbox"] [data-baseweb="select"] > div {{
            background-color: {COLORS["card"]};
            border-color: {COLORS["border"]};
            border-radius: 8px;
            color: {COLORS["text"]};
        }}

        div[data-testid="stSelectbox"] [data-baseweb="select"] input,
        div[data-testid="stSelectbox"] [data-baseweb="select"] [data-testid="stMarkdownContainer"] p {{
            color: {COLORS["text"]};
        }}

        div[data-testid="stSelectbox"] [data-baseweb="select"] svg {{
            fill: {COLORS["muted"]};
        }}

        [data-baseweb="popover"],
        [data-baseweb="popover"] [data-baseweb="menu"],
        [data-baseweb="popover"] [role="listbox"] {{
            background-color: {COLORS["card"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 8px;
        }}

        [data-baseweb="popover"] [role="option"] {{
            background-color: {COLORS["card"]};
            color: {COLORS["text"]};
        }}

        [data-baseweb="popover"] [role="option"]:hover,
        [data-baseweb="popover"] [role="option"][aria-selected="true"] {{
            background-color: {COLORS["card_hover"]};
            color: {COLORS["text"]};
        }}


        /* =========================
           Sidebar
        ========================= */

        section[data-testid="stSidebar"] {{
            background: {COLORS["sidebar"]};
            border-right: 1px solid {COLORS["border"]};
        }}

        section[data-testid="stSidebar"] > div {{
            padding-top: 1rem;
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
            align-items: center;
            gap: 2rem;
            margin-bottom: 0.75rem;
            min-height: 150px;
            padding: 1rem 1.5rem;
            position: relative;
            overflow: hidden;
            border: 1px solid {COLORS["border"]};
            border-radius: 14px;
            background-image:
                linear-gradient(
                    90deg,
                    rgba(7,24,39,0.88) 0%,
                    rgba(7,24,39,0.66) 58%,
                    rgba(7,24,39,0.46) 100%
                ),
                var(--header-image);
            background-position: center, center 58%;
            background-size: cover;
            box-sizing: border-box;
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

        .header-image-credit {{
            align-self: flex-end;
            color: rgba(245,247,250,0.78);
            font-size: 0.58rem;
            margin-top: auto;
            text-decoration: none;
        }}

        .header-image-credit:hover {{
            color: {COLORS["text"]};
            text-decoration: underline;
        }}


        /* =========================
           KPI Cards
        ========================= */

        .kpi-card {{
            background: {COLORS["card"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 12px;
            display: grid;
            grid-template-columns: 38% minmax(0, 1fr);
            min-height: 126px;
            box-sizing: border-box;
            overflow: hidden;
        }}

        .kpi-card-text {{
            grid-template-columns: minmax(0, 1fr);
        }}

        .kpi-card-centered .kpi-content {{
            align-items: center;
            text-align: center;
        }}

        .kpi-card-centered .kpi-title {{
            font-size: 0.92rem;
        }}

        .kpi-card-centered .kpi-value {{
            font-size: 2rem;
        }}

        .kpi-card-centered .kpi-subtitle {{
            font-size: 0.72rem;
        }}

        .kpi-card-large-value .kpi-value {{
            font-size: 2.25rem;
        }}

        .kpi-icon {{
            display: block;
            width: 100%;
            height: 100%;
            border-radius: 11px 0 0 11px;
            object-fit: cover;
            object-position: center;
        }}

        .kpi-content {{
            background-color: {COLORS["card"]};
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 0.35rem;
            min-width: 0;
            padding: 0.75rem 0.65rem;
        }}

        .kpi-title {{
            color: {COLORS["muted"]};
            font-size: 0.78rem;
            font-weight: 600;
            line-height: 1.25;
        }}

        .kpi-value {{
            color: {COLORS["text"]};
            font-size: 1.75rem;
            font-weight: 750;
            line-height: 1;
        }}

        .kpi-subtitle {{
            color: {COLORS["muted"]};
            font-size: 0.6rem;
            line-height: 1.25;
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

        .st-key-saudi-region-map-card,
        .st-key-saudi-region-map-card [data-testid="stVerticalBlockBorderWrapper"],
        .st-key-airports-by-region-card,
        .st-key-airports-by-region-card [data-testid="stVerticalBlockBorderWrapper"],
        .st-key-airports-by-type-card,
        .st-key-airports-by-type-card [data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: {COLORS["card"]} !important;
            border-color: {COLORS["border"]};
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
            box-sizing: border-box;
            display: grid;
            grid-template-columns: 38px minmax(0, 1fr);
            gap: 0.75rem;
            align-items: center;
            padding: 0.9rem;
            width: 100%;
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

        .insight-content {{
            min-width: 0;
        }}

        .insight-value {{
            color: {COLORS["text"]};
            font-size: 1.15rem;
            font-weight: 700;
            line-height: 1.25;
        }}

        .insight-description {{
            color: {COLORS["muted"]};
            font-size: 0.78rem;
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
            padding: 0.2rem 0.25rem 1.25rem 0.25rem;
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
            font-size: 1.2rem;
            font-weight: 700;
            line-height: 1.2;
        }}

        .brand-subtitle {{
            color: {COLORS["muted"]};
            font-size: 0.68rem;
            margin-top: 0.15rem;
        }}

        .sidebar-nav {{
            border-top: 1px solid {COLORS["border"]};
            padding-top: 1rem;
        }}

        .sidebar-nav-heading {{
            color: {COLORS["muted"]};
            font-size: 0.65rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            margin: 0 0 0.55rem 0.25rem;
            text-transform: uppercase;
        }}

        .sidebar-nav-item {{
            align-items: center;
            border-radius: 8px;
            color: {COLORS["muted"]};
            display: flex;
            font-size: 0.82rem;
            gap: 0.7rem;
            margin: 0.15rem 0;
            min-height: 2.5rem;
            padding: 0 0.65rem;
        }}

        .sidebar-nav-item.active {{
            background: rgba(32,168,224,0.14);
            color: {COLORS["text"]};
            font-weight: 650;
        }}

        .sidebar-nav-icon {{
            color: {COLORS["muted"]};
            font-size: 1.05rem;
            line-height: 1;
            text-align: center;
            width: 1.1rem;
        }}

        .sidebar-nav-item.active .sidebar-nav-icon {{
            color: {COLORS["cyan"]};
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
            background-color: {COLORS["blue"]};
            border-color: {COLORS["blue"]};
            border-radius: 8px;
            color: {COLORS["text"]};
            height: 42px;
            min-height: 42px;
        }}

        button[kind="secondary"]:hover {{
            background-color: {COLORS["cyan"]};
            border-color: {COLORS["cyan"]};
            color: {COLORS["text"]};
        }}

        button[kind="secondary"]:active {{
            background-color: {COLORS["card_hover"]};
            border-color: {COLORS["cyan"]};
            color: {COLORS["text"]};
        }}

        button[kind="secondary"] p {{
            color: {COLORS["text"]};
        }}

        div[data-testid="stButton"] {{
            padding-top: 1.7rem;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )