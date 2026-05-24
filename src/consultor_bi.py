# src/consultor_bi.py
import os
from groq import Groq

PROMPT_EQUIVALENCIA_DAX = """
Eres un experto en Business Intelligence y Power BI. Tu única misión es recibir una consulta analítica de un e-commerce y traducirla en componentes nativos de Power BI.

Basándote en la pregunta del usuario y el esquema de la base de datos, devuelve una respuesta estructurada con:
1. 📐 **MEDIDAS DAX EQUIVALENTES**: Las fórmulas DAX exactas (en mayúsculas) necesarias para calcular esa métrica en Power BI usando el formato `Tabla[Columna]`. Usa DIVIDE para ratios.
2. 🎨 **VISUALIZACIÓN RECOMENDADA**: Indica qué tipo de gráfico nativo de Power BI (Gráfico de barras apiladas, gráfico de líneas, tarjeta, matriz) replica mejor el resultado y qué campos arrastrar a los campos de 'Eje X', 'Eje Y' o 'Valores'.

Sé muy conciso, directo al grano y utiliza estrictamente los nombres de las tablas y columnas reales del esquema proporcionado.
"""

def generar_equivalencia_dax(pregunta_usuario, query_sql, esquema_db):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": PROMPT_EQUIVALENCIA_DAX},
            {"role": "user", "content": f"Esquema de tablas:\n{esquema_db}\n\nPregunta: {pregunta_usuario}\n\nQuery SQL ejecutada: {query_sql}"}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.1,
    )
    return chat_completion.choices[0].message.content