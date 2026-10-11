import streamlit as st

def render_header(
    title,
    subtitle,
    snapshot_date="8 October 2026",
):

    st.html(
        f"""
        <div class="page-header">
            <div>
                <div class="page-title">{title}</div>
                <div class="page-subtitle">{subtitle}</div>
            </div>
            <div class="snapshot-badge">
                <div class="snapshot-icon">▣</div>
                <div>
                    <span class="snapshot-label">Data snapshot</span>
                    <span class="snapshot-date">{snapshot_date}</span>
                </div>
            </div>
        </div>
        """
    )