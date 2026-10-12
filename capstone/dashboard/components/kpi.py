import base64
from html import escape
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
        image.thumbnail((256, 256))
        ImageDraw.floodfill(image, (0, 0), (255, 255, 255, 0), thresh=40)
        optimized_image = io.BytesIO()
        image.save(optimized_image, format="WEBP", quality=92)
    return base64.b64encode(optimized_image.getvalue()).decode("ascii")


def render_kpi(
    title,
    value,
    subtitle,
    icon_image=None,
    centered=False,
    large_value=False,
):
    icon_html = ""
    card_class = "kpi-card kpi-card-text"
    if icon_image:
        icon_data = _load_icon_data(icon_image)
        icon_html = f"""
            <img
                class="kpi-icon"
                src="data:image/webp;base64,{icon_data}"
                alt="{escape(title)} icon"
            >
        """
        card_class = "kpi-card"

    if centered:
        card_class += " kpi-card-centered"
    if large_value:
        card_class += " kpi-card-large-value"

    st.html(
        textwrap.dedent(f"""
        <div class="{card_class}">
            {icon_html}
            <div class="kpi-content">
                <div class="kpi-title">{escape(title)}</div>
                <div class="kpi-value">{escape(str(value))}</div>
                <div class="kpi-subtitle">{escape(subtitle)}</div>
            </div>
        </div>
        """)
    )