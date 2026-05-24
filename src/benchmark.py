import time
import sqlite3
import os
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

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
Genera SOLO la query SQL, sin explicaciones, sin markdown, sin comillas.
"""

PREGUNTAS = [
    "cuales son los 5 productos mas vendidos?",
    "cual es el estado con mas clientes?",
    "cuantos pedidos fueron entregados vs cancelados?",
    "cuales son los 5 estados con mas pedidos?",
    "cual es el ticket medio de los pedidos?",
]

def medir(pregunta):
    # Medir tiempo LLM
    t0 = time.time()
    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SCHEMA},
            {"role": "user", "content": pregunta}
        ]
    )
    query = respuesta.choices[0].message.content.strip()
    t_llm = round(time.time() - t0, 3)

    # Medir tiempo SQL
    t1 = time.time()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    cursor.fetchall()
    conn.close()
    t_sql = round(time.time() - t1, 3)

    t_total = round(t_llm + t_sql, 3)

    return {
        "pregunta": pregunta,
        "t_llm": t_llm,
        "t_sql": t_sql,
        "t_total": t_total,
        "query": query
    }

if __name__ == "__main__":
    print("🏁 Iniciando benchmark...\n")
    resultados = []

    for pregunta in PREGUNTAS:
        print(f"⏱️  Midiendo: {pregunta}")
        resultado = medir(pregunta)
        resultados.append(resultado)
        print(f"   LLM: {resultado['t_llm']}s | SQL: {resultado['t_sql']}s | Total: {resultado['t_total']}s\n")

    df = pd.DataFrame(resultados)
    df.to_csv("outputs/benchmark.csv", index=False)
    print("✅ Benchmark completado. Resultados guardados en outputs/benchmark.csv")
    print(df[["pregunta", "t_llm", "t_sql", "t_total"]].to_string(index=False))