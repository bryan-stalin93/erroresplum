import streamlit as st
import pandas as pd
import re

st.set_page_config(page_title="Asistente de Códigos de Error", layout="centered")

st.title("🤖 Asistente Inteligente de Códigos de Error")
st.write("Consulta errores usando lenguaje natural. El sistema busca automáticamente en el Excel.")

# ===== CARGA AUTOMÁTICA DEL EXCEL =====
EXCEL_PATH = "errores.xlsx"

try:
    df = pd.read_excel(EXCEL_PATH)
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
    st.info("Se requieren columnas equivalentes a: Código / Descripción / Solución")
    st.write("Columnas detectadas:", list(df.columns))
    st.stop()

# ===== INTERFAZ DE CONSULTA =====
consulta = st.text_input("💬 Escribe tu consulta (ej: ¿Qué significa el error 123?)")

if consulta:
    # Extraer posible código numérico
    match = re.search(r"\d+", consulta)

    if not match:
        st.warning("No se detectó ningún código de error en la consulta.")
    else:
        codigo = match.group()
        resultado = df[df[col_codigo].astype(str).str.contains(codigo, regex=False, na=False)]


        if resultado.empty:
            st.error(f"No se encontró el error con código {codigo}.")
        else:
            fila = resultado.iloc[0]
            st.success(f"✅ Error {codigo} encontrado")

            st.markdown(f"### 📌 ¿Qué representa este error?")
            st.write(fila[col_desc])

            st.markdown(f"### 🛠️ Solución recomendada")
            st.write(fila[col_sol])

            st.markdown("### 👨‍🔧 Recomendación adicional")
            st.write(
                "Si el problema persiste, escalar el caso al área de ingeniería "
                "adjuntando este código de error y la descripción del evento."
            )
