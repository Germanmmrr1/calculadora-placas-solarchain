import streamlit as st

# Colores y tipografía
principal_color = "#FF6839"  # Naranja principal de solarchain.es
secundario_color = "#000000" # Negro
bg_color = "#FFFFFF"
font_family = "'Montserrat', 'Arial', sans-serif"

# Estilos personalizados
st.markdown(
    f"""
    <style>
    body {{
        background-color: {bg_color};
        color: {secundario_color};
        font-family: {font_family};
    }}
    .main, .stApp {{
        background-color: {bg_color};
        color: {secundario_color};
        font-family: {font_family};
    }}
    h1, h2, h3, .big {{
        color: {principal_color} !important;
        font-family: {font_family};
        font-weight: 700;
    }}
    .result-box {{
        background: #fff4f0;
        border-left: 5px solid {principal_color};
        border-radius: 14px;
        padding: 25px 25px 10px 25px;
        margin-bottom: 30px;
        font-family: {font_family};
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
    }}
    label, .stTextInput, .stSelectbox, .stNumberInput {{
        color: {secundario_color};
        font-family: {font_family};
    }}
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
    f"<h1 style='color:{principal_color}; font-family:{font_family}; font-size:2.6em;'>Calculadora de ahorro con placas solares</h1>",
    unsafe_allow_html=True
)
st.write(
    f"<div style='color:{secundario_color}; font-size:1.15em; margin-bottom: 1.5em;'>"
    "Introduce tu provincia y tu gasto mensual para estimar cuántas placas necesitas y cuánto podrías ahorrar cada año."
    "</div>",
    unsafe_allow_html=True
)

provincia = st.selectbox("Selecciona tu provincia", provincias)
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
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Gasto anual antes de instalar placas:</b> {gasto_anual:,.0f} €</p>"
        f"<p style='font-size:1.13em; color:{principal_color};'><b>Ahorro anual estimado:</b> {ahorro_anual:,.0f} €</p>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div class='info-box'>"
        "Este cálculo es solo una estimación. "
        "Para un estudio personalizado y mucho más preciso, contacta con "
        "<a href='https://solarchain.es' target='_blank' style='color:#FF6839;text-decoration:underline;font-weight:600;'>solarchain.es</a>."
        "</div>",
        unsafe_allow_html=True
    )