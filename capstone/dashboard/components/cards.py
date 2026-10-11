from html import escape

import streamlit as st


def render_card_header(title, description=None):

    description_html = ""

    if description:
        description_html = f"""
        <div class="card-description">
            {description}
        </div>
        """

    st.markdown(
        f"""
        <div class="card-title">
            {title}
        </div>

        {description_html}
        """,
        unsafe_allow_html=True,
    )


def render_insight(
    value,
    description,
    icon="💡",
    height=None,
):
    card_height = f"height: {height}px;" if height is not None else ""
    st.html(
        f"""
        <div class="insight-card" style="{card_height}">
            <div class="insight-icon" aria-hidden="true">{escape(icon)}</div>
            <div class="insight-content">
                <div class="insight-value">{escape(str(value))}</div>
                <div class="insight-description">
                    {escape(description)}
                </div>
            </div>
        </div>
        """
    )