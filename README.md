# 🤖 Agente SQL con IA + Consultor Automático Power BI (DAX)

Agente conversacional avanzado que permite consultar y analizar datos de un e-commerce real utilizando **lenguaje natural en español**, abstrayendo por completo la complejidad técnica. 

El sistema ejecuta un flujo dual en menos de 1 segundo: genera y ejecuta la query SQL automáticamente sobre una base de datos de más de 100,000 registros, limpia los datos, renderiza visualizaciones interactivas y, **en paralelo, deduce y escribe las fórmulas DAX nativas** y la maquetación visual necesarias para replicar el informe de manera inmediata en **Power BI**.

---

## 🖥️ Demo e Interfaz

![Interfaz principal](assets/Interfaz.png)

![Consulta de ejemplo](assets/Consulta_ejemplo.png)

![Módulo DAX y Réplica Power BI](assets/Archivo_CSV_generado.png)

![Benchmark de velocidad](assets/Benchmark_velocidad_consulta.png)

---

## ⚙️ ¿Cómo funciona el flujo unificado?

   Usuario escribe consulta analítica en español
                        ↓
         LLM (LLaMA 3.3 70B via Groq API)
                        ↓
     ┌──────────────────┴──────────────────┐
     ▼                                     ▼
[Pipeline SQL & Python]             [Pipeline Business Intelligence]
Genera query SQL optimizada         Abstrae la lógica de negocio
↓                                     ↓
SQLite ejecuta en >100k filas       Traduce a medidas DAX exactas
↓                                     ↓
Pandas limpia tipos y nulos        Recomienda visual nativa Power BI
↓                                     ↓
Renderiza tabla y Plotly             Expone bloque listo para copiar
└──────────────────┬──────────────────┘
▼
Dashboard unificado en Streamlit listo para descargar en CSV


---

## 🛠️ Tecnologías y Arquitectura

| Herramienta | Capa | Uso y Funcionalidad |
|---|---|---|
| **Python** | Core | Lenguaje base del ecosistema analítico |
| **Groq API + LLaMA 3.3 70B** | Inteligencia | Generador de consultas relacionales y motor de traducción a DAX |
| **SQLite** | Almacenamiento | Motor de base de datos relacional local con datos indexados |
| **Pandas** | Procesamiento | Pipeline automático de data cleaning (cast de tipos, gestión de nulos) |
| **Plotly** | Visualización | Gráficos interactivos dinámicos embebidos en el chat |
| **Streamlit** | Frontend | Interfaz web de usuario responsiva y panel interactivo |
| **python-dotenv** | Seguridad | Gestión de variables de entorno y protección de credenciales API |

---

## 📊 Dataset

El proyecto utiliza datos reales extraídos del [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), simulando un entorno empresarial complejo con más de **100,000 registros** interconectados.

| Tabla | Registros | Descripción de Datos |
|---|---|---|
| **orders** | 99.441 | Estado de pedidos y marcas de tiempo (timestamps) |
| **order_items** | 112.650 | Precios de productos, fletes y relaciones logísticas |
| **order_payments** | 103.886 | Métodos de pago, cuotas y montos financieros |
| **order_reviews** | 99.224 | Puntuaciones de satisfacción del cliente y comentarios |
| **customers** | 99.441 | Ubicación geográfica e identificadores de consumidores |
| **products** | 32.951 | Dimensiones, pesos y categorización de artículos |
| **sellers** | 3.095 | Datos operativos de los vendedores en Brasil |
| **geolocation** | 1.000.163 | Prefijos postales y coordenadas geográficas lat/long |
| **category_names** | 71 | Diccionario de traducción de categorías (Portugués - Inglés) |

---

## ⚡ Benchmark de Velocidad del Sistema

Análisis empírico del tiempo de procesamiento medio sobre el dataset de Olist (LLM + motor SQL local):

| Consulta de Negocio | Fase LLM | Fase SQL | Tiempo Total |
|---|---|---|---|
| Top 5 productos más vendidos | 0.35s | 0.26s | **0.61s** |
| Estado con mayor densidad de clientes | 0.15s | 0.07s | **0.22s** |
| Ratio de pedidos entregados vs cancelados | 0.22s | 0.02s | **0.24s** |
| Distribución de los 5 estados con más volumen | 0.23s | 0.77s | **1.00s** |
| Ticket medio transaccionado por pedido | 0.30s | 0.09s | **0.39s** |

---

## 🚀 Instalación y Despliegue Local

### 1. Clona el repositorio
```bash
git clone [https://github.com/David-Simon-Soler/Agente-SQL-Analisis-IA.git](https://github.com/David-Simon-Soler/Agente-SQL-Analisis-IA.git)
cd Agente-SQL-Analisis-IA
2. Instala el entorno de dependencias
Bash
pip install -r requirements.txt
3. Configura tus credenciales seguras
Crea un archivo .env en la raíz del proyecto para alojar tus credenciales (ignorado automáticamente por Git):

Fragmento de código
GROQ_API_KEY=tu_api_key_aqui
Consigue tu API key de alto rendimiento de manera gratuita en console.groq.com

4. Preparación de los Datos
Descarga los archivos estructurados desde Kaggle.

Ubica los archivos CSV descomprimidos dentro de la ruta Data/raw/.

Compila y migra los datos hacia el motor SQLite relacional ejecutando:

Bash
python src/load_data.py
5. Lanzamiento de la Aplicación
Lanza el servidor de Streamlit para desplegar la interfaz web interactiva en tu navegador local:

Bash
streamlit run app.py
📁 Estructura Arquitectónica del Proyecto
Agente-SQL-Analisis-IA/
├── Data/
│   └── raw/                  # Archivos fuente CSV cargados desde Kaggle
├── assets/                   # Recursos gráficos, demostraciones y capturas del sistema
├── outputs/                  # Repositorio local de CSVs limpios descargados por el usuario
├── src/
│   ├── load_data.py          # Script de automatización ETL: Carga CSVs raw hacia SQLite
│   ├── limpieza.py           # Pipeline de normalización y preprocesamiento de tipos con Pandas
│   ├── consultor_bi.py       # Módulo IA: Abstracción de reglas de negocio y traducción a DAX nativo
│   └── benchmark.py          # Evaluador automático de latencia y tiempos de respuesta (LLM vs SQL)
├── app.py                    # Orquestador del Dashboard principal y layouts en Streamlit
├── iniciar.bat               # Automatismo ejecutable para entornos Windows con un doble clic
├── .env                      # Almacén de claves privadas (Excluido en el repositorio)
├── .gitignore
├── requirements.txt
└── README.md
👨‍💻 Autor
David José Simón Soler - Junior Data Analyst
(Graduado en Sociología)

