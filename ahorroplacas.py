import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import re

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
    "Córdoba": {"porcentaje": 50, "anios": 10},
    "Almería": {"porcentaje": 50, "anios": 3},
    "Cádiz": {"porcentaje": 50, "anios": 4},
    "Granada": {"porcentaje": 50, "anios": 1},
    "Huelva": {"porcentaje": 50, "anios": 3},
    "Jaén": {"porcentaje": 50, "anios": 3},
    "Málaga": {"porcentaje": 15, "anios": 3},
    "Sevilla": {"porcentaje": 50, "anios": 3}
}

provincia = st.selectbox("Selecciona tu provincia", list(bonificaciones_ibi.keys()))
gasto_mensual = st.number_input("¿Cuál es tu gasto mensual medio en electricidad? (€)", min_value=0.0, value=100.0, step=5.0)
ibi_anual = st.number_input("¿Cuánto pagas de IBI al año? (€)", min_value=0.0, value=400.0, step=10.0)

porcentaje_boni = bonificaciones_ibi[provincia]["porcentaje"]
anios_boni = bonificaciones_ibi[provincia]["anios"]

st.markdown(
    f"""
    <div style='
        background: #f9f9f9;
        color: #000;
        border-left: 5px solid {principal_color};
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 18px;
        font-size: 1.11em;
        font-family: {font_family};
        text-align: center;
    '>
    <b>Bonificación automática en {provincia}:</b> {porcentaje_boni}% de descuento en el IBI durante {anios_boni} años (según datos municipales)
    </div>
    """,
    unsafe_allow_html=True
)

if gasto_mensual > 0 and ibi_anual > 0:
    # --- CÁLCULOS ---
    num_placas = (gasto_mensual / 1.26) * 0.6 / 0.15 * 12 / 1500
    num_placas = round(num_placas) * 2
    ahorro_anual_base = num_placas * 0.55 * 1500 * 0.15
    gasto_anual = gasto_mensual * 12
    inversion = 4000 + 200 * num_placas
    ahorro_ibi = ibi_anual * (porcentaje_boni / 100) * anios_boni

    # --- Cálculo del ahorro acumulado año a año con inflación del 2% ---
    anios = np.arange(1, 21)
    ahorro_acumulado = []
    acumulado = 0
    inflacion = 0.02  # 2% anual
    for i in range(20):
        ahorro_electricidad = ahorro_anual_base * ((1 + inflacion) ** i)
        if i < anios_boni:
            ahorro_anual_total = ahorro_electricidad + ibi_anual * (porcentaje_boni / 100)
        else:
            ahorro_anual_total = ahorro_electricidad
        acumulado += ahorro_anual_total
        ahorro_acumulado.append(acumulado)

    # Payback real según la gráfica
    payback_real = next((i + 1 for i, ahorro in enumerate(ahorro_acumulado) if ahorro >= inversion), None)
    payback_texto = f"{payback_real} años" if payback_real else "Más de 20 años"

    # --- RESULTADOS ---
    st.markdown(
        f"<div class='result-box'>"
        f"<p style='font-size:1.18em; color:{principal_color};'><b>Número estimado de placas necesarias:</b> {num_placas}</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Gasto anual antes de instalar placas:</b> {gasto_anual:,.0f} €</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Ahorro anual estimado (primer año):</b> {ahorro_anual_base:,.0f} €</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Ahorro total bonificación IBI:</b> {ahorro_ibi:,.0f} €</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Inversión estimada:</b> {inversion:,.0f} €</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Años estimados para recuperar la inversión:</b> {payback_texto}</p>"
        "</div>",
        unsafe_allow_html=True
    )

    # --- GRÁFICA ---
    inversion_linea = np.full_like(anios, inversion, dtype=float)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(anios, ahorro_acumulado, marker="o", color="#FF6839", linewidth=2, label="Ahorro acumulado (incl. IBI e inflación luz)")
    ax.plot(anios, inversion_linea, "--", color="#444", linewidth=2, label="Inversión inicial")
    if payback_real and payback_real <= 20:
        ax.axvline(payback_real, color="#FF6839", linestyle=":", linewidth=2, alpha=0.6)
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
principal_color = "#FF6839"

st.markdown(
    f"""
    <div style='
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-top: 2em;
        margin-bottom: 0.5em;
    '>
        <div style='font-weight: 700; font-size:1.35em; margin-bottom: 7px;'>
            ¿Quieres un <span style="color:{principal_color};">estudio personalizado</span> y sin compromiso?
        </div>
        <div style='font-size: 1.11em; margin-bottom: 10px; color:#222;'>
            Déjanos tu email aquí y te contactamos:
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Centrar input y botón en el mismo bloque con HTML + st.form para que no haya hueco
with st.form(key="contact_form", clear_on_submit=False):
    email = st.text_input("", value="", max_chars=60, placeholder="tucorreo@ejemplo.com")
    btn = st.form_submit_button("Quiero que me contacten", use_container_width=True)

if btn:
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        try:
            with open("emails.txt", "a") as f:
                f.write(email.strip() + "\n")
            st.success("¡Gracias! Nos pondremos en contacto contigo muy pronto.")
        except Exception:
            st.warning("Recibido. Si quieres una respuesta urgente, escríbenos a contacto@solarchain.es")
    else:
        st.error("Por favor, introduce un email válido.")
    
