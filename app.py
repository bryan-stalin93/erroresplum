import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Asistente de Códigos de Error", layout="centered")

st.title("🤖 Asistente de Códigos de Error  TAXONOMY - ICU MEDICAL")
st.write("Consulta errores usando lenguaje natural.  "
         "El sistema busca automáticamente.")

# ===== CARGA AUTOMÁTICA DEL EXCEL =====
EXCEL_PATH = "errores.xlsx"

try:
    df = pd.read_excel(EXCEL_PATH, dtype=str)
except Exception as e:
    st.error(f"No se pudo cargar el archivo Excel: {e}")
    st.stop()

# Normalizar nombres de columnas
df.columns = [c.strip().lower() for c in df.columns]

# Buscar columnas equivalentes
def find_column(posibles):
    for col in df.columns:
        for p in posibles:
            if p in col:
                return col
    return None

col_codigo = find_column(["codigo", "error"])
col_desc = find_column(["descripcion", "representa", "significa"])
col_sol = find_column(["solucion", "solución", "fix"])

if not all([col_codigo, col_desc, col_sol]):
    st.error("❌ El Excel no tiene las columnas necesarias.")
    st.write("Columnas detectadas:", list(df.columns))
    st.stop()

# Normalizar códigos (MUY IMPORTANTE)
df[col_codigo] = df[col_codigo].str.upper().str.strip()

# ===== INTERFAZ DE CONSULTA =====
consulta = st.text_input("💬 Escribe tu consulta - " 
                         "Ejemplo: ¿Qué significa el error N234?"
)

if consulta:
    # Detectar código alfanumérico completo
    match = re.search(r"\b[A-Z]*\d+[A-Z]*\b", consulta.upper())

    if not match:
        st.warning("No se detectó ningún código de error válido en la consulta.")
    else:
        codigo = match.group().strip()

        resultado = df[df[col_codigo] == codigo]

        if resultado.empty:
            st.error(f"No se encontró el error con código {codigo}.")
        else:
            fila = resultado.iloc[0]
            st.success(f"✅ Error {codigo} encontrado")

            st.markdown("### 📌 ¿Qué representa este error?")
            st.write(fila[col_desc])

            st.markdown("### 🛠️ Solución recomendada")
            st.write(fila[col_sol])

            st.markdown("### 👨‍🔧 Recomendación adicional")
            st.write(
                "Si el problema persiste, escalar el caso al Departamento de Ingeniería ICU Medical, "
                "adjuntando una foto del equipo con su número de serie, "
                "el código de error y la descripción del evento."
            )