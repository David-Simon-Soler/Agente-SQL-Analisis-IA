from visualizar import generar_grafico, exportar_csv
from groq import Groq
import sqlite3
import os

from dotenv import load_dotenv
import os
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

API_KEY = os.getenv("GROQ_API_KEY")

DB_PATH = DB_PATH = r"C:\datos_agente\ecommerce.db"
print(f"🔍 Buscando DB en: {DB_PATH}")
print(f"🔍 Existe: {os.path.exists(DB_PATH)}")

# Configurar Groq
client = Groq(api_key=API_KEY)

# Esquema de la base de datos
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
    from pathlib import Path
    db = Path(DB_PATH)
    conn = sqlite3.connect(str(db.resolve()))
    cursor = conn.cursor()
    cursor.execute(query)
    columnas = [desc[0] for desc in cursor.description]
    filas = cursor.fetchall()
    conn.close()
    return columnas, filas

from limpieza import limpiar_datos

def agente(pregunta):
    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SCHEMA},
            {"role": "user", "content": pregunta}
        ]
    )
    query = respuesta.choices[0].message.content.strip()
    
    print(f"\n📝 Query generada:\n{query}")
    
    columnas, filas = ejecutar_query(query)
    
    # Limpiar datos
    df, reporte = limpiar_datos(columnas, filas)
    
    # Mostrar reporte de limpieza
    if reporte:
        print("\n🧹 Limpieza aplicada:")
        for item in reporte:
            print(f"   {item}")
    else:
        print("\n✅ Datos limpios, no se necesitaron cambios")
    
    # Mostrar resultados (máximo 10 filas)
    total = len(df)
    print(f"\n📊 Resultados ({total} filas en total, mostrando primeras 10):")
    print(df.head(10).to_string(index=False))
    
    if total > 10:
        print(f"\n   ... y {total - 10} filas más.")
# Exportar CSV para Power BI
    exportar_csv(df)
    
    # Generar gráfico automático
    generar_grafico(df, pregunta)       

# Loop principal
print("🤖 Agente SQL listo. Escribe tu pregunta en español.")
print("(escribe 'salir' para terminar)\n")

while True:
    pregunta = input("Tu pregunta: ")
    if pregunta.lower() == "salir":
        break
    agente(pregunta)