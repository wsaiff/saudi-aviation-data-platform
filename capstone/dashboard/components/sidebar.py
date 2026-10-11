import streamlit as st
import textwrap


def render_sidebar(active_page="Overview"):
    st.sidebar.markdown(
        textwrap.dedent(
            """
            <div class="brand">
                <div class="brand-icon">✈</div>
                <div>
                    <div class="brand-name">
                        Saudi Aviation
                    </div>
                    <div class="brand-subtitle">
                        Infrastructure & Data Platform
                    </div>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    navigation_items = (
        ("Overview", "▦"),
        ("Airport explorer", "⌕"),
        ("Data coverage", "◫"),
        ("About & sources", "ⓘ"),
    )
    navigation = []
    for name, icon in navigation_items:
        active_class = " active" if name == active_page else ""
        current_page = ' aria-current="page"' if name == active_page else ""
        navigation.append(
            f"""
            <div class="sidebar-nav-item{active_class}"{current_page}>
                <span class="sidebar-nav-icon">{icon}</span>
                <span>{name}</span>
            </div>
            """
        )

    st.sidebar.markdown(
        textwrap.dedent(
            f"""
            <div class="sidebar-nav" role="navigation" aria-label="Pages">
                <div class="sidebar-nav-heading">Pages</div>
                {"".join(navigation)}
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        textwrap.dedent(
            """
            <div class="source-card">
                <div class="source-title">
                    Data Source
                </div>
                <div class="source-text">
                    OurAirports<br>
                    Fixed snapshot<br>
                    8 October 2026
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )