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
df3 = gpd.read_file('df3.geojson')


tab1, tab2, tab3, tab4, tab5 = st.tabs(['Análisis estadístico', 'Análisis gráfico específico', 'Análisis de hipótesis', 'Análisis georreferenciado', 'Indicador de bienestar'])

with tab1:
    st.dataframe(df.describe())

    t= """
    La media de cada una de las variables teniendo en cuenta los 17 años y los 15 países del panel,
    reflejan el desempeño de cada una de las variables escogidas para el estudio en la región a lo 
    largo del tiempo. La tasa  promedio de desempleo fue de 6.87%, el ingreso per cápita promedio fue 
    de $13,292 dólares, pasando al gasto per cápita en salud este fue de $ 1, 350 dólares, mientras 
    que el acceso a agua a recursos de agua dulce de la región en centímetros cúbicos fue de 20,948. 
    Finalmente la región contó con una tasa de desnutrición promedio de 6.25%.  
    """
    st.text(t)


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
    Textot="""
    Las medias de la tasa de desnutrición entre 2002 y 2019 reflejan el desempeño regional, siendo 
    Bolivia y Ecuador los países con las tasas más altas (19.75% y 15.24%, respectivamente), mientras 
    que Canadá y Estados Unidos tienen las tasas más bajas (2.5%). Respecto al ingreso per cápita, 
    Estados Unidos lidera con $50,825 anuales, mientras que Bolivia tiene el menor ingreso con $2,144 
    anuales. En cuanto al desempleo, Colombia muestra la peor tasa (10.65%), mientras que Bolivia tiene 
    la más baja (2.76%). En el gasto per cápita en salud, Estados Unidos destaca con $7,944, y 
    Bolivia tiene el menor gasto con $124. En términos de acceso per cápita a recursos de agua dulce, 
    Canadá lidera con 83,509 cm3, y México tiene el menor acceso con 3,623 cm3.
    """
    st.text(Textot)

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

    x= """
    Los mapas de calor, reflejan la relación entre las variables escogidas a lo largo de los años, 
    se evidencia que estas relaciones son homogeneas en los 17 años y que tienen una baja relación, 
    a excepción del pib y la salud que tenían una alta relación entre 0.96 y 0.97 para todos los años. 
    """
    st.text(x)
    
    st.divider()
    st.subheader('Análisis gráfico')
    
    fig, ax = plt.subplots(1, 1)
    fig = px.line(df, x="año", y="pib", color="pais",markers=True, title="Evolución del ingreso per capita")
    fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig)
    x= """
    La evolución del ingreso per capita, nos permite evidenciar en que puntos del panel de tiempo 
    los países tuvieron puntos altos o bajos, así mismo conocer cuales fueron los de mejor y peor 
    desempeño, evidenciando que los mejores resultados fueron los de Estados Unidos, seguido por 
    Canadá, pese a que ambos tuvieron caidas en 2009 que pueden deberse a la crisis financiera de 
    2008, nunca perdieron el mejor desempeño. Por su parte, el de peor desempeño fue Bolivia. 
    """
    st.text(x)
    
    fig, ax = plt.subplots(1, 1)
    fig = px.line(df, x="año", y="salud", color="pais",markers=True, title="Evolución del gasto en salud per capita")
    fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig)

    x= """
    La evolución del gasto en salud percapita, nos permite evidenciar en que puntos del panel de 
    tiempo los países tuvieron puntos altos o bajos, así mismo conocer cuales fueron los de mejor 
    y peor desempeño,se puede evidenciar, que los mejores resultados fueron para Estados Unidos y 
    Canadá, no obstante estas no fueron tan homogeneos a través del tiempo, ya que tuvieron puntos 
    altos y bajos. Por su parte,el país con peor desempeño a lo largo del tiempo fue Bolivia, se 
    logra evidenciar que Venezuela también baja su desempeño después del estallido de su crisis social. 
    """
    st.text(x)
    
    fig, ax = plt.subplots(1, 1)
    fig = px.line(df, x="año", y="agua", color="pais",markers=True, title="Evolución del acceso a recursos de agua dulce per capita")
    fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig)
    x= """
    La evolución del acceso a recursos de agua dulce, nos permite evidenciar en que puntos del panel 
    de tiempo los países tuvieron puntos altos o bajos, así mismo conocer cuales fueron los de mejor 
    y peor desempeño, algo interesante en general es que el acceso de recursos de agua dulce han disminuido 
    a lo largo del tiempo en los países de la región, los países con mejor desempeño son Canadá, Perú, Chile 
    y Colombia. 
    """
    st.text(x)
    
    fig, ax = plt.subplots(1, 1)
    fig = px.line(df, x="año", y="desempleo", color="pais",markers=True, title="Evolución del % de desempleados en la poblacion activa")
    fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig)

    x= """
    La evolución del acceso a recursos de agua dulce, nos permite evidenciar en que puntos del panel 
    de tiempo los países tuvieron puntos altos o bajos, así mismo conocer cuales fueron los de mejor 
    y peor desempeño, algo interesante en general es que el acceso de recursos de agua dulce han disminuido 
    a lo largo del tiempo en los países de la región, los países con mejor desempeño son Canadá, Perú, Chile 
    y Colombia. 
    """
    st.text(x)

    fig, ax = plt.subplots(1, 1)
    fig = px.line(df, x="año", y="nutricion", color="pais",markers=True, title="Evolución del % de la población en situacion de desnutrición")
    fig.update_traces(textposition="bottom right")
    st.plotly_chart(fig)

    x= """
    La evolución de la tasa de desnutrición, nos permite evidenciar en qué puntos del panel de tiempo 
    los países tuvieron puntos altos o bajos, así mismo conocer cuáles fueron los de mejor y peor 
    desempeño, entre los puntos destacables, se encuentra Bolivia que a inicios de 2002 con 26,9%, 
    logrando disminuir su tasa a 2019 en 11,9%. Mientras que una de las tasas más bajas antes de 2010, 
    se convirtió en una de las más altas, siendo el caso de Venezuela que a 2019 cerró con una tasa de 
    desnutrición de 24.9%. Mientras que la más baja de manera constante fue Canadá.  
    """
    st.text(x)

    fig, ax = plt.subplots(1, 1)
    fig = px.bar(df, x='año', y=['pib', 'desempleo'],
             color='pais',
             labels={'pib':'PIB', 'desempleo': 'Desempleo'},
             height=400)
    fig.update_layout(title_text='Comparación de PIB percapita y el desempleo a lo largo del tiempo')
    st.plotly_chart(fig)

    x= """
    Al comparar estas dos variables se logra evidenciar que la mayor participación la tiene Estados 
    Unidos, en cada uno de los años estudiados, mientras que los de menor participación fueron Brasil, 
    Perú y Colombia.
    """
    st.text(x)

    fig, ax = plt.subplots(1, 1)
    paises_interes = ['Colombia', 'Venezuela', 'Uruguay', 'Peru', 'Paraguay', 'Ecuador', 'Chile', 'Brasil', 'Bolivia', 'Argentina']
    df_filtrado = df[df['pais'].isin(paises_interes)]
    media_por_pais = df_filtrado.groupby(['pais']).agg({'pib': 'mean'}).reset_index()
    fig = px.bar(media_por_pais, x='pais', y='pib', title='Comparación de PIB percapita en America del Sur', text='pib',color='pais')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig)

    x= """
    Al hacer un análisis más centrado en la región de Sur, respecto al ingreso per cápita se puede 
    videnciar que el país con mayor ingreso, teniendo en cuenta la media entre 2002 y 2019 fue Uruguay 
    con  $12,170 dólares, seguido por Chile con $11, 667 dólares, mientras que el de menor ingreso per 
    cápita es Bolivia con $2, 144 dólares.
    """
    st.text(x)

    fig, ax = plt.subplots(1, 1)
    paises_interes = ['Colombia', 'Venezuela', 'Uruguay', 'Peru', 'Paraguay', 'Ecuador', 'Chile', 'Brasil', 'Bolivia', 'Argentina']
    df_filtrado = df[df['pais'].isin(paises_interes)]
    media_por_pais = df_filtrado.groupby(['pais']).agg({'salud': 'mean'}).reset_index()
    fig = px.bar(media_por_pais, x='pais', y='salud', title='Comparación del gasto percapita en salud en America del Sur', text='salud',color='pais')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig)

    x= """
    Al igual que en el anterior apartado, el mayor gasto en salud se encuentra en Uruguay con $1,044 
    dólares por persona, seguido de Argentina con $912 dólares en promedio de gasto per cápita. El país 
    con menor gasto fue Bolivia, que refleja uno de los peores desempeños a comparación de los demás 
    países de América del Sur.
    """
    st.text(x)

    fig, ax = plt.subplots(1, 1)
    paises_interes = ['Colombia', 'Venezuela', 'Uruguay', 'Peru', 'Paraguay', 'Ecuador', 'Chile', 'Brasil', 'Bolivia', 'Argentina']
    df_filtrado = df[df['pais'].isin(paises_interes)]
    media_por_pais = df_filtrado.groupby(['pais']).agg({'desempleo': 'mean'}).reset_index()
    fig = px.bar(media_por_pais, x='pais', y='desempleo', title='Comparación de % de desempleo en America del Sur', text='desempleo', color='pais')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig)

    x= """
    Teniendo en cuenta la media de la tasa de desempleo entre 2002 y 2019, el país con la tasa de 
    desempleo más alta fue Colombia con 10,66% seguido por Argentina con una tasa de 9,70%. 
    Por otro lado, el país con la menor tasa de desempleo en América del Sur es Bolivia con 2,76%, 
    lo cual sorprende teniendo en cuenta que anteriormente se evidenció que era el país con menor 
    ingreso per cápita. 
    """
    st.text(x)

    fig, ax = plt.subplots(1, 1)
    paises_interes = ['Colombia', 'Venezuela', 'Uruguay', 'Peru', 'Paraguay', 'Ecuador', 'Chile', 'Brasil', 'Bolivia', 'Argentina']
    df_filtrado = df[df['pais'].isin(paises_interes)]
    media_por_pais = df_filtrado.groupby(['pais']).agg({'agua': 'mean'}).reset_index()
    fig = px.bar(media_por_pais, x='pais', y='agua', title='Comparación de recursos internos renovables de agua dulce en America del Sur', text='agua', color='pais')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig)

    x= """
    Al revisar, el acceso a recursos de agua dulce en América del Sur, teniendo en cuenta la 
    disponibilidad per cápita, se evidencia que Perú es el país con mayor desempeño en esta 
    variable con un promedio de 55.554 centimetros cúbicos por habitante, mientras que el que 
    menor disponibilidad de este recurso tiene es Argentina con 7092 cm3. 
    """
    st.text(x)

    fig, ax = plt.subplots(1, 1)
    paises_interes = ['Colombia', 'Venezuela', 'Uruguay', 'Peru', 'Paraguay', 'Ecuador', 'Chile', 'Brasil', 'Bolivia', 'Argentina']
    df_filtrado = df[df['pais'].isin(paises_interes)]
    medias_por_pais = df_filtrado.groupby(['pais']).agg({'nutricion': 'mean'}).reset_index()
    fig = px.bar(medias_por_pais, x='pais', y='nutricion', title='Comparación de indices de desnutrición en America del Sur', text='nutricion',color='pais')
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig)

    x= """
    La media del % de desnutrición en América del Sur, permite ver que Bolivia tiene la 
    tasa más alta de la región, incluso duplicando el promedio de esta, con una tasa de 19,76%. 
    Mientras que la menor fue la de Uruguay con 2,86%, seguido de Chile con 3,12%.
    """
    st.text(x)
    
    fig, ax = plt.subplots(1, 1)
    paises_seleccionados = ['Argentina', 'Bolivia', 'Brazil', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Ecuador', 'Mexico', 'Paraguay', 'Peru', 'United States', 'Uruguay', 'Venezuela, RB']
    df_seleccionados = df[df['pais'].isin(paises_seleccionados)]
    media_pib = df_seleccionados.groupby('pais')['pib'].mean().reset_index()
    fig = px.treemap(media_pib, path=['pais'], values='pib',
                    title='Media del PIB ',
                    labels={'pib': 'Media del PIB per capita'})
    st.plotly_chart(fig)

    x= """
    Con este gráfico podemos evidenciar la proporción que abarca cada uno de los países 
    respecto al ingreso per cápita en los países de América, evidenciando que Estados 
    Unidos y Canadá son los países con mayor ingreso, por lo que son los países con mayor 
    participación, mientras que el  de menor participación es Bolivia.
    """
    st.text(x)

    fig, ax = plt.subplots(1, 1)
    paises_seleccionados = ['Argentina', 'Bolivia', 'Brazil', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Ecuador', 'Mexico', 'Paraguay', 'Peru', 'United States', 'Uruguay', 'Venezuela, RB']
    df_seleccionados = df[df['pais'].isin(paises_seleccionados)]
    media_pib = df_seleccionados.groupby('pais')['salud'].mean().reset_index()
    fig = px.treemap(media_pib, path=['pais'], values='salud',
                    title='Media del gasto en salud ',
                    labels={'salud': 'Media de gasto en salud'})
    st.plotly_chart(fig)

    x= """
    Con este gráfico podemos evidenciar la proporción que abarca cada uno de los países 
    respecto al  gasto en salud per cápita en los países de América, evidenciando 
    Estados Unidos y Canadá son los países con mayor gasto, no obstante, la participación 
    de Estados Unidos es casi el doble que la de Canadá, mientras que el  de menor participación 
    y por ende gasto son Bolivia y Perú.    
    """
    st.text(x)

    fig, ax = plt.subplots(1, 1)
    paises_seleccionados = ['Argentina', 'Bolivia', 'Brazil', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Ecuador', 'Mexico', 'Paraguay', 'Peru', 'United States', 'Uruguay', 'Venezuela, RB']

    df_seleccionados = df[df['pais'].isin(paises_seleccionados)]
    media_pib = df_seleccionados.groupby('pais')['desempleo'].mean().reset_index()
    fig = px.treemap(media_pib, path=['pais'], values='desempleo',
                    title='Media del desempleo',
                    labels={'desempleo': 'Media del desempleo (calculado en %)'})
    st.plotly_chart(fig)
    x= """
    Con este gráfico podemos evidenciar la proporción que abarca cada uno de los países 
    respecto a la media de la tasa de desempleo en los países de América, evidenciando 
    que esta es una de las variables más homogéneas, lo que refleja que varios países de 
    América tienen tasas de desempleo cercanas, sin embargo, la de mayor participación es 
    la de Colombia, y la de menor Bolivia. 
    """
    st.text(x)
    
    fig, ax = plt.subplots(1, 1)
    paises_seleccionados = ['Argentina', 'Bolivia', 'Brazil', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Ecuador', 'Mexico', 'Paraguay', 'Peru', 'United States', 'Uruguay', 'Venezuela, RB']
    df_seleccionados = df[df['pais'].isin(paises_seleccionados)]
    media_pib = df_seleccionados.groupby('pais')['agua'].mean().reset_index()
    fig = px.treemap(media_pib, path=['pais'], values='agua',
                    title='Media de recursos internos renovables de agua dulce per cápita (metros cúbicos)',
                    labels={'agua': 'Media de recursos internos'})
    st.plotly_chart(fig)

    x= """
    Con este gráfico podemos evidenciar la proporción que abarca cada uno de los países 
    respecto al  acceso de recursos de agua dulce en los países de América, evidenciando 
    que Canadá es el país con mayor participación, seguido de Perú y Chile, siendo que estos 
    dos tienen una proporción parecida. Por otro lado, el de menor participación es México.
    """
    st.text(x)
    
    fig, ax = plt.subplots(1, 1)
    paises_seleccionados = ['Argentina', 'Bolivia', 'Brazil', 'Canada', 'Chile', 'Colombia', 'Costa Rica', 'Ecuador', 'Mexico', 'Paraguay', 'Peru', 'United States', 'Uruguay', 'Venezuela, RB']
    df_seleccionados = df[df['pais'].isin(paises_seleccionados)]
    media_pib = df_seleccionados.groupby('pais')['nutricion'].mean().reset_index()
    fig = px.treemap(media_pib, path=['pais'], values='nutricion',
                    title='Media de Prevalencia de la desnutrición (% de la población)',
                    labels={'nutricion': 'Media de nutricion'})
    st.plotly_chart(fig)

    x= """
    Con este gráfico podemos evidenciar la proporción que abarca cada uno de los países 
    respecto a la tasa de desnutrición en los países de América, evidenciando  que Bolivia, 
    es el país con la mayor tasa de desnutrición, casi duplicando e incluso triplicando la 
    participación de la mayoría de países estudiados, a excepción de Ecuador que cuenta con 
    una tasa de desnutrición de 15,24%. Mientras que las tasas de desnutrición más baja, se 
    encuentran en países de Norte América siendo estos Estados Unidos y Canadá. 
    """
    st.text(x)

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

with tab3:

    st.subheader('Variable #1: Tasa de desempleo')
    latex_formula = r"H_0: \text{No hay diferencia significativa en las tasas de desempleo entre Colombia y Suramérica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en las tasas de desempleo entre Colombia y suramerica}"
    st.latex(latex_formula)
    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las 17 pruebas se obtuvo un valor p value menor 
    a 0.05, por lo que se rechaza la hipótesis nula. Con esto se puede decir que 
    existe una diferencia significativa en las tasas de desempleo 
    entre Colombia y los paises de Suramérica.
    """
    st.text(texto_simple)

    latex_formula = r"H_0: \text{No hay diferencia significativa en las tasas de desempleo entre Colombia y Norteamérica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en las tasas de desempleo entre Colombia y Norteamérica}"
    st.latex(latex_formula)

    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las pruebas de 2002 a 2010 se obtuvo un valor 
    p value menor a 0.05 por lo que se rechaza la hipótesis nula. Con esto se puede decir que 
    existe una diferencia significativa en las tasas de desempleo 
    entre Colombia y los paises de Norteamérica. 

    Sin embargo a partir del año 2011 hasta el 2019 se obtuvo un valor p value mayor a 0.05,
    por lo que no se puede rechazar la hipótesis nula lo que indica que no hay 
    diferencia significativa en las tasas de desempleo entre Colombia y Norteamérica.
    """
    st.text(texto_simple)

    st.subheader('Variable #2: PIB (Producto Interno Bruto)')
    latex_formula = r"H_0: \text{No hay diferencia significativa en el Ingreso Per Cápita entre Colombia y Suramérica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en el Ingreso Per Cápita entre Colombia y Suramerica}"
    st.latex(latex_formula)
    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las pruebas de 2002 a 2015 y de 2018 a 2019 se obtuvo un valor 
    p value menor a 0.05 por lo que se rechaza la hipótesis nula. Con esto se puede decir que 
    existe una diferencia significativa en el Ingreso Per cápita 
    entre Colombia y los paises de Suramérica. 

    Sin embargo en los años 2016 y 2017 se obtuvo un valor p value mayor a 0.05,
    por lo que no se puede rechazar la hipótesis nula lo que indica que no hay 
    diferencia significativa en el Ingreso Per Cápita entre Colombia y Suramérica.
    """
    st.text(texto_simple)

    latex_formula = r"H_0: \text{No hay diferencia significativa en el Ingreso Per Cápita entre Colombia y Norteamérica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en el Ingreso Per Cápita entre Colombia y Norteamérica}"
    st.latex(latex_formula)

    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las 17 pruebas se obtuvo un valor p value mayor a 0.05,
    por lo que no se puede rechazar la hipótesis nula lo que indica que no hay 
    diferencia significativa en el Ingreso Per Cápita entre Colombia y Norteamérica.
    """
    st.text(texto_simple)

    st.subheader('Variable #3: Salud')
    latex_formula = r"H_0: \text{No hay diferencia significativa del gasto en salud entre Colombia y Suramerica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia ignificativa del gasto en salud entre Colombia y Suramerica}"
    st.latex(latex_formula)
    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las 17 pruebas se obtuvo un valor p value mayor a 0.05,
    por lo que no se puede rechazar la hipótesis nula lo que indica que no hay 
    diferencia significativa en el gasto per cápita en salud entre Colombia y Suramérica.
    """
    st.text(texto_simple)

    latex_formula = r"H_0: \text{No hay diferencia significativa del gasto en salud entre Colombia y Norteamérica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia ignificativa del gasto en salud entre Colombia y Norteamérica}"
    st.latex(latex_formula)

    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las 17 pruebas se obtuvo un valor p value mayor a 0.05,
    por lo que no se puede rechazar la hipótesis nula lo que indica que no hay 
    diferencia significativa en el gasto per cápita en salud entre Colombia y Norteamérica.
    """
    st.text(texto_simple)

    st.subheader('Variable #4: Desnutrición')
    latex_formula = r"H_0: \text{No hay diferencia significativa en la tasa de desnutrición entre Colombia Suramerica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en la tasa de desnutrición entre Colombia y Suramerica}"
    st.latex(latex_formula)

    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las pruebas de 2002 a 2009 y de 2013 a 2019
    se obtuvo un valor p value mayor a 0.05,por lo que no se puede rechazar 
    la hipótesis nula lo que indica que no hay diferencia significativa en 
    la tasa de desnutrición entre Colombia y Suramérica.
    
    Sin embargo en los años 2010 a 2012 se obtuvo un valor p value menor a 0.05 
    por lo que se rechaza la hipótesis nula. Con esto se puede decir que 
    existe una diferencia significativa en la tasa de desnutrición 
    entre Colombia y los paises de Suramérica.
    """
    st.text(texto_simple)

    latex_formula = r"H_0: \text{No hay diferencia significativa en la tasa de desnutrición entre Colombia y Norteamérica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en la tasa de desnutrición entre Colombia y Norteamérica}"
    st.latex(latex_formula)

    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las 17 pruebas se obtuvo un valor p value mayor a 0.05,
    por lo que no se puede rechazar la hipótesis nula lo que indica que no hay 
    diferencia significativa en la tasa de denutrición entre Colombia y Norteamérica.
    """
    st.text(texto_simple)

    st.subheader('Variable #5: Acceso al agua')
    latex_formula = r"H_0: \text{No hay diferencia significativa en el acceso a recursos de agua dulce entre Colombia y Suramerica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en el acceso a recursos de agua dulce entre Colombia y Suramerica}"
    st.latex(latex_formula)

    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las 17 pruebas se obtuvo un valor p value menor 
    a 0.05, por lo que se rechaza la hipótesis nula. Con esto se puede decir que 
    existe una diferencia significativa en el acceso a recursos de agua dulce 
    entre Colombia y los paises de Suramérica.
    """
    st.text(texto_simple)

    latex_formula = r"H_0: \text{No hay diferencia significativa en el acceso a recursos de agua dulce entre Colombia y Norteamérica}"
    latex_formula += r", \\ H_1: \text{Existe una diferencia significativa en el acceso a recursos de agua dulce entre Colombia y Norteamérica}"
    st.latex(latex_formula)

    texto_simple = """
    Se realizó la prueba de hipótesis por año y en las 17 pruebas se obtuvo un valor p value mayor a 0.05,
    por lo que no se puede rechazar la hipótesis nula lo que indica que no hay 
    diferencia significativa en el acceso a recursos de agua dulce entre Colombia y Norteamérica.
    """
    st.text(texto_simple)


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
    
    for i, ax in enumerate(axs):
        year_range = years[i]
        start_year, end_year = map(int, year_range.split("-"))
        df_year = df3[(df3['año'] >= start_year) & (df3['año'] <= end_year)]
    
        df_year.plot(
            column="indicador",
            scheme="Quantiles",
            cmap="plasma",
            legend=True,
            legend_kwds={"fmt": "{:.0f}"},
            ax=ax,
        )
    
        ax.set_axis_off()
        ax.set_title(f"Indicador de bienestar {year_range} en Países de América")
    plt.suptitle("EVOLUCIÓN DEL INDICADOR DE BIENESTAR (2002-2019)")
    plt.tight_layout()
    st.pyplot(fig)






