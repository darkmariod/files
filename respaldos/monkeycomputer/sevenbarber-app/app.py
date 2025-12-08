import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta
from gc_service import GoogleService
import base64, os

# --------------------------------------------
# CONFIGURACIÓN GOOGLE CALENDAR
# --------------------------------------------
CALENDAR_ID = "b77c487c4370c521a73e8d4eff10e17167349e7afe7d49c8a5309c0ccd7863e2@group.calendar.google.com"
gc = GoogleService()   # carga automática desde GOOGLE_CREDENTIALS_JSON

# --------------------------------------------
# BASE64 PARA IMÁGENES
# --------------------------------------------
def img_to_b64(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

# --------------------------------------------
# CARGAR CSS
# --------------------------------------------
def load_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Seven Barber Club", page_icon="✂️", layout="centered")
load_css("css/style.css")

# --------------------------------------------
# HEADER
# --------------------------------------------
st.image("assets/banner.png")
st.title("Seven Barber Club")
st.text("📍 Av. Unidad Nacional entre Juan Montalvo y Carabobo")

# --------------------------------------------
# MENÚ
# --------------------------------------------
selected = option_menu(
    menu_title=None,
    options=["Reservar", "Portafolio", "Aprendiz", "Detalles", "Reseñas"],
    icons=["calendar-check", "scissors", "person-workspace", "pin", "chat-dots"],
    orientation="horizontal",
)

# ============================================================
# 🗓️ RESERVAS
# ============================================================
if selected == "Reservar":

    st.subheader("✂️ Reserva tu cita (pago obligatorio)")

    col1, col2 = st.columns(2)

    nombre = col1.text_input("Tu Nombre *")
    whatsapp = col2.text_input("Tu WhatsApp * (Ej: 0987654321)")
    email = col1.text_input("Tu Email (opcional)")
    fecha = col2.date_input("Fecha *")

    hora = col2.selectbox("Hora *", [
        "09:00","10:00","11:00","12:00",
        "14:00","15:00","16:00","17:00",
        "18:00","19:00","20:00"
    ])

    servicios = {
        "Perfil de cejas": 1,
        "Afeitado / Barba": 3,
        "Corte Clásico máquina": 5,
        "Corte Clásico tijera": 5,
        "Freestyle": 7,
        "Semi Ondulado (ondas)": 20,
        "VIP": 8,
        "Aprendiz (Mario)": 2
    }

    servicio = col1.selectbox("Servicio *", [""] + list(servicios.keys()))
    nota = col1.text_area("Nota (opcional)")

    barbero = col2.selectbox("Barbero *", ["", "💈 Josué", "💈 Ariel", "🧪 Aprendiz"])

    if "mostrar_qr" not in st.session_state:
        st.session_state["mostrar_qr"] = False
    if "pago_ok" not in st.session_state:
        st.session_state["pago_ok"] = False

    # Botón reservar
    if st.button("Reservar"):
        if not nombre or not whatsapp or not fecha or servicio == "" or barbero == "":
            st.warning("⚠ Debes llenar todos los campos obligatorios.")
        else:
            if barbero == "🧪 Aprendiz":
                st.session_state["pago_ok"] = True
            else:
                st.session_state["mostrar_qr"] = True

    # Mostrar QR
    if st.session_state["mostrar_qr"] and not st.session_state["pago_ok"]:

        precio = servicios[servicio]

        st.markdown(f"""
        ### 🏦 Confirmar pago
        <div class="qr-box">
            <h4>💰 Total a pagar: {precio}.00 USD</h4>
            <p>Escanea este QR para pagar y confirmar tu cita.<br>
            Presenta tu comprobante al llegar.</p>
        </div>
        """, unsafe_allow_html=True)

        st.image("assets/qr_pago.png", width=260)

        if st.button("✔ Ya pagué"):
            st.session_state["pago_ok"] = True

    # Crear evento
    if st.session_state["pago_ok"]:
        try:
            start = datetime.combine(fecha, datetime.strptime(hora, "%H:%M").time())
            end = start + timedelta(hours=1)

            descripcion = (
                f"Cliente: {nombre}\n"
                f"WhatsApp: {whatsapp}\n"
                f"Email: {email}\n"
                f"Servicio: {servicio}\n"
                f"Barbero: {barbero}\n"
                f"Nota: {nota}\n"
                f"Pago: {'✔ PAGADO' if barbero != '🧪 Aprendiz' else 'No aplica'}"
            )

            gc.crear_evento(
                calendar_id=CALENDAR_ID,
                resumen=f"Reserva {servicio} - {nombre}",
                descripcion=descripcion,
                inicio=start,
                fin=end
            )

            st.success("✅ Reserva creada con éxito. ¡Gracias!")
            st.balloons()

            st.session_state["mostrar_qr"] = False
            st.session_state["pago_ok"] = False

        except Exception as e:
            st.error(f"❌ Error creando evento: {e}")

# ============================================================
# PORTAFOLIO
# ============================================================
if selected == "Portafolio":
    st.subheader("📸 Portafolio — Trabajos reales")

    perfil_josue = img_to_b64("assets/josue-perfil.jpg")
    perfil_ariel = img_to_b64("assets/ariel-perfil.jpg")

    st.markdown(f"""
    <div class="perfil-barbero">
        <img class="perfil-avatar" src="data:image/jpeg;base64,{perfil_josue}">
        <h3>👑 Josué</h3>
        <p>Estilo moderno y precisión profesional.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for c, img in zip(cols, [
        "assets/corte-1.jpg",
        "assets/corte-2.jpg",
        "assets/corte-3.jpg"
    ]):
        c.image(img, use_container_width=True)

    st.write("---")

    st.markdown(f"""
    <div class="perfil-barbero">
        <img class="perfil-avatar" src="data:image/jpeg;base64,{perfil_ariel}">
        <h3>💈 Ariel</h3>
        <p>Detalles limpios y acabados profesionales.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for c, img in zip(cols, [
        "assets/corte-4.jpg",
        "assets/corte-5.jpg",
        "assets/corte-6.jpg"
    ]):
        c.image(img, use_container_width=True)

# ============================================================
# APRENDIZ
# ============================================================
if selected == "Aprendiz":
    st.subheader("💈 Aprendiz — Mario")
    st.markdown("""
    ✂️ <b>Corte profesional en práctica.</b><br><br>
    💸 <b>Precio:</b> 2 USD — NO requiere pago adelantado.<br>
    ⏰ <b>Horario:</b> 16:00 a 20:00.
    """, unsafe_allow_html=True)

# ============================================================
# DETALLES
# ============================================================
if selected == "Detalles":
    st.subheader("📍 Ubicación y Horarios")
    st.image("assets/map.jpg", use_container_width=True)
    st.markdown("""
    📌 Dirección: Av. Unidad Nacional — Riobamba  
    🕒 Horario: 09:00 - 21:00 todos los días
    """)

# ============================================================
# RESEÑAS
# ============================================================
if selected == "Reseñas":
    st.subheader("💬 Opiniones reales")
    st.image("assets/review-1.png")
    st.image("assets/review-2.png")

    st.markdown("### ⭐ Déjanos tu reseña")
    st.markdown("""
    <a href="https://g.page/r/CWV9JygXfEa_EBM/review" target="_blank">
        <button class="review-btn">📢 Dejar Reseña</button>
    </a>
    """, unsafe_allow_html=True)
