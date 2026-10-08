"""
☁️ Observatorio de Niebla — Tejedor de Palabras Mágicas
Aplicación Streamlit ambientada en un reino fantástico.

Instalación:
    pip install streamlit wordcloud matplotlib pandas Pillow numpy

Ejecución:
    streamlit run wordcloud_app.py
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import io
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Observatorio de Niebla — Tejedor de Palabras",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS — diseño profesional / corporativo
# ─────────────────────────────────────────────
st.markdown(""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Fondo general gris muy claro */
    .stApp {
        background-color: #f4f5f7;
    }

    /* Sidebar blanco con borde sutil */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #dde1e7;
    }
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #161a1d !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
    }
    [data-testid="stSidebar"] label {
        color: #4a5568 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    [data-testid="stSidebar"] p {
        color: #6b7280 !important;
        font-size: 0.88rem !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #e5e7eb !important;
        margin: 16px 0 !important;
    }

    /* Inputs */
    textarea, input[type="text"] {
        background-color: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
        color: #111827 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
    }
    textarea:focus, input[type="text"]:focus {
        border-color: #374151 !important;
        box-shadow: 0 0 0 2px rgba(55,65,81,0.12) !important;
    }

    /* Selectbox */
    [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 6px !important;
        color: #111827 !important;
        font-size: 0.9rem !important;
    }

    /* Títulos */
    h1 {
        font-family: 'Inter', sans-serif !important;
        color: #111827 !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
    }
    h2, h3 {
        font-family: 'Inter', sans-serif !important;
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
    p, li {
        color: #374151 !important;
        font-size: 0.95rem !important;
        line-height: 1.65 !important;
    }

    /* Botón principal — antracita sólido */
    .stButton > button {
        background: #1f2937 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.3px !important;
        padding: 0.6rem 1.4rem !important;
        width: 100% !important;
        transition: background 0.2s ease, box-shadow 0.2s ease !important;
    }
    .stButton > button:hover {
        background: #111827 !important;
        box-shadow: 0 2px 12px rgba(17,24,39,0.25) !important;
    }

    /* Botón descarga — gris slate */
    [data-testid="stDownloadButton"] button {
        background: #374151 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        transition: background 0.2s !important;
    }
    [data-testid="stDownloadButton"] button:hover {
        background: #1f2937 !important;
    }

    /* Métricas */
    [data-testid="metric-container"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-top: 3px solid #374151;
        border-radius: 8px;
        padding: 18px 22px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    }
    [data-testid="metric-container"] label {
        color: #6b7280 !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 700 !important;
        font-size: 1.55rem !important;
    }

    /* Header */
    .header-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-left: 5px solid #1f2937;
        border-radius: 8px;
        padding: 28px 36px;
        margin-bottom: 24px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    }

    /* Sección card */
    .section-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 24px 28px;
        margin-bottom: 16px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }

    /* Barras de frecuencia */
    .freq-row {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 7px 14px;
        margin: 4px 0;
        background: #f9fafb;
        border: 1px solid #f3f4f6;
        border-radius: 6px;
        transition: background 0.15s;
    }
    .freq-row:hover { background: #f3f4f6; }

    .freq-bar {
        height: 8px;
        background: #374151;
        border-radius: 4px;
        display: inline-block;
        vertical-align: middle;
    }

    /* Tag de ranking */
    .rank-tag {
        background: #f3f4f6;
        border: 1px solid #e5e7eb;
        border-radius: 4px;
        padding: 1px 8px;
        font-size: 0.75rem;
        font-weight: 700;
        color: #6b7280;
        font-family: 'IBM Plex Mono', monospace;
        min-width: 36px;
        text-align: center;
    }

    /* Welcome items */
    .info-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 12px 16px;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        margin-bottom: 8px;
    }

    /* Uso cards */
    .uso-tag {
        display: inline-block;
        background: #f3f4f6;
        border: 1px solid #e5e7eb;
        border-radius: 20px;
        padding: 5px 14px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #374151;
        margin: 4px 3px;
    }

    /* Expander */
    div[data-testid="stExpander"] {
        border: 1px solid #e5e7eb !important;
        border-radius: 8px !important;
        background: #ffffff !important;
    }

    hr { border-color: #e5e7eb !important; }

    /* Nube container */
    .wc-container {
        background: #ffffff;
