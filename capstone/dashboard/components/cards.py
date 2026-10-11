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
):
    # Native Streamlit elements stay in the app's theme and avoid the isolated
    # iframe used by components.html, which does not inherit styles.py CSS.
    with st.container(border=True):
        icon_column, content_column = st.columns(
            [1, 5], vertical_alignment="center"
        )
        with icon_column:
            st.markdown(f"### {icon}")
        with content_column:
            st.markdown(f"#### {value}")
            st.caption(description)