import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import re
import smtplib
from email.mime.text import MIMEText

st.set_page_config(
    page_title="Calculadora Placas Solares ☀️",
    page_icon="logo_browser.png"
)

# --- ESTILOS ---
principal_color = "#FF6839"
secundario_color = "#000000"
bg_color = "#FFFFFF"
font_family = "'Montserrat', 'Arial', sans-serif"

def send_notification_email(nombre,user_email, provincia, gasto_mensual, ibi_anual, num_placas, inversion, ahorro_anual_base, payback_texto):
    sender_email = "gmunozraya@gmail.com"
    sender_password = "eump xkih qqqm phhx"
    recipient_email = "bmunoz@solarchain.es"

    subject = "Nuevo lead recibido desde la calculadora SolarChain"
    body = f"""
    Nuevo lead recibido:

    Nombre: {nombre}
    Email: {user_email}
    Provincia: {provincia}
    Gasto mensual en electricidad: {gasto_mensual} €
    IBI anual: {ibi_anual} €
    Número estimado de placas: {num_placas}
    Inversión estimada: {inversion} €
    Ahorro anual estimado (primer año): {ahorro_anual_base} €
    Payback estimado: {payback_texto}
    """

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return True
    except Exception as e:
        print("Error sending notification:", e)
        return False


st.markdown("""
    <style>
    /* Super-specific targeting for all Streamlit buttons, including in forms */
    button[kind="primary"], div.stButton > button, div.stForm > form button {
        color: #FF6839 !important;
        border: 2px solid #FF6839 !important;
        background: #fff !important;
        font-weight: 700 !important;
        border-radius: 12px !important;
        padding: 0.5em 2.5em !important;
        font-size: 1.13em !important;
        box-shadow: none !important;
        text-shadow: none !important;
        transition: 0.1s !important;
        outline: none !important;
    }
    button[kind="primary"]:hover, div.stButton > button:hover, div.stForm > form button:hover {
        background: #FF6839 !important;
        color: #fff !important;
        border: 2px solid #FF6839 !important;
    }
    </style>
""", unsafe_allow_html=True)

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
    num_placas = ((gasto_mensual / 1.26) * 0.6 / 0.15 * 12 / 1500)*3
    num_placas = round(num_placas)
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
        f"<p style='font-size:1.18em; color:{principal_color};'><b>Número de placas necesarias:</b> {num_placas}</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Ahorro anual (1er año):</b> {ahorro_anual_base:,.0f} €</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Bonificación IBI total:</b> {ahorro_ibi:,.0f} €</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Inversión estimada:</b> {inversion:,.0f} €</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Retorno de inversión:</b> {payback_texto}</p>"
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

# Centered header and description
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
            Déjanos tu nombre y tu email y te contactamos:
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Centered name and email input, and button
cols = st.columns([1,2,1])
with cols[1]:
    nombre = st.text_input("Nombre", value="", max_chars=60, placeholder="Tu nombre")
    email = st.text_input("Email", value="", max_chars=60, placeholder="tucorreo@ejemplo.com")
    btn = st.button("Quiero que me contacten", use_container_width=True)

# Custom success/error message, centered and black
if btn:
    if not nombre.strip():
        st.markdown(
            "<div style='background:#ffeaea; border-left:5px solid #FF6839; color:#111; padding:16px 18px; border-radius:10px; font-size:1.1em; margin-top:14px; text-align:center;'>"
            "Por favor, introduce tu nombre."
            "</div>",
            unsafe_allow_html=True
        )
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.markdown(
            "<div style='background:#ffeaea; border-left:5px solid #FF6839; color:#111; padding:16px 18px; border-radius:10px; font-size:1.1em; margin-top:14px; text-align:center;'>"
            "Por favor, introduce un email válido."
            "</div>",
            unsafe_allow_html=True
        )
    else:
        try:
            with open("emails.txt", "a") as f:
                f.write(f"{nombre.strip()} <{email.strip()}>\n")
            send_notification_email(
                nombre, email, provincia, gasto_mensual, ibi_anual,
                num_placas, inversion, ahorro_anual_base, payback_texto
            )
            st.markdown(
                "<div style='background:#e8ffe8; border-left:5px solid #00a651; color:#111; padding:16px 18px; border-radius:10px; font-size:1.1em; margin-top:14px; text-align:center;'>"
                "¡Gracias! Nos pondremos en contacto contigo muy pronto."
                "</div>",
                unsafe_allow_html=True
            )
        except Exception:
            st.markdown(
                "<div style='background:#fffbe8; border-left:5px solid #FF6839; color:#111; padding:16px 18px; border-radius:10px; font-size:1.1em; margin-top:14px; text-align:center;'>"
                "Recibido. Si quieres una respuesta urgente, escríbenos a <b>info@solarchain.es</b>"
                "</div>",
                unsafe_allow_html=True
            )
