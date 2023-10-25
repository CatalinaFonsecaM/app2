import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd


st.set_page_config(layout='wide')
st.title("Medición del bienestar")
df = pd.read_csv('dataframe.csv')
df2 = gpd.read_file('dataframe2.geojson')
df3 = pd.read_csv('df3.csv')

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Análisis estadístico', 'Análisis gráfico específico', 'Análisis de hipótesis', 'Análisis georreferenciado', 'Indicador de bienestar'])

with tab1:
    st.dataframe(df.describe())

    resumen = {}

    resumen['Medias nutricion'] = df.groupby(['pais']).agg({'nutricion':'mean'})
    resumen['Medias PIB'] = df.groupby(['pais']).agg({'pib':'mean'})
    resumen['Medias desempleo'] = df.groupby(['pais']).agg({'desempleo':'mean'})
    resumen['Medias salud'] = df.groupby(['pais']).agg({'salud':'mean'})
    resumen['Medias agua'] = df.groupby(['pais']).agg({'agua':'mean'})
    num_tables = len(resumen)
    num_columns = 5
    num_rows = (num_tables + num_columns - 1) // num_columns
    for i in range(num_rows):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            index = i * num_columns + j
            if index < num_tables:
                titulo, serie = list(resumen.items())[index]
                with cols[j]:
                    st.subheader(f"{titulo}")
                    st.dataframe(serie.reset_index()) 


    st.subheader('Mosaico de Mapas de Calor por Año')
    years = df['año'].unique()
    columnas_numericas = df.select_dtypes(include=['number'])
    num_columns = 4 
    num_rows = (len(years) + num_columns - 1) // num_columns
    for i in range(num_rows):
        cols = st.columns(num_columns)
        for j in range(num_columns):
            index = i * num_columns + j
            if index < len(years):
                year = years[index]
                with cols[j]:
                    st.subheader(f"Mapa de Calor para el Año {year}")
                    df_year = columnas_numericas[columnas_numericas['año'] == year]
                    corr_matrix = df_year.corr()
                    fig, ax = plt.subplots()
                    sns.heatmap(corr_matrix, annot=True, cmap="Blues", linewidths=0.5)
                    st.pyplot(fig)
    
    st.divider()
    st.subheader('Análisis gráfico')
    
    fig, ax = plt.subplots(1, 1)
    fig = px.line(df, x="año", y="pib", color="pais",markers=True, title="Evolución del ingreso per capita")
    fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    fig = px.line(df, x="año", y="salud", color="pais",markers=True, title="Evolución del gasto en salud per capita")
    fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    fig = px.line(df, x="año", y="agua", color="pais",markers=True, title="Evolución del acceso a recursos de agua dulce per capita")
    fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    fig = px.line(df, x="año", y="desempleo", color="pais",markers=True, title="Evolución del % de desempleados en la poblacion activa")
    fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    fig = px.line(df, x="año", y="nutricion", color="pais",markers=True, title="Evolución del % de la población en situacion de desnutrición")
    fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    fig = px.bar(df, x='año', y=['pib', 'desempleo'],
             color='pais',
             labels={'pib':'PIB', 'desempleo': 'Desempleo'},
             height=400)
    fig.update_layout(title_text='Comparación de PIB percapita y el desempleo a lo largo del tiempo')
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    paises_interes = ['Colombia', 'Venezuela', 'Uruguay', 'Peru', 'Paraguay', 'Ecuador', 'Chile', 'Brasil', 'Bolivia', 'Argentina']
    df_filtrado = df[df['pais'].isin(paises_interes)]
    media_por_pais = df_filtrado.groupby(['pais']).agg({'pib': 'mean'}).reset_index()
    fig = px.bar(media_por_pais, x='pais', y='pib', title='Comparación de PIB percapita en America del Sur', text='pib',color='pais')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    paises_interes = ['Colombia', 'Venezuela', 'Uruguay', 'Peru', 'Paraguay', 'Ecuador', 'Chile', 'Brasil', 'Bolivia', 'Argentina']
    df_filtrado = df[df['pais'].isin(paises_interes)]
    media_por_pais = df_filtrado.groupby(['pais']).agg({'salud': 'mean'}).reset_index()
    fig = px.bar(media_por_pais, x='pais', y='salud', title='Comparación del gasto percapita en salud en America del Sur', text='salud',color='pais')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    paises_interes = ['Colombia', 'Venezuela', 'Uruguay', 'Peru', 'Paraguay', 'Ecuador', 'Chile', 'Brasil', 'Bolivia', 'Argentina']
    df_filtrado = df[df['pais'].isin(paises_interes)]
    media_por_pais = df_filtrado.groupby(['pais']).agg({'desempleo': 'mean'}).reset_index()
    fig = px.bar(media_por_pais, x='pais', y='desempleo', title='Comparación de % de desempleo en America del Sur', text='desempleo', color='pais')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    paises_interes = ['Colombia', 'Venezuela', 'Uruguay', 'Peru', 'Paraguay', 'Ecuador', 'Chile', 'Brasil', 'Bolivia', 'Argentina']
    df_filtrado = df[df['pais'].isin(paises_interes)]
    media_por_pais = df_filtrado.groupby(['pais']).agg({'agua': 'mean'}).reset_index()
    fig = px.bar(media_por_pais, x='pais', y='agua', title='Comparación de recursos internos renovables de agua dulce en America del Sur', text='agua', color='pais')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    paises_interes = ['Colombia', 'Venezuela', 'Uruguay', 'Peru', 'Paraguay', 'Ecuador', 'Chile', 'Brasil', 'Bolivia', 'Argentina']
    df_filtrado = df[df['pais'].isin(paises_interes)]
    medias_por_pais = df_filtrado.groupby(['pais']).agg({'nutricion': 'mean'}).reset_index()
    fig = px.bar(medias_por_pais, x='pais', y='nutricion', title='Comparación de indices de desnutrición en America del Sur', text='nutricion',color='pais')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    paises_seleccionados = ['Argentina', 'Bolivia', 'Brazil', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Ecuador', 'Mexico', 'Paraguay', 'Peru', 'United States', 'Uruguay', 'Venezuela, RB']
    df_seleccionados = df[df['pais'].isin(paises_seleccionados)]
    media_pib = df_seleccionados.groupby('pais')['pib'].mean().reset_index()
    fig = px.treemap(media_pib, path=['pais'], values='pib',
                    title='Media del PIB ',
                    labels={'pib': 'Media del PIB per capita'})
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    paises_seleccionados = ['Argentina', 'Bolivia', 'Brazil', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Ecuador', 'Mexico', 'Paraguay', 'Peru', 'United States', 'Uruguay', 'Venezuela, RB']
    df_seleccionados = df[df['pais'].isin(paises_seleccionados)]
    media_pib = df_seleccionados.groupby('pais')['salud'].mean().reset_index()
    fig = px.treemap(media_pib, path=['pais'], values='salud',
                    title='Media del gasto en salud ',
                    labels={'salud': 'Media de gasto en salud'})
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    paises_seleccionados = ['Argentina', 'Bolivia', 'Brazil', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Ecuador', 'Mexico', 'Paraguay', 'Peru', 'United States', 'Uruguay', 'Venezuela, RB']

    df_seleccionados = df[df['pais'].isin(paises_seleccionados)]
    media_pib = df_seleccionados.groupby('pais')['desempleo'].mean().reset_index()
    fig = px.treemap(media_pib, path=['pais'], values='desempleo',
                    title='Media del desempleo',
                    labels={'desempleo': 'Media del desempleo (calculado en %)'})
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    paises_seleccionados = ['Argentina', 'Bolivia', 'Brazil', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Ecuador', 'Mexico', 'Paraguay', 'Peru', 'United States', 'Uruguay', 'Venezuela, RB']
    df_seleccionados = df[df['pais'].isin(paises_seleccionados)]
    media_pib = df_seleccionados.groupby('pais')['agua'].mean().reset_index()
    fig = px.treemap(media_pib, path=['pais'], values='agua',
                    title='Media de recursos internos renovables de agua dulce per cápita (metros cúbicos)',
                    labels={'agua': 'Media de recursos internos'})
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    paises_seleccionados = ['Argentina', 'Bolivia', 'Brazil', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Ecuador', 'Mexico', 'Paraguay', 'Peru', 'United States', 'Uruguay', 'Venezuela, RB']
    df_seleccionados = df[df['pais'].isin(paises_seleccionados)]
    media_pib = df_seleccionados.groupby('pais')['nutricion'].mean().reset_index()
    fig = px.treemap(media_pib, path=['pais'], values='nutricion',
                    title='Media de Prevalencia de la desnutrición (% de la población)',
                    labels={'nutricion': 'Media de nutricion'})
    st.plotly_chart(fig)
with tab2:
    st.subheader('Análisis gráfico específico')

    fig, ax = plt.subplots(1, 1)
    paises_seleccionados = ['Colombia','Mexico']
    df_seleccionados = df[df['pais'].isin(paises_seleccionados)]
    df_seleccionados['tamano_puntos'] = df_seleccionados['nutricion'].mean()
    fig = px.scatter(df_seleccionados, x='nutricion', y='salud', color='pais', size='tamano_puntos',
                    title='<b>Relación entre Nutrición y Salud en Colombia y México</b>',
                    labels={'nutricion': 'Nutrición', 'salud': 'Salud', 'tamano_puntos': 'Tamaño de Puntos'})
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    paises_seleccionados = ['Colombia','Mexico']
    df_seleccionados = df[df['pais'].isin(paises_seleccionados)]
    df_seleccionados['tamano_puntos'] = df_seleccionados['pib'].mean()
    fig = px.scatter(df_seleccionados, x='pib', y='desempleo', color='pais', size='tamano_puntos',
                    title='<b>Relación entre PIB percapita y Desempleo en Colombia y México</b>',
                    labels={'pib': 'PIB', 'desempelo': 'Desempleo', 'tamano_puntos': 'Tamaño de Puntos'})
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    paises_seleccionados = ['Colombia','United States']
    df_seleccionados = df[df['pais'].isin(paises_seleccionados)]
    df_seleccionados['tamano_puntos'] = df_seleccionados['pib'].mean()
    fig = px.scatter(df_seleccionados, x='pib', y='desempleo', color='pais', size='tamano_puntos',
                    title='<b>Relación entre PIB percapita y Desempleo en Colombia y Estados Unidos</b>',
                    labels={'pib': 'PIB', 'desempelo': 'Desempleo', 'tamano_puntos': 'Tamaño de Puntos'})
    st.plotly_chart(fig)

    fig, ax = plt.subplots(1, 1)
    paises_seleccionados = ['Colombia','United States']
    df_seleccionados = df[df['pais'].isin(paises_seleccionados)]
    df_seleccionados['tamano_puntos'] = df_seleccionados['nutricion'].mean()
    fig = px.scatter(df_seleccionados, x='nutricion', y='salud', color='pais', size='tamano_puntos',
                    title='<b>Relación entre Nutrición y Salud en Colombia y Estados Unidos</b>',
                    labels={'nutricion': 'Nutrición', 'salud': 'Salud', 'tamano_puntos': 'Tamaño de Puntos'})
    st.plotly_chart(fig)

with tab4:

    st.title("Mapa General")
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    df2.plot(
    cmap="plasma", 
    ax=ax)
    ax.set_axis_off()
    st.pyplot(fig)

    st.divider()
    fig, axs = plt.subplots(1, 5, figsize=(20, 4))
    columns = ["pib", "desempleo", "salud", "agua", "nutricion"]
    titles = ["PIB per cápita", "Desempleo", "Salud", "Recursos de agua", "Nivel de desnutrición"]

    for i, (column, title) in enumerate(zip(columns, titles)):
        ax = axs[i]
        df2.plot(
            column=column,
            scheme="Quantiles",
            cmap="plasma",
            legend=True,
            legend_kwds={"fmt": "{:.0f}"},
            ax=ax
        )
        ax.set_title(title)
        ax.set_axis_off()
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()
    st.subheader('Evolución por variables')
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    axs = axs.flatten()
    years = ["2002-2007", "2008-2011", "2012-2015", "2016-2019"]
    df2['año'] = df2['año'].astype(int)
    
    for i, ax in enumerate(axs):
        year_range = years[i]
        start_year, end_year = map(int, year_range.split("-"))
        df_year = df2[(df2['año'] >= start_year) & (df2['año'] <= end_year)]
    
        df_year.plot(
            column="pib",
            scheme="Quantiles",
            cmap="plasma",
            legend=True,
            legend_kwds={"fmt": "{:.0f}"},
            ax=ax,
        )
    
        ax.set_axis_off()
        ax.set_title(f"PIB de {year_range} en Países de América Latina")
    plt.suptitle("EVOLUCIÓN DEL PIB EN AMÉRICA LATINA (2002-2019)")
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    axs = axs.flatten()
    years = ["2002-2007", "2008-2011", "2012-2015", "2016-2019"]
    df2['año'] = df2['año'].astype(int)
    
    for i, ax in enumerate(axs):
        year_range = years[i]
        start_year, end_year = map(int, year_range.split("-"))
        df_year = df2[(df2['año'] >= start_year) & (df2['año'] <= end_year)]
    
        df_year.plot(
            column="pib",
            scheme="Quantiles",
            cmap="plasma",
            legend=True,
            legend_kwds={"fmt": "{:.0f}"},
            ax=ax,
        )
    
        ax.set_axis_off()
        ax.set_title(f"PIB de {year_range} en Países de América Latina")
    
    plt.suptitle("EVOLUCIÓN DEL PIB EN AMÉRICA LATINA (2002-2019)")
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    axs = axs.flatten()
    years = ["2002-2007", "2008-2011", "2012-2015", "2016-2019"]
    df2['año'] = df2['año'].astype(int)

    for i, ax in enumerate(axs):
    
        year_range = years[i]
        start_year, end_year = map(int, year_range.split("-"))
        df_year = df2[(df2['año'] >= start_year) & (df2['año'] <= end_year)]
    
        df_year.plot(
            column="salud",
            scheme="Quantiles",
            cmap="plasma",
            legend=True,
            legend_kwds={"fmt": "{:.0f}"},
            ax=ax,
        )
    
        ax.set_axis_off()
        ax.set_title(f"Gasto en salud  {year_range} en Países de América Latina")
    plt.suptitle("EVOLUCIÓN DEL GASTO EN SALUD EN AMÉRICA LATINA (2002-2019)")
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    axs = axs.flatten()
    years = ["2002-2007", "2008-2011", "2012-2015", "2016-2019"]
    df2['año'] = df2['año'].astype(int)

    for i, ax in enumerate(axs):
        year_range = years[i]
        start_year, end_year = map(int, year_range.split("-"))
        df_year = df2[(df2['año'] >= start_year) & (df2['año'] <= end_year)]
    
        df_year.plot(
            column="nutricion",
            scheme="Quantiles",
            cmap="plasma",
            legend=True,
            legend_kwds={"fmt": "{:.0f}"},
            ax=ax,
        )
    
        ax.set_axis_off()
        ax.set_title(f"Nivel de desnutricón de {year_range} en Países de América Latina")
    plt.suptitle("EVOLUCIÓN DE LA DESNUTRICIÓN EN AMÉRICA LATINA (2002-2019)")
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    axs = axs.flatten()
    years = ["2002-2007", "2008-2011", "2012-2015", "2016-2019"]
    df2['año'] = df2['año'].astype(int)
    for i, ax in enumerate(axs):
        year_range = years[i]
        start_year, end_year = map(int, year_range.split("-"))
        df_year = df2[(df2['año'] >= start_year) & (df2['año'] <= end_year)]
    
        df_year.plot(
            column="agua",
            scheme="Quantiles",
            cmap="plasma",
            legend=True,
            legend_kwds={"fmt": "{:.0f}"},
            ax=ax,
        )
    
        ax.set_axis_off()
        ax.set_title(f"Nivel de acceso al agua {year_range} en Países de América Latina")
    plt.suptitle("EVOLUCIÓN DEL ACCESO AL AGUA EN AMÉRICA LATINA (2002-2019)")
    plt.tight_layout()
    st.pyplot(fig)

    st.divider()
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    axs = axs.flatten()
    years = ["2002-2007", "2008-2011", "2012-2015", "2016-2019"]
    df2['año'] = df2['año'].astype(int)
    for i, ax in enumerate(axs):
        year_range = years[i]
        start_year, end_year = map(int, year_range.split("-"))
        df_year = df2[(df2['año'] >= start_year) & (df2['año'] <= end_year)]
    
        df_year.plot(
            column="desempleo",
            scheme="Quantiles",
            cmap="plasma",
            legend=True,
            legend_kwds={"fmt": "{:.0f}"},
            ax=ax,
        )
    
        ax.set_axis_off()
        ax.set_title(f"Nivel de desempleo {year_range} en Países de América Latina")
    plt.suptitle("EVOLUCIÓN DEL DESEMPLEO EN AMÉRICA LATINA (2002-2019)")
    plt.tight_layout()
    st.pyplot(fig)

with tab5:

    latex_formula = r"\frac{{PIB + Salud + Desnutrición + Agua}}{{Desempleo}}"
    st.latex(latex_formula)

    st.divider()
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    axs = axs.flatten()
    years = ["2002-2007", "2008-2011", "2012-2015", "2016-2019"]
    df3['año'] = df3['año'].astype(int)
    for i, ax in enumerate(axs):
        year_range = years[i]
        start_year, end_year = map(int, year_range.split("-"))
        df_year = df3[(df3['año'] >= start_year) & (df3['año'] <= end_year)]
        df_year.plot(
            column="indicador",
            cmap="plasma",
            legend=True,  # Habilita la leyenda
            ax=ax,
        )
        ax.set_axis_off()
        ax.set_title(f"Indicador de bienestar {year_range} en Países de América")
    plt.suptitle("EVOLUCIÓN DEL INDICADOR DE BIENESTAR (2002-2019)")
    plt.tight_layout()
    st.pyplot(fig)






