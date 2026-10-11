import streamlit as st
import textwrap

def render_kpi(
    title,
    value,
    subtitle,
    icon,
    accent,
):

    st.markdown(
        textwrap.dedent(f"""
        <div class="kpi-card">
            <div
                class="kpi-icon"
                style="background: {accent}20; color: {accent};"
            >
                {icon}
            </div>
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-subtitle">{subtitle}</div>
        </div>
        """),
        unsafe_allow_html=True,
    )