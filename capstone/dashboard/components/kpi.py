import base64
import io
from pathlib import Path
import textwrap

from PIL import Image, ImageDraw
import streamlit as st


@st.cache_data
def _load_icon_data(icon_file):
    icon_path = Path(__file__).resolve().parents[1] / "icons" / icon_file
    with Image.open(icon_path) as image:
        image = image.convert("RGBA")
        image.thumbnail((96, 96))
        ImageDraw.floodfill(image, (0, 0), (255, 255, 255, 0), thresh=40)
        optimized_image = io.BytesIO()
        image.save(optimized_image, format="WEBP", quality=85)
    return base64.b64encode(optimized_image.getvalue()).decode("ascii")


def render_kpi(
    title,
    value,
    subtitle,
    icon_image,
):
    icon_data = _load_icon_data(icon_image)
    st.markdown(
        textwrap.dedent(f"""
        <div class="kpi-card">
            <img
                class="kpi-icon"
                src="data:image/webp;base64,{icon_data}"
                alt="{title} icon"
            >
            <div class="kpi-content">
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-subtitle">{subtitle}</div>
            </div>
        </div>
        """),
        unsafe_allow_html=True,
    )