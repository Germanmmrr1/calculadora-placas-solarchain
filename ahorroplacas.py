import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Muestra el logo centrado arriba
cols = st.columns([1,2,1])
with cols[1]:
    st.image("logo_solarchain.png", width=180)

# Colores y tipografía
principal_color = "#FF6839"  # Naranja principal
secundario_color = "#000000" # Negro
bg_color = "#FFFFFF"
font_family = "'Montserrat', 'Arial', sans-serif"

# Estilos personalizados para centrar y colores
st.markdown(
    f"""
    <style>
    /* Fondo y textos generales */
    .main, .stApp {{
        background-color: {bg_color};
        color: {secundario_color};
        font-family: {font_family};
    }}
    /* Títulos */
    h1, h2, h3, .big {{
        color: {principal_color} !important;
        font-family: {font_family};
        font-weight: 700;
        text-align: center;
    }}
    /* Caja de resultados */
    .result-box {{
        background: #fff4f0;
        border-left: 5px solid {principal_color};
        border-radius: 14px;
        padding: 25px 25px 10px 25px;
        margin-bottom: 30px;
        font-family: {font_family};
        text-align: center;
    }}
    /* Info-box */
    .info-box {{
        background: #f6f6f6;
        color: {principal_color};
        border-radius: 12px;
        padding: 18px 20px;
        margin: 30px 0;
        font-size: 1.08em;
        border-left: 4px solid {principal_color};
        font-family: {font_family};
        text-align: center;
    }}
    /* Centrado de textos */
    .centered {{
        text-align: center;
    }}
    /* Forzar color negro en labels e inputs */
    label, .stTextInput > label, .stSelectbox > label, .stNumberInput > label {{
        color: #000000 !important;
    }}
    /* Menú desplegable selectbox */
    .stSelectbox div[role="combobox"] {{
        color: #000000 !important;
        background-color: #fff !important;
    }}
    /* Valor del input numérico */
    .stNumberInput input {{
        color: #000000 !important;
        background-color: #fff !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    /* Oculta la barra superior de Streamlit Cloud (Share, GitHub, etc.) */
    header[data-testid="stHeader"] {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)


provincias = [
    "Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz",
    "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ciudad Real",
    "Córdoba", "Cuenca", "Girona", "Granada", "Guadalajara", "Guipúzcoa", "Huelva",
    "Huesca", "Illes Balears", "Jaén", "La Coruña", "La Rioja", "Las Palmas", "León",
    "Lleida", "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Ourense", "Palencia",
    "Pontevedra", "Salamanca", "Santa Cruz de Tenerife", "Segovia", "Sevilla",
    "Soria", "Tarragona", "Teruel", "Toledo", "Valencia", "Valladolid", "Vizcaya",
    "Zamora", "Zaragoza"
]

st.markdown(
    f"<h1 style='color:{principal_color}; font-family:{font_family}; font-size:2.6em;text-align:center;'>Calculadora de ahorro con placas solares</h1>",
    unsafe_allow_html=True
)
st.markdown(
    f"<div style='color:{secundario_color}; font-size:1.15em; margin-bottom: 1.5em; text-align:center;'>"
    "Introduce tu provincia y tu gasto mensual para estimar cuántas placas necesitas y cuánto podrías ahorrar cada año."
    "</div>",
    unsafe_allow_html=True
)

col1, col2 = st.columns([1, 1], gap="large")
with col1:
    provincia = st.selectbox("Selecciona tu provincia", provincias)
with col2:
    gasto_mensual = st.number_input(
        "¿Cuál es tu gasto mensual medio en electricidad? (€)",
        min_value=0.0,
        value=100.0,
        step=1.0
    )

if gasto_mensual > 0:
    num_placas = (gasto_mensual / 1.26) * 0.6 / 0.15 * 12 / 1500
    num_placas = round(num_placas)
    ahorro_anual = num_placas * 0.55 * 1500 * 0.15
    gasto_anual = gasto_mensual * 12

    st.markdown(
        f"<div class='result-box'>"
        f"<p style='font-size:1.18em; color:{principal_color};'><b>Número estimado de placas necesarias:</b> {num_placas}</p>"
        f"<p style='font-size:1.13em; color:{secundario_color};'><b>Gasto anual antes de instalar placas:</b> {gasto_anual:,.0f} €</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Ahorro anual estimado:</b> {ahorro_anual:,.0f} €</p>"
        "</div>",
        unsafe_allow_html=True
    )

    # Gráfica de ahorro acumulado a 20 años
    anios = np.arange(1, 21)
    ahorro_acumulado = ahorro_anual * anios

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(anios, ahorro_acumulado, marker="o", color="#FF6839", linewidth=2)
    ax.set_title("Ahorro acumulado estimado en 20 años", fontsize=16, color=principal_color)
    ax.set_xlabel("Años", fontsize=12, color=secundario_color)
    ax.set_ylabel("Ahorro acumulado (€)", fontsize=12, color=secundario_color)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.tick_params(colors=secundario_color)
    ax.yaxis.label.set_color(secundario_color)
    ax.xaxis.label.set_color(secundario_color)
    ax.title.set_color(principal_color)
    plt.xticks(anios)
    plt.tight_layout()

    st.pyplot(fig)

    st.markdown(
        f"<div class='info-box'>"
        "Este cálculo es solo una estimación. "
        "Para un estudio personalizado y mucho más preciso, contacta con "
        "<a href='https://solarchain.es' target='_blank' style='color:#FF6839;text-decoration:underline;font-weight:600;'>solarchain.es</a>."
        "</div>",
        unsafe_allow_html=True
    )
