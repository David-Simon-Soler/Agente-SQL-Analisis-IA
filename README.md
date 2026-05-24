# 🤖 Agente SQL con IA + Consultor Automático Power BI (DAX)

Agente conversacional avanzado que permite consultar y analizar datos de un e-commerce real utilizando **lenguaje natural en español**, abstrayendo por completo la complejidad técnica.

El sistema ejecuta un **flujo dual en menos de 1 segundo**: genera y ejecuta la query SQL automáticamente sobre una base de datos de más de 100.000 registros, limpia los datos, renderiza visualizaciones interactivas y, en paralelo, deduce y escribe las **fórmulas DAX nativas** y la maquetación visual necesarias para replicar el informe de manera inmediata en Power BI.

---

## 🖥️ Demo

![Interfaz](https://github.com/David-Simon-Soler/Agente-SQL-Analisis-IA/blob/main/Assets/Interfaz.png) 

https://github.com/David-Simon-Soler/Agente-SQL-Analisis-IA/blob/main/Assets/Power_DAX.png

https://github.com/David-Simon-Soler/Agente-SQL-Analisis-IA/blob/main/Assets/Consulta_ejemplo.png

https://github.com/David-Simon-Soler/Agente-SQL-Analisis-IA/blob/main/Assets/Benchmark_velocidad_consulta.png

https://github.com/David-Simon-Soler/Agente-SQL-Analisis-IA/blob/main/Assets/Archivo_CSV_generado.png

---

## ⚙️ ¿Cómo funciona el flujo unificado?

```
Usuario escribe consulta analítica en español
                    ↓
       LLM (LLaMA 3.3 70B via Groq API)
                    ↓
     ┌──────────────┴──────────────┐
     ▼                             ▼
[Pipeline SQL & Python]   [Pipeline Business Intelligence]
Genera query SQL          Abstrae la lógica de negocio
       ↓                             ↓
SQLite ejecuta            Traduce a medidas DAX exactas
en >100k filas                       ↓
       ↓                  Recomienda visual nativa Power BI
Pandas limpia                        ↓
tipos y nulos             Expone bloque listo para copiar
       ↓                             ↓
     └──────────────┬──────────────┘
                    ↓
     Dashboard unificado en Streamlit
     + CSV listo para Power BI
```

---

## 🛠️ Tecnologías y Arquitectura

| Herramienta | Capa | Uso |
|---|---|---|
| Python | Core | Lenguaje base del ecosistema analítico |
| Groq API + LLaMA 3.3 70B | Inteligencia | Generador de queries SQL y motor de traducción a DAX |
| SQLite | Almacenamiento | Base de datos relacional local con datos indexados |
| Pandas | Procesamiento | Pipeline automático de data cleaning (tipos, nulos) |
| Plotly | Visualización | Gráficos interactivos dinámicos embebidos en el chat |
| Streamlit | Frontend | Interfaz web conversacional e interactiva |
| python-dotenv | Seguridad | Gestión de variables de entorno y credenciales API |

---

## 📊 Dataset

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

| Tabla | Registros | Descripción |
|---|---|---|
| orders | 99.441 | Estado de pedidos y timestamps |
| order_items | 112.650 | Precios, fletes y relaciones logísticas |
| order_payments | 103.886 | Métodos de pago y montos financieros |
| order_reviews | 99.224 | Puntuaciones y comentarios de clientes |
| customers | 99.441 | Ubicación geográfica de consumidores |
| products | 32.951 | Dimensiones, pesos y categorías |
| sellers | 3.095 | Datos operativos de vendedores |
| geolocation | 1.000.163 | Prefijos postales y coordenadas lat/long |
| category_names | 71 | Diccionario Portugués - Inglés |

---

## ⚡ Benchmark de Velocidad

Tiempos de procesamiento empíricos sobre el dataset de Olist (+100k registros):

| Consulta | LLM | SQL | Total |
|---|---|---|---|
| Top 5 productos más vendidos | 0.35s | 0.26s | 0.61s |
| Estado con mayor densidad de clientes | 0.15s | 0.07s | 0.22s |
| Ratio pedidos entregados vs cancelados | 0.22s | 0.02s | 0.24s |
| Top 5 estados con más volumen | 0.23s | 0.77s | 1.00s |
| Ticket medio por pedido | 0.30s | 0.09s | 0.39s |

---

## 🚀 Instalación

### 1. Clona el repositorio
```bash
git clone https://github.com/David-Simon-Soler/Agente-SQL-Analisis-IA.git
cd Agente-SQL-Analisis-IA
```

### 2. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 3. Configura tus credenciales
Crea un archivo `.env` en la raíz del proyecto:
```
GROQ_API_KEY=tu_api_key_aqui
```
Consigue tu API key gratuita en [console.groq.com](https://console.groq.com)

### 4. Descarga el dataset
Descarga los CSVs desde [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) y colócalos en `Data/raw/`

### 5. Carga la base de datos
```bash
python src/load_data.py
```

### 6. Ejecuta la app
```bash
streamlit run app.py
```
> En Windows puedes hacer doble clic en `iniciar.bat` para lanzarla directamente.

---

## 💬 Ejemplos de consultas

- ¿Cuáles son las 5 categorías más vendidas?
- ¿Cuál es el estado con más clientes?
- ¿Cuántos pedidos fueron entregados vs cancelados?
- ¿Cuál es el ticket medio de los pedidos?
- ¿Qué métodos de pago se usan más?
- ¿Cuál es la puntuación media de las reseñas?
- ¿Cuáles son los 5 vendedores con más ventas?

---

## 📁 Estructura del Proyecto

```
Agente-SQL-Analisis-IA/
├── Data/
│   └── raw/                  # CSVs originales de Kaggle
├── assets/                   # Capturas de pantalla y demos
├── outputs/                  # CSVs limpios generados por el usuario
├── src/
│   ├── load_data.py          # ETL: carga CSVs a SQLite
│   ├── agente.py             # Agente conversacional CLI
│   ├── limpieza.py           # Pipeline de normalización con Pandas
│   ├── visualizar.py         # Generación de gráficos con Plotly
│   ├── consultor_bi.py       # Módulo IA: traducción a DAX nativo Power BI
│   └── benchmark.py          # Evaluador de latencia LLM vs SQL
├── app.py                    # Dashboard principal en Streamlit
├── iniciar.bat               # Lanzador con doble clic (Windows)
├── .env                      # Credenciales privadas (excluido del repo)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 👨‍💻 Autor

**David José Simón Soler** — Junior Data Analyst · Graduado en Sociología

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/tuusuario)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/David-Simon-Soler)
