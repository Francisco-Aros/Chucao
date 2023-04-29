import pydeck as pdk
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_icon=":thumbs_up:",
    layout="wide",
)

#Cargar el documento a utilizar, éste debe encontrarse en la misma carpeta desde donde se está trabajando
@st.cache_data
def carga_data():
  return pd.read_excel("Chucao_cl.xlsx", header=0)

st.sidebar.write(" Información sobre la cantidad de incendios forestales en la Región de Los Lagos en las temporadas 2017 a 2022.")


ciudad = carga_data()
ciudad["Fecha_de_Proceso"] = "27-04-2023"

st.header("Desafío final")
st.info("#### Visualización de geolocalización de incendios forestales en la Región de Los Lagos")
#Hasta aquí se encuentra operativo el código a la fecha del 29-04-23


#Se obtiene parte de la información contenida en excel para crear un nuevo DataFrame y se renombran las columnas para un mejor entendimiento.
#Desde aquí vuelve a estar operativo a la fecha del 29-04-23
geo_puntos_comuna = ciudad[["kingdom", "phylum", "class", "order", "family", "genus", "species", "scientificName", "decimalLatitude", "decimalLongitude", "eventDate", "day","month", "year", "basisOfRecord", "Fecha_de_Proceso"]].rename(columns={
    "kingdom": "Reino",
    "phylum": "Phylum",
    "class": "Clase",
    "Order": "Orden",
    "family": "Familia",
    "genus": "Genus",
    "species": "Especie",
    "scientificName": "Nombre_Cientifico",
    "decimalLatitude": "Latitud",
    "decimalLongitude": "Longitud",
    "eventDate": "Fecha_avistamiento",
    "day": "Día",
    "month": "Mes",
    "year": "Año",
    "basisOfRecord": "Tipo_registro"
})
geo_puntos_comuna.dropna(subset=["Fecha_avistamiento"], inplace=True)
geo_data = geo_puntos_comuna
geo_data["Fecha_de_Proceso"] = "08-11-2022"

avg_lat = np.median(geo_data["Latitud"])
avg_lng = np.median(geo_data["Longitud"])


#Lo que viene a continuación es una nueva parte del código para ver si puede ser agregado a la visualización
################################################################
col_bar, col_pie, col_table = st.columns(3, gap="large")
#Agrupar los datos en base a la columna donde están las comunas
#Se gnera la serie de la agrupación usando "Size()"
group_mes = geo_data.groupby(["Mes"]).size()
#Se ordena de mayor a menor, gracias al uso del parámetro "ascending="
group_mes.sort_values(axis="index", ascending=False, inplace=True)
#Ya se pueden obtener los 5 primeros registros
top5=group_mes[0:5]

##############################################################
st.info("#### Cantidad de incendios forestales por Comuna en la Región de Los Lagos")

col_sel, col_map = st.columns([1,2])

#Crear grupos por cantidad de puntos
group_200= group_mes.apply(lambda x: x if x <= 200 else None)
group_300= group_mes.apply(lambda x: x if x > 201 and x <=300 else None)
group_max= group_mes.apply(lambda x: x if x > 300 else None)

with col_sel:
    comunas_agrupadas = st.multiselect(
        label="Filtrar por grupos de mes",
        options=["Menos de 200 Puntos", "201 a 300 Puntos", "Más de 300 Puntos"],
        help="Selecciona la agrupación a mostrar",
        default=[]
    )
    st.write("")    #Con este comando "St.write("")" y dejandolo en blanco, puedo crear una línea imaginaría y realizar un salto dentro del recuadro.
    st.write("En el mapa que se aprecia a contnuación, ustedes podrán ver la geolocaliación de los avistamientos del Chucao en la zona correspondiente a Chile.")
filtrar = []

if "Menos de 200 Puntos" in comunas_agrupadas:
    filtrar = filtrar + group_200.index.tolist()

if "201 a 300 Puntos" in comunas_agrupadas:
    filtrar = filtrar + group_300.index.tolist()

if "Más de 300 Puntos" in comunas_agrupadas:
    filtrar = filtrar + group_max.index.tolist()
#Hasta aquí es la nueva parte del código que se agrega para ver si puede ser visualizada


print(comunas_agrupadas)


puntos_mapa = pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=avg_lat,
        longitude=avg_lng,
        zoom=5.2,
        min_zoom=6,
        max_zoom=15,
        pitch=10,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=geo_data,
            pickable=True,
            auto_highlight=True,
            get_position='[Longitud, Latitud]',
            filled=True,
            opacity=1,
            radius_scale=20,
            radius_min_pixels=3,
            get_fill_color=["Mes == '9' ? 200 : 10", "Mes == '9' ? 0 : 100", 60, 230]
        ),
    ],
    tooltip={
        "html": "<b>Mes de avistamiento: </b> {Mes} <br/>"
                "<b> Especie: </b> {Especie} <br/>"
                "<b>Tipo de registro: </b> {Tipo_registro} <br/>"
                "<b>Georreferencia (Lat, Lng): </b> [{Latitud}, {Longitud}] <br/>"
    }
)



with col_map:
    st.write(puntos_mapa)


st.write("Como podrán apreciar existen puntos geolocalizados en zonas del Océano Pácifico, esto es debido a un error en la toma de datos al momento de realizar el resgistro")