import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
# --- CONFIGURACIÓN ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ec8MkeiCGsou1T-rgCJoyksyxs8OMG2QybdfLeBZqZc/edit?usp=sharing"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
# --- AUTENTICACIÓN CON GOOGLE SHEETS ---
service_account_info = json.loads(st.secrets["gcp_service_account"]["json"])
creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open_by_url(SHEET_URL).sheet1
st.title("📋 Formulario de Identificación de Tanques")
# --- FORMULARIO ---
with st.form("registro_form"):
   bo = st.text_input("1. Base operativa (Almacén, empieza por 8, 4 dígitos)")
   pdv = st.text_input("2. Punto de venta (Bar al que pertenece)")
   modelo = st.selectbox("3. Modelo", ["H500", "H1000", "V500", "V1000", "H250", "V250"])
   anio_input = st.text_input("4. Año de fabricación (2 dígitos, si desconocido poner 77)")
   ped_input = st.text_input("5. PED (4 dígitos, si desconocido poner 7777)")
   submitted = st.form_submit_button("Guardar")
   if submitted:
       # Validaciones básicas
       if not (bo.isdigit() and len(bo) == 4 and bo.startswith("8")):
           st.error("La Base Operativa debe tener 4 dígitos y empezar por 8.")
       elif not anio_input.isdigit() or len(anio_input) != 2:
           st.error("El Año debe ser numérico de 2 dígitos.")
       elif not ped_input.isdigit() or len(ped_input) != 4:
           st.error("El PED debe ser numérico de 4 dígitos.")
       else:
           # Valores por defecto
           anio = anio_input if anio_input else "77"
           ped = ped_input if ped_input else "7777"
           # Número de serie
           numero_serie = f"20{anio}{modelo}{ped}"
           # Guardar en Google Sheet
           sheet.append_row([bo, pdv, modelo, anio, ped, numero_serie])
           st.success(f"✅ Registro guardado con Número de Serie: {numero_serie}")
# --- MOSTRAR DATOS ---
st.subheader("📊 Datos registrados")
data = sheet.get_all_values()
if data:
   st.table(data)
else:
   st.info("Aún no hay registros.")
