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

    # Pass the Page objects registered with st.navigation; raw page paths
    # are not valid links when the app uses the navigation API. Callers may
    # also pass a single page name, which does not contain link definitions.
    if isinstance(pages, str):
        pages = ()

    for name, page, icon in pages:
        st.sidebar.page_link(page, label=name, icon=icon)

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