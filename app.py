import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# ------------------------------
# CONFIGURACIÓN GOOGLE SHEETS
# ------------------------------
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ec8MkeiCGsou1T-rgCJoyksyxs8OMG2QybdfLeBZqZc/edit?usp=sharing"
# Permisos
scope = ["https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"]
# Credenciales (sube tu JSON al repositorio)
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url(SHEET_URL).sheet1
# ------------------------------
# INTERFAZ STREAMLIT
# ------------------------------
st.set_page_config(page_title="📋 Registro de Equipos", page_icon="🛠️", layout="centered")
st.title("🛠️ Formulario Interactivo de Registro de Equipos")
st.markdown("Rellena los campos para registrar un equipo y generar su Número de Serie automáticamente.")
# --- Formulario ---
with st.form("registro_form"):
   st.subheader("Datos del Equipo")
   bo = st.text_input("1️⃣ Base Operativa (4 dígitos, empieza por 8)", max_chars=4)
   pdv = st.text_input("2️⃣ Punto de Venta (Bar)")
   modelo = st.selectbox("3️⃣ Modelo", ["H500","H1000","V500","V1000","H250","V250"])
   op_ano = st.radio("4️⃣ Año Fabricación", ["Indicar año (2 dígitos)", "Desconocido"])
   if op_ano == "Indicar año (2 dígitos)":
       ano = st.number_input("Año (00 - 99)", min_value=0, max_value=99, step=1)
       ano_str = f"{ano:02d}"
   else:
       ano_str = "77"
   op_ped = st.radio("5️⃣ PED", ["Indicar PED", "Desconocido"])
   if op_ped == "Indicar PED":
       ped = st.number_input("PED (0001 - 9999)", min_value=1, max_value=9999, step=1)
       ped_str = f"{ped:04d}"
   else:
       ped_str = "7777"
   num_serie = f"20{ano_str}{modelo}{ped_str}"
   submitted = st.form_submit_button("💾 Guardar Equipo")
# --- Validaciones y guardado ---
if submitted:
   if not (bo.isdigit() and len(bo) == 4 and bo.startswith("8")):
       st.error("❌ La Base Operativa debe ser un número de 4 dígitos que empiece por 8.")
   elif not pdv.strip():
       st.error("❌ Debes indicar el Punto de Venta.")
   else:
       try:
           sheet.append_row([bo, pdv, modelo, ano_str, ped_str, num_serie])
           st.success("✅ Equipo registrado correctamente en Google Sheets!")
           st.markdown("### 📄 Resumen del Equipo Registrado")
           st.write({
               "BO": bo,
               "PDV": pdv,
               "Modelo": modelo,
               "Año": ano_str,
               "PED": ped_str,
               "Número de Serie": num_serie
           })
       except Exception as e:
           st.error("❌ Error al guardar en Google Sheets. Revisa las credenciales y conexión.")
           st.exception(e)