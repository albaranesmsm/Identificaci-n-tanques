import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# --------------------------
# CONFIGURACIÓN GOOGLE SHEETS
# --------------------------
scope = [
   "https://spreadsheets.google.com/feeds",
   "https://www.googleapis.com/auth/drive"
]
# Cargar credenciales
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)
# ID del Google Sheet (extraído de la URL)
SHEET_ID = "1Ec8MkeiCGsou1T-rgCJoyksyxs8OMG2QybdfLeBZqZc"
sheet = client.open_by_key(SHEET_ID).sheet1
# --------------------------
# INTERFAZ STREAMLIT
# --------------------------
st.set_page_config(page_title="Registro de Equipos", page_icon="📋", layout="centered")
st.title("📋 Registro de Equipos")
with st.form("registro_form"):
   # 1. Base Operativa
   base_operativa = st.text_input("1. Base operativa (Almacén, 4 dígitos empezando por 8)")
   # 2. Punto de venta
   punto_venta = st.text_input("2. Punto de venta (Bar)")
   # 3. Modelo
   modelo = st.selectbox("3. Modelo", ["H500", "H1000", "V500", "V1000", "H250", "V250"])
   # 4. Año Fabricación
   col1, col2 = st.columns(2)
   with col1:
       opcion_anio = st.radio("4. Año fabricación", ["Especificar", "Desconocido"])
   with col2:
       anio_fabricacion = ""
       if opcion_anio == "Especificar":
           anio_fabricacion = st.text_input("Introduce año (2 dígitos, ej: 25)")
   # 5. PED
   col3, col4 = st.columns(2)
   with col3:
       opcion_ped = st.radio("5. PED", ["Especificar", "Desconocido"])
   with col4:
       ped = ""
       if opcion_ped == "Especificar":
           ped = st.text_input("Introduce PED (máx 4 dígitos)")
   # Botón de envío
   submitted = st.form_submit_button("✅ Registrar")
# --------------------------
# VALIDACIÓN Y GUARDADO
# --------------------------
if submitted:
   errores = []
   # Validar Base Operativa
   if not (base_operativa.isdigit() and len(base_operativa) == 4 and base_operativa.startswith("8")):
       errores.append("⚠️ La Base Operativa debe ser un número de 4 dígitos que empiece por 8.")
   # Validar Año
   if opcion_anio == "Especificar":
       if not (anio_fabricacion.isdigit() and len(anio_fabricacion) == 2):
           errores.append("⚠️ El año debe tener exactamente 2 dígitos (ej: 25).")
   else:
       anio_fabricacion = "77"
   # Validar PED
   if opcion_ped == "Especificar":
       if not (ped.isdigit() and 1 <= len(ped) <= 4):
           errores.append("⚠️ El PED debe ser un número de hasta 4 dígitos.")
   else:
       ped = "7777"
   # Si hay errores
   if errores:
       for e in errores:
           st.error(e)
   else:
       # Generar Número de Serie: 20;Año;Modelo;PED (ej: 2025H10007777)
       numero_serie = f"20{anio_fabricacion}{modelo}{ped}"
       # Guardar en Google Sheets
       nueva_fila = [base_operativa, punto_venta, modelo, anio_fabricacion, ped, numero_serie]
       sheet.append_row(nueva_fila)
       st.success("✅ Registro guardado con éxito")
       st.write("**Número de Serie generado:**", numero_serie)
