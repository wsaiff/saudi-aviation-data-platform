import base64
from pathlib import Path

import streamlit as st


@st.cache_data
def _load_header_image():
    image_path = (
        Path(__file__).resolve().parents[1]
        / "images"
        / "King_Abdulaziz_International_Airport_-_Terminal_1.jpg"
    )
    return base64.b64encode(image_path.read_bytes()).decode("ascii")


def render_header(title, subtitle):
    image_data = _load_header_image()
    st.html(
        f"""
        <div
            class="page-header"
            style="--header-image: url('data:image/jpeg;base64,{image_data}')"
        >
            <div>
                <div class="page-title">{title}</div>
                <div class="page-subtitle">{subtitle}</div>
            </div>
            <a
                class="header-image-credit"
                href="https://commons.wikimedia.org/wiki/File:King_Abdulaziz_International_Airport_-_Terminal_1.jpg"
                target="_blank"
                rel="noopener noreferrer"
            >
                Image: Skytrax / Wikimedia Commons (CC BY-SA 4.0)
            </a>
        </div>
        """
    )