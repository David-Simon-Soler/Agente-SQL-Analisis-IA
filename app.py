import streamlit as st
import sqlite3
import os
import pandas as pd
import plotly.express as px
from groq import Groq
from dotenv import load_dotenv
from src.limpieza import limpiar_datos

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

API_KEY = os.getenv("GROQ_API_KEY")
DB_PATH = r"C:\datos_agente\ecommerce.db"
client = Groq(api_key=API_KEY)

SCHEMA = """
Tienes acceso a una base de datos SQLite de un ecommerce brasileño con estas tablas:
- customers: customer_id, customer_city, customer_state
- orders: order_id, customer_id, order_status, order_purchase_timestamp
- order_items: order_id, product_id, seller_id, price, freight_value
- order_payments: order_id, payment_type, payment_value
- order_reviews: order_id, review_score, review_comment_message
- products: product_id, product_category_name, product_weight_g
- sellers: seller_id, seller_city, seller_state
- category_names: product_category_name, product_category_name_english
- geolocation: geolocation_zip_code_prefix, geolocation_city, geolocation_state
Genera SOLO la query SQL, sin explicaciones, sin markdown, sin comillas al inicio o al final.
"""

def ejecutar_query(query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    columnas = [desc[0] for desc in cursor.description]
    filas = cursor.fetchall()
    conn.close()
    return columnas, filas

def generar_query(pregunta):
    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SCHEMA},
            {"role": "user", "content": pregunta}
        ]
    )
    return respuesta.choices[0].message.content.strip()

def generar_grafico(df):
    cols_numericas = df.select_dtypes(include='number').columns.tolist()
    cols_texto = df.select_dtypes(include='object').columns.tolist()
    if len(cols_texto) >= 1 and len(cols_numericas) >= 1:
        return px.bar(df, x=cols_texto[0], y=cols_numericas[0],
                      color=cols_numericas[0], color_continuous_scale="Blues")
    elif len(cols_numericas) >= 2:
        return px.line(df, x=df.columns[0], y=df.columns[1])
    return None

def procesar_pregunta(pregunta):
    MAX_INTENTOS = 3
    for intento in range(MAX_INTENTOS):
        try:
            query = generar_query(pregunta)
            columnas, filas = ejecutar_query(query)
            df, reporte = limpiar_datos(columnas, filas)
            st.session_state.historial.append({
                "pregunta": pregunta,
                "query": query,
                "df": df,
                "reporte": reporte
            })
            return
        except Exception:
            if intento + 1 == MAX_INTENTOS:
                st.error(f"❌ No se pudo ejecutar tras {MAX_INTENTOS} intentos. Reformula la pregunta.")
            else:
                st.warning(f"⚠️ Intento {intento + 1} fallido, reintentando...")

# --- CONFIG ---
st.set_page_config(page_title="Agente SQL IA", page_icon="🤖", layout="wide")

if "historial" not in st.session_state:
    st.session_state.historial = []
if "pregunta_ejemplo" not in st.session_state:
    st.session_state.pregunta_ejemplo = None

# --- SIDEBAR ---
with st.sidebar:
    st.header("💡 Consultas de ejemplo")
    st.caption("Selecciona una consulta o escribe la tuya abajo")

    ejemplos = [
        "Selecciona una consulta...",
        "¿Cuáles son las 5 categorías más vendidas?",
        "¿Cuál es el estado con más clientes?",
        "¿Cuántos pedidos entregados vs cancelados?",
        "¿Cuál es el ticket medio de los pedidos?",
        "¿Cuáles son los 5 estados con más pedidos?",
        "¿Qué métodos de pago se usan más?",
        "¿Cuál es la puntuación media de las reseñas?",
        "¿Cuáles son los 5 vendedores con más ventas?",
    ]

    seleccion = st.selectbox("", ejemplos, key="selectbox_ejemplo")

    if st.button("▶️ Ejecutar consulta", use_container_width=True):
        if seleccion != "Selecciona una consulta...":
            st.session_state.pregunta_ejemplo = seleccion

    st.divider()
    st.markdown("**🗄️ Base de datos**")
    st.markdown("📦 9 tablas")
    st.markdown("📊 +100.000 registros")
    st.markdown("🇧🇷 Olist E-Commerce Brasil")

# --- MAIN ---
st.title("🤖 Agente SQL con IA")
st.caption("Escribe una pregunta en español y el agente generará la query SQL, limpiará los datos y mostrará el gráfico automáticamente.")

if st.session_state.pregunta_ejemplo:
    with st.spinner("Analizando..."):
        procesar_pregunta(st.session_state.pregunta_ejemplo)
    st.session_state.pregunta_ejemplo = None

pregunta = st.chat_input("Escribe tu pregunta aquí...")
if pregunta:
    with st.spinner("Analizando..."):
        procesar_pregunta(pregunta)

# --- HISTORIAL ---
for i, item in enumerate(reversed(st.session_state.historial)):
    with st.chat_message("user"):
        st.write(item["pregunta"])

    with st.chat_message("assistant"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**📝 Query generada:**")
            st.code(item["query"], language="sql")

            if item["reporte"]:
                st.markdown("**🧹 Limpieza aplicada:**")
                for r in item["reporte"]:
                    st.write(r)

            st.markdown(f"**📊 Resultados ({len(item['df'])} filas):**")
            st.dataframe(item["df"].head(10), use_container_width=True)

            csv = item["df"].to_csv(index=False).encode("utf-8")
            st.download_button(
                "💾 Descargar CSV",
                csv,
                f"resultado_{i}.csv",
                "text/csv",
                key=f"download_{i}"
            )

        with col2:
            fig = generar_grafico(item["df"])
            if fig:
                st.plotly_chart(fig, use_container_width=True, key=f"chart_{i}")

# --- BENCHMARK ---
st.divider()
st.subheader("⚡ Benchmark de velocidad")

if st.button("🏁 Ejecutar benchmark"):
    from src.benchmark import medir, PREGUNTAS

    resultados = []
    progress = st.progress(0)
    status = st.empty()

    for i, p in enumerate(PREGUNTAS):
        status.write(f"⏱️ Midiendo: {p}")
        resultado = medir(p)
        resultados.append(resultado)
        progress.progress((i + 1) / len(PREGUNTAS))

    df_bench = pd.DataFrame(resultados)

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_bench[["pregunta", "t_llm", "t_sql", "t_total"]], use_container_width=True)
    with col2:
        fig = px.bar(
            df_bench,
            x="pregunta",
            y=["t_llm", "t_sql"],
            title="Tiempo LLM vs SQL por consulta (segundos)",
            barmode="stack",
            labels={"value": "Segundos", "variable": "Fase"},
            color_discrete_map={"t_llm": "#1f77b4", "t_sql": "#ff7f0e"}
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    status.write("✅ Benchmark completado")