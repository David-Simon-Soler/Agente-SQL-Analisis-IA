import plotly.express as px
import pandas as pd
import os

OUTPUT_PATH = os.path.join(os.getcwd(), "outputs")
os.makedirs(OUTPUT_PATH, exist_ok=True)

def exportar_csv(df, nombre="resultado"):
    ruta = os.path.join(OUTPUT_PATH, f"{nombre}.csv")
    df.to_csv(ruta, index=False)
    print(f"\n💾 CSV exportado en: {ruta}")

def generar_grafico(df, pregunta):
    cols_numericas = df.select_dtypes(include='number').columns.tolist()
    cols_texto = df.select_dtypes(include='object').columns.tolist()

    if len(df.columns) < 2:
        print("\n⚠️ No hay suficientes columnas para graficar.")
        return

    try:
        # Si hay una columna de texto y una numérica → barras
        if len(cols_texto) >= 1 and len(cols_numericas) >= 1:
            fig = px.bar(
                df,
                x=cols_texto[0],
                y=cols_numericas[0],
                title=pregunta,
                color=cols_numericas[0],
                color_continuous_scale="Blues"
            )

        # Si hay dos columnas numéricas → línea
        elif len(cols_numericas) >= 2:
            fig = px.line(
                df,
                x=df.columns[0],
                y=df.columns[1],
                title=pregunta
            )

        # Si hay fechas → línea temporal
        elif df.dtypes[df.columns[0]] == 'datetime64[ns]':
            fig = px.line(
                df,
                x=df.columns[0],
                y=cols_numericas[0],
                title=pregunta
            )
        else:
            print("\n⚠️ No se pudo determinar el tipo de gráfico.")
            return

        # Guardar HTML interactivo
        nombre_archivo = "grafico_" + pregunta[:30].replace(" ", "_").replace("?", "")
        ruta_html = os.path.join(OUTPUT_PATH, f"{nombre_archivo}.html")
        fig.write_html(ruta_html)
        print(f"\n📈 Gráfico guardado en: {ruta_html}")
        fig.show()

    except Exception as e:
        print(f"\n⚠️ No se pudo generar el gráfico: {e}")