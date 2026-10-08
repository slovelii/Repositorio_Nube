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
st.markdown("""
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
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 6px rgba(0,0,0,0.05);
        margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STOPWORDS
# ─────────────────────────────────────────────
STOPWORDS_ES = {
    "de","la","el","en","y","a","los","del","se","las","un","por","con","no","una","su",
    "para","es","al","lo","como","mas","pero","sus","le","ya","o","este","si","porque",
    "esta","entre","cuando","muy","sin","sobre","tambien","me","hasta","hay","donde",
    "quien","desde","nos","durante","ni","contra","ese","eso","ante","bajo","tras",
    "que","fue","son","han","ha","ser","era","estan","siendo","sido","he","has","hemos",
    "habian","tiene","tienen","hacer","puede","pueden","asi","tan","parte","todo","todos",
    "todas","cada","otro","otra","otros","otras","mismo","misma","nuestro","nuestra",
    "ellos","ellas","nosotros","les","esa","esos","esas","aquel","aquella","aquellos",
}

def obtener_stopwords(idioma):
    sw = set(STOPWORDS)
    if idioma in ("Español", "Ambos"):
        sw |= STOPWORDS_ES
    return sw


# ─────────────────────────────────────────────
# PALETAS PROFESIONALES
# ─────────────────────────────────────────────
PALETAS = {
    "Escala de grises":      ["#111827","#1f2937","#374151","#4b5563","#6b7280","#9ca3af","#d1d5db"],
    "Azul corporativo":     ["#1e3a5f","#1d4ed8","#2563eb","#3b82f6","#60a5fa","#93c5fd","#0f2942"],
    "Verde institucional":  ["#064e3b","#065f46","#047857","#059669","#10b981","#34d399","#6ee7b7"],
    "Gris azulado":         ["#0f172a","#1e293b","#334155","#475569","#64748b","#94a3b8","#cbd5e1"],
    "Terracota":            ["#7c2d12","#9a3412","#c2410c","#ea580c","#f97316","#fb923c","#fdba74"],
    "Índigo profundo":      ["#1e1b4b","#312e81","#3730a3","#4338ca","#4f46e5","#6366f1","#818cf8"],
    "Monocromático negro":  ["#000000","#111111","#222222","#444444","#666666","#888888","#aaaaaa"],
}

FORMAS = {
    "Rectángulo": None,
    "Círculo":    "circle",
}

def crear_mascara(forma, size=500):
    if forma == "circle":
        y, x = np.ogrid[:size, :size]
        cx, cy = size // 2, size // 2
        mascara = np.ones((size, size), dtype=np.uint8) * 255
        mascara[(x - cx)**2 + (y - cy)**2 <= (size // 2 - 12)**2] = 0
        return mascara
    return None


# ─────────────────────────────────────────────
# FUNCIONES CORE
# ─────────────────────────────────────────────
def limpiar_texto(texto, stopwords, min_longitud):
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+", "", texto)
    texto = re.sub(r"[^a-záéíóúüñàâèêîôùûäëïöü\s]", " ", texto, flags=re.UNICODE)
    palabras = [p for p in texto.split() if p not in stopwords and len(p) >= min_longitud]
    return " ".join(palabras)


def contar_palabras(texto_limpio):
    return pd.DataFrame(Counter(texto_limpio.split()).most_common(50),
                        columns=["Palabra", "Frecuencia"])


def generar_wordcloud(texto_limpio, paleta_nombre, max_words, fondo, forma, ancho=1000, alto=520):
    import random
    colores = PALETAS[paleta_nombre]

    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        rng = random_state or random.Random()
        return colores[rng.randint(0, len(colores) - 1)]

    mascara = crear_mascara(forma, size=min(ancho, alto))
    wc = WordCloud(
        width=ancho, height=alto, max_words=max_words,
        background_color=fondo, color_func=color_func,
        mask=mascara, collocations=False,
        min_font_size=11, max_font_size=120,
        prefer_horizontal=0.75, relative_scaling=0.5, margin=5,
    ).generate(texto_limpio)

    fig, ax = plt.subplots(figsize=(ancho / 100, alto / 100))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_facecolor(fondo)
    plt.tight_layout(pad=0)
    return fig


def fig_a_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# SIDEBAR — CONTROLES DEL HECHIZO
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔮 El Grimorio de Eldrin")
    st.divider()

    # ── Fuente ──
    st.markdown("### ORIGEN DEL INVENTO / TEXTO")
    fuente = st.radio("fuente", ["✍️ Transcribir Manuscrito", "📂 Desplegar Pergamino"],
                      label_visibility="collapsed")
    texto_input = ""

    if fuente == "✍️ Transcribir Manuscrito":
        texto_input = st.text_area(
            "Encantamiento:", height=190,
            placeholder="Escribe o susurra aquí las palabras, profesías o fragmentos de tu historia...")

        with st.expander("Revelar Crónicas Antiguas"):
            ejemplos = {
                "La Leyenda del Archidragón": """
                En las alturas de las montañas de Eldoria habita el dragón de fuego celestial.
                El dragón protege el templo antiguo de las sombras oscuras. La magia del dragón
                revela el destino de la corona perdurable y el honor del reino. La leyenda del
                dragón perdura en los cantares del pueblo, donde cada guerrero sueña con la victoria,
                la sabiduría del fuego y el poder de los antiguos guardianes de la luz.
                """,
                "Bitácora del Alquimista": """
                El elixir de la vida eterna requiere la esencia pura del cristal nocturno.
                En mi laboratorio de alquimia combino la luz de la luna con polvo de estrellas.
                La alquimia transmuta el plomo en oro noble mientras los espíritus del bosque
                observan el ritual. La sabiduría antigua de la alquimia busca la armonía entre
                el fuego, la tierra, el aire y la magia secreta del conocimiento infinito.
                """,
                "Diario de un Navegante del Éter": """
                Navegando por los mares de vapor flotante hacia el horizonte desconocido.
                El barco veloz atraviesa las nubes de plata guiado por la brújula astral.
                Los piratas del éter buscan tesoros perdidos en las islas flotantes. La aventura
                exige valor, astucia, coraje y libertad en el cielo infinito donde las tormentas
                de magia purifican el alma de los navegantes legendarios.
                """,
            }
            ejemplo_sel = st.selectbox("Elige un relato:", list(ejemplos.keys()),
                                       label_visibility="collapsed")
            if st.button("Conjurar pergamino seleccionado"):
                st.session_state["texto_ejemplo"] = ejemplos[ejemplo_sel]
                st.rerun()

        if "texto_ejemplo" in st.session_state and not texto_input:
            texto_input = st.session_state["texto_ejemplo"]

    else:
        archivo = st.file_uploader("Subir pergamino (.txt o .csv):", type=["txt", "csv"],
                                   label_visibility="collapsed")
        if archivo:
            if archivo.name.endswith(".txt"):
                texto_input = archivo.read().decode("utf-8", errors="ignore")
            elif archivo.name.endswith(".csv"):
                df_csv = pd.read_csv(archivo)
                col_txt = st.selectbox("Columna de runas/texto:", df_csv.columns.tolist())
                texto_input = " ".join(df_csv[col_txt].dropna().astype(str).tolist())
            st.success(f"Pergamino desencriptado — {len(texto_input):,} caracteres mágicos")

    st.divider()

    # ── Procesamiento ──
    st.markdown("### PURIFICACIÓN DEL TEXTO")
    idioma         = st.selectbox("Palabras de ruido (Stopwords):", ["Español", "Inglés", "Ambos", "Ninguno"])
    min_longitud   = st.slider("Longitud mínima de la runa", 2, 8, 3)
    palabras_extra = st.text_input("Bañar en olvido (Excluir):",
                                   placeholder="ej: dragón, rey, magia")

    st.divider()

    # ── Apariencia ──
    st.markdown("### ALQUIMIA VISUAL")
    paleta_sel  = st.selectbox("Esencia cromática:", list(PALETAS.keys()))
    fondo_sel   = st.radio("Cielo del Reino:", ["Blanco", "Negro"], horizontal=True)
    fondo_color = "white" if fondo_sel == "Blanco" else "black"
    forma_sel   = st.selectbox("Aura del Encantamiento:", list(FORMAS.keys()))
    max_words   = st.slider("Densidad de runas:", 20, 200, 80)

    st.divider()
    generar = st.button("CANALIZAR NIEBLA  ↗", use_container_width=True)


# ─────────────────────────────────────────────
# CONTENIDO PRINCIPAL — LA NARRATIVA
# ─────────────────────────────────────────────

# Header
st.markdown("""
<div class="header-card">
    <h1 style="margin:0; font-size:1.9rem;">🔮 Observatorio de Niebla y Palabras</h1>
    <p style="margin:6px 0 0 0; color:#6b7280 !important; font-size:0.97rem;">
        Bienvenido a la torre del Sabio Eldrin, donde los discursos, historias y hechizos cobran vida en tormentas de niebla visual.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Pantalla de bienvenida ──
if not generar or not texto_input.strip():
    col_izq, col_der = st.columns([3, 2], gap="large")

    with col_izq:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### El Arte de Cristalizar Pensamientos")
        st.markdown("""
        Cuentan las crónicas de Eldoria que las palabras pronunciadas no desaparecen: flotan en el éter hasta que un **Tejedor de Niebla** las condensa. 
        Al concentrar cualquier escrito en este altar, los vocablos con mayor carga de energía divina crecen y resplandecen, revelando el verdadero corazón de tu historia.
        """)

        for icono, titulo, desc in [
            ("✨", "Revelación de Esencias", "Descubre qué términos dominan tus leyendas, profecías o escritos."),
            ("🧹", "Purificación de Ruido", "Disuelve las palabras comunes para dejar únicamente los conceptos con alma."),
            ("🎨", "Tejido de Formas y Colores", "Elige las tonalidades del reino y la forma geométrica de tu niebla."),
            ("📜", "Captura del Ritual", "Guarda el mapa visual en alta definición o extrae el registro de frecuencias en un papiro digital."),
        ]:
            st.markdown(
                f'<div class="info-item">'
                f'<span style="font-size:1.3rem; flex-shrink:0;">{icono}</span>'
                f'<div><strong style="color:#111827;">{titulo}</strong>'
                f'<p style="margin:2px 0 0 0; color:#6b7280 !important; font-size:0.88rem;">{desc}</p></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("#### Pasos para ejecutar el ritual")
        for i, paso in enumerate([
            "Escribe un relato o sube un pergamino en el grimorio lateral.",
            "Selecciona las runas a purificar, los colores de tu orden y la densidad de la niebla.",
            "Presiona **CANALIZAR NIEBLA ↗** para iniciar el conjuro.",
            "Extrae la imagen cristalizada o descarga el papiro de frecuencias.",
        ], 1):
            st.markdown(f"**{i}.** {paso}")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### Usos del Observatorio")
        for caso in [
            "📜 Interpretación de Profecías",
            "📖 Análisis de Mitos y Leyendas",
            "🧙 Resumen de Grimorios Antiguos",
            "🏰 Mapas Conceptuales de Reinos",
            "🛡️ Cartas de Alianzas e Historias",
            "🐉 Catálogo de Monstruos y Héroes",
            "🌟 Condensación de Cantares Bardicos",
        ]:
            st.markdown(
                f'<span class="uso-tag">{caso}</span>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card" style="margin-top:16px;">', unsafe_allow_html=True)
        st.markdown("### Esencias de Color Disponibles")
        for nombre in PALETAS.keys():
            st.markdown(
                f'<div style="padding:5px 0; border-bottom:1px solid #f3f4f6;">'
                f'<span style="color:#374151; font-size:0.88rem; font-weight:500;">{nombre}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    if not texto_input.strip() and generar:
        st.warning("Escribe unas palabras o carga un pergamino en el panel izquierdo antes de invocarlas.")
    st.stop()


# ─────────────────────────────────────────────
# PROCESAMIENTO
# ─────────────────────────────────────────────
stopwords_set = obtener_stopwords(idioma) if idioma != "Ninguno" else set()
if palabras_extra.strip():
    stopwords_set |= {p.strip().lower() for p in palabras_extra.split(",") if p.strip()}

texto_limpio = limpiar_texto(texto_input, stopwords_set, min_longitud)

if not texto_limpio.strip():
    st.error("El pergamino se disolvió por completo. Reduce la longitud de la runa o ajusta la purificación de ruido.")
    st.stop()

df_freq        = contar_palabras(texto_limpio)
total_palabras = len(texto_limpio.split())
vocabulario    = len(df_freq)

# ── Métricas ──
m1, m2, m3, m4 = st.columns(4)
m1.metric("Runas invocadas",        f"{total_palabras:,}")
m2.metric("Vocabulario místico",    f"{vocabulario:,}")
m3.metric("Runa dominante",         df_freq.iloc[0]["Palabra"] if not df_freq.empty else "—")
m4.metric("Potencia de resonancia", int(df_freq.iloc[0]["Frecuencia"]) if not df_freq.empty else 0)

st.markdown("<br>", unsafe_allow_html=True)

# ── Nube ──
with st.spinner("Canalizando los vapores del éter y tejiendo la niebla..."):
    fig_wc = generar_wordcloud(
        texto_limpio, paleta_sel, max_words, fondo_color,
        FORMAS[forma_sel], ancho=1000, alto=520,
    )

st.markdown('<div class="wc-container">', unsafe_allow_html=True)
st.markdown(f"**Tejido de Niebla Cristalizado** &nbsp;·&nbsp; Esencia: *{paleta_sel}* &nbsp;·&nbsp; Cielo: *{fondo_sel}* &nbsp;·&nbsp; {max_words} runas máximas.")
st.pyplot(fig_wc, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

img_bytes = fig_a_bytes(fig_wc)
st.download_button(
    "⬇️ Guardar Cristal de Niebla (PNG)",
    data=img_bytes, file_name="niebla_de_palabras.png", mime="image/png",
    use_container_width=True,
)

st.divider()

# ── Análisis ──
col_freq, col_tabla = st.columns([3, 2], gap="large")

with col_freq:
    st.markdown("### Jerarquía de Runas — Top 20")
    top20    = df_freq.head(20)
    max_freq = top20["Frecuencia"].max()

    for rank, (_, row) in enumerate(top20.iterrows(), 1):
        p = row["Palabra"]
        f = int(row["Frecuencia"])
        barra_w = max(12, int((f / max_freq) * 210))
        st.markdown(
            f'<div class="freq-row">'
            f'<span class="rank-tag">#{rank:02d}</span>'
            f'<span style="font-weight:600; color:#111827; min-width:130px; font-size:0.93rem;">{p}</span>'
            f'<div class="freq-bar" style="width:{barra_w}px; opacity:{0.5 + 0.5*(f/max_freq):.2f};"></div>'
            f'<span style="font-family:\'IBM Plex Mono\',monospace; font-size:0.88rem; '
            f'color:#374151; min-width:28px; text-align:right; font-weight:500;">{f}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

with col_tabla:
    st.markdown("### Registro Alquímico")
    st.dataframe(
        df_freq.head(30).style
               .background_gradient(subset=["Frecuencia"], cmap="Greys")
               .format({"Frecuencia": "{:,}"}),
        use_container_width=True, height=500,
    )
    csv_bytes = df_freq.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Exportar Registro de Frecuencias (.csv)",
        data=csv_bytes, file_name="frecuencias_misticas.csv", mime="text/csv",
        use_container_width=True,
    )

st.divider()

with st.expander("Inspeccionar esencia del texto purificado (tras el filtro de ruido)"):
    preview = texto_limpio[:2500] + ("..." if len(texto_limpio) > 2500 else "")
    st.markdown(
        f'<p style="font-family:IBM Plex Mono,monospace; font-size:0.85rem; '
        f'color:#374151; background:#f9fafb; padding:16px; border-radius:6px; '
        f'border:1px solid #e5e7eb; line-height:1.8;">{preview}</p>',
        unsafe_allow_html=True,
    )

plt.close("all")
