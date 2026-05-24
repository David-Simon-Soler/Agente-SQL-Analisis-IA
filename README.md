# 🤖 Agente SQL con IA

Agente conversacional que permite consultar y analizar datos de un ecommerce real usando **lenguaje natural en español**, sin necesidad de saber SQL.

El usuario escribe una pregunta, el agente genera la query SQL automáticamente, limpia los datos y devuelve una tabla interactiva, un gráfico y un CSV listo para Power BI, todo en menos de 1 segundo.

---

## 🖥️ Demo

![Interfaz principal](assets/Interfaz.png)

![Consulta de ejemplo](assets/Consulta_ejemplo.png)

![Benchmark de velocidad](assets/Benchmark_velocidad_consulta.png)

![CSV generado](assets/Archivo_CSV_generado.png)

---

## ⚙️ ¿Cómo funciona?

```
Usuario escribe en español
        ↓
   LLM (LLaMA 3.3 70B via Groq API)
        ↓
  Genera la query SQL automáticamente
        ↓
  SQLite ejecuta la query sobre +100k registros
        ↓
  Pandas limpia y transforma los datos
        ↓
  Streamlit muestra tabla, gráfico y CSV
```

---

## 🛠️ Tecnologías

| Herramienta | Uso |
|---|---|
| Python | Lenguaje principal |
| Groq API + LLaMA 3.3 70B | Generación de SQL desde lenguaje natural |
| SQLite | Base de datos local |
| Pandas | Limpieza y transformación de datos |
| Plotly | Visualizaciones interactivas |
| Streamlit | Interfaz web conversacional |
| python-dotenv | Gestión segura de credenciales |

---

## 📊 Dataset

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

| Tabla | Registros |
|---|---|
| orders | 99.441 |
| order_items | 112.650 |
| order_payments | 103.886 |
| order_reviews | 99.224 |
| customers | 99.441 |
| products | 32.951 |
| sellers | 3.095 |
| geolocation | 1.000.163 |
| category_names | 71 |

---

## ⚡ Benchmark de velocidad

Tiempo medio de respuesta sobre +100.000 registros reales:

| Consulta | LLM | SQL | Total |
|---|---|---|---|
| 5 productos más vendidos | 0.35s | 0.26s | 0.61s |
| Estado con más clientes | 0.15s | 0.07s | 0.22s |
| Pedidos entregados vs cancelados | 0.22s | 0.02s | 0.24s |
| 5 estados con más pedidos | 0.23s | 0.77s | 1.00s |
| Ticket medio de pedidos | 0.30s | 0.09s | 0.39s |

---

## 🚀 Instalación

### 1. Clona el repositorio
```bash
git clone https://github.com/tuusuario/agente-sql-ia.git
cd agente-sql-ia
```

### 2. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 3. Configura tu API key
Crea un archivo `.env` en la raíz del proyecto:
```
GROQ_API_KEY=tu_api_key_aqui
```
Consigue tu API key gratuita en [console.groq.com](https://console.groq.com)

### 4. Descarga el dataset
Descarga el dataset de [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) y coloca los CSVs en `Data/raw/`

### 5. Carga la base de datos
```bash
python src/load_data.py
```

### 6. Ejecuta la app
```bash
streamlit run app.py
```

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

## 📁 Estructura del proyecto

```
agente-sql-ia/
├── Data/
│   └── raw/                  # CSVs originales de Kaggle
├── assets/                   # Capturas de pantalla
├── outputs/                  # CSVs y gráficos generados
├── src/
│   ├── load_data.py          # Carga CSVs a SQLite
│   ├── agente.py             # Agente conversacional (CLI)
│   ├── limpieza.py           # Limpieza automática con Pandas
│   ├── visualizar.py         # Generación de gráficos con Plotly
│   └── benchmark.py          # Benchmark de velocidad
├── app.py                    # Interfaz web con Streamlit
├── iniciar.bat               # Lanzador con doble clic (Windows)
├── .env                      # API key (no se sube a GitHub)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 👨‍💻 Autor

**David José Simón Soler**
Sociólogo en transición a Analista de Datos

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/tuusuario)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/tuusuario)
