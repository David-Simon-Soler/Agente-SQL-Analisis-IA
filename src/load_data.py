import pandas as pd
import sqlite3
import os

# Rutas absolutas
RAW_DATA_PATH = r"C:\Users\dss29\Desktop\GITHUB\PROYECTOS\PROYECTO 3\PROYECTO_3_AGENTE_IA\Data\raw"
DB_PATH = r"C:\datos_agente\ecommerce.db"
# Crear carpeta database si no existe
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
print(f"Carpeta database lista en: {os.path.dirname(DB_PATH)}")

# Crear conexión a SQLite
conn = sqlite3.connect(DB_PATH)

# Diccionario: nombre de tabla → archivo CSV
tables = {
    "customers":      "olist_customers_dataset.csv",
    "geolocation":    "olist_geolocation_dataset.csv",
    "order_items":    "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews":  "olist_order_reviews_dataset.csv",
    "orders":         "olist_orders_dataset.csv",
    "products":       "olist_products_dataset.csv",
    "sellers":        "olist_sellers_dataset.csv",
    "category_names": "product_category_name_translation.csv",
}

# Cargar cada CSV y subirlo a SQLite
for table_name, filename in tables.items():
    filepath = os.path.join(RAW_DATA_PATH, filename)
    print(f"Cargando {filename}...")
    
    df = pd.read_csv(filepath)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    
    print(f"  ✓ '{table_name}' → {len(df)} filas, {len(df.columns)} columnas")

conn.close()
print("\n✅ Base de datos creada en:", DB_PATH)