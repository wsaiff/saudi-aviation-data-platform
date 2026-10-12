import streamlit as st
import textwrap


def render_sidebar(pages):
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

    st.sidebar.markdown(
    '<span style="color: #F5F7FA; font-weight: 600;">Pages</span>',
    unsafe_allow_html=True,
)
    for name, page in pages.items():
        st.sidebar.page_link(page, label=name, icon=page.icon, width="stretch")

    st.sidebar.markdown(
        textwrap.dedent(
            """
            <div class="source-card">
                <div class="source-title">
                    Data Source
                </div>
                <div class="source-text">
                    OurAirports<br>
                    Snapshot loaded<br>
                    11 October 2026
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )
