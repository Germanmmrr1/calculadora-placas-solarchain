import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- ESTILOS ---
principal_color = "#FF6839"
secundario_color = "#000000"
bg_color = "#FFFFFF"
font_family = "'Montserrat', 'Arial', sans-serif"

st.markdown(
    f"""
    <style>
    .main, .stApp {{
        background-color: {bg_color};
        color: {secundario_color};
        font-family: {font_family};
    }}
    h1, h2, h3, .big {{
        color: {principal_color} !important;
        font-family: {font_family};
        font-weight: 700;
        text-align: center;
    }}
    .result-box {{
        background: #fff4f0;
        border-left: 5px solid {principal_color};
        border-radius: 14px;
        padding: 25px 25px 10px 25px;
        margin-bottom: 30px;
        font-family: {font_family};
        text-align: center;
    }}
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
    label, .stTextInput > label, .stSelectbox > label, .stNumberInput > label {{
        color: #000000 !important;
    }}
    .stSelectbox div[role="combobox"] {{
        color: #000000 !important;
        background-color: #fff !important;
    }}
    .stNumberInput input {{
        color: #000000 !important;
        background-color: #fff !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- LOGO CENTRADO ---
cols = st.columns([2,1,2])
with cols[1]:
    st.image("logo_solarchain.png", use_container_width=True)

# --- CABECERA ---
st.markdown(
    f"<h1 style='color:{principal_color}; font-family:{font_family}; font-size:2.6em;text-align:center;'>Calculadora de ahorro con placas solares</h1>",
    unsafe_allow_html=True
)
st.markdown(
    f"<div style='color:{secundario_color}; font-size:1.15em; margin-bottom: 1.5em; text-align:center;'>"
    "Introduce tu provincia, tu gasto mensual en electricidad y tu IBI anual para calcular el ahorro estimado y la recuperación de la inversión."
    "</div>",
    unsafe_allow_html=True
)

# --- FORMULARIO ---
bonificaciones_ibi = {
    "Almería": {"porcentaje": 50, "anios": 3},
    "Cádiz": {"porcentaje": 50, "anios": 4},
    "Córdoba": {"porcentaje": 50, "anios": 10},
    "Granada": {"porcentaje": 50, "anios": 1},
    "Huelva": {"porcentaje": 50, "anios": 3},
    "Jaén": {"porcentaje": 50, "anios": 3},  # Por defecto, confirma según tu municipio si necesitas
    "Málaga": {"porcentaje": 15, "anios": 3},
    "Sevilla": {"porcentaje": 50, "anios": 3}
}

provincia = st.selectbox("Selecciona tu provincia", list(bonificaciones_ibi.keys()))
gasto_mensual = st.number_input("¿Cuál es tu gasto mensual medio en electricidad? (€)", min_value=0.0, value=50.0, step=1.0)
ibi_anual = st.number_input("¿Cuánto pagas de IBI al año? (€)", min_value=0.0, value=300.0, step=10.0)

porcentaje_boni = bonificaciones_ibi[provincia]["porcentaje"]
anios_boni = bonificaciones_ibi[provincia]["anios"]

st.info(f"Bonificación automática en {provincia}: {porcentaje_boni}% de descuento en el IBI durante {anios_boni} años (según datos municipales)")

if gasto_mensual > 0 and ibi_anual > 0:
    # --- CÁLCULOS ---
    num_placas = (gasto_mensual / 1.26) * 0.6 / 0.15 * 12 / 1500
    num_placas = round(num_placas)
    ahorro_anual = num_placas * 0.55 * 1500 * 0.15
    gasto_anual = gasto_mensual * 12
    inversion = 4000 + 200 * num_placas
    ahorro_ibi = ibi_anual * (porcentaje_boni / 100) * anios_boni

    # Payback teniendo en cuenta el ahorro de IBI (prorrateado)
    ahorro_anual_total = ahorro_anual + (ahorro_ibi / anios_boni if anios_boni > 0 else 0)
    payback_anio = int(np.ceil(inversion / ahorro_anual_total)) if ahorro_anual_total > 0 else 0
    payback_texto = f"{payback_anio} años" if payback_anio <= 20 else "Más de 20 años"

    # --- RESULTADOS ---
    st.markdown(
        f"<div class='result-box'>"
        f"<p style='font-size:1.18em; color:{principal_color};'><b>Número estimado de placas necesarias:</b> {num_placas}</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Gasto anual antes de instalar placas:</b> {gasto_anual:,.0f} €</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Ahorro anual estimado:</b> {ahorro_anual:,.0f} €</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Ahorro total bonificación IBI:</b> {ahorro_ibi:,.0f} €</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Inversión estimada:</b> {inversion:,.0f} €</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Años estimados para recuperar la inversión:</b> {payback_texto}</p>"
        "</div>",
        unsafe_allow_html=True
    )

    # --- GRÁFICA ---
    anios = np.arange(1, 21)
    ahorro_acumulado = ahorro_anual * anios
    # Suma bonificación IBI el año correspondiente
    for i in range(anios_boni):
        if i < len(ahorro_acumulado):
            ahorro_acumulado[i] += ibi_anual * (porcentaje_boni / 100)
    ahorro_acumulado = np.cumsum(np.diff(np.insert(ahorro_acumulado, 0, 0)))

    inversion_linea = np.full_like(anios, inversion)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(anios, ahorro_acumulado, marker="o", color="#FF6839", linewidth=2, label="Ahorro acumulado (incl. IBI)")
    ax.plot(anios, inversion_linea, "--", color="#444", linewidth=2, label="Inversión inicial")
    ax.set_title("Ahorro acumulado estimado vs Inversión inicial (20 años)", fontsize=15, color=principal_color)
    ax.set_xlabel("Años", fontsize=12, color=secundario_color)
    ax.set_ylabel("€", fontsize=12, color=secundario_color)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.tick_params(colors=secundario_color)
    ax.yaxis.label.set_color(secundario_color)
    ax.xaxis.label.set_color(secundario_color)
    ax.title.set_color(principal_color)
    plt.xticks(anios)
    ax.legend()
    plt.tight_layout()

    st.pyplot(fig)

    # --- AVISO ---
    st.markdown(
        f"<div class='info-box'>"
        "Este cálculo es solo una estimación. "
        "Para un estudio personalizado y mucho más preciso, contacta con "
        "<a href='https://solarchain.es' target='_blank' style='color:#FF6839;text-decoration:underline;font-weight:600;'>solarchain.es</a>."
        "</div>",
        unsafe_allow_html=True
    )
