import pydeck as pdk
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_icon=":thumbs_up:",
    layout="wide",
)

@st.cache_data
def carga_data():
  return pd.read_excel("Chucao_cl.xlsx", header=0)

st.sidebar.write("Información sobre la cantidad de incendios forestales en la Región de Los Lagos en las temporadas 2017 a 2022.")

ciudad = carga_data()
ciudad["Fecha_de_Proceso"] = "27-04-2023"

st.header("Desafío final")
st.info("#### Visualización de geolocalización de avistamiento de Chucaos en Chile durante el período comprendido entre los años 2021 a 2023")

geo_puntos_visual = ciudad[["gbifID","kingdom", "phylum", "class", "order", "family", "genus", "species", "scientificName", "decimalLatitude", "decimalLongitude", "eventDate", "day","month", "year", "basisOfRecord", "Fecha_de_Proceso"]].rename(columns={
    "gbifID": "Código",
    "kingdom": "Reino",
    "phylum": "Phylum",
    "class": "Clase",
    "order": "Orden",
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

geo_data = geo_puntos_visual
geo_data["Fecha_de_Proceso"] = "08-11-2022"

st.info("#### Avistamiento de Chucaos en Chile.")
col_sel, col_map = st.columns([1, 2])

with col_sel:
  # Obtener los nombres unicos por mes
  Visualizacion = geo_puntos_visual["Mes"].sort_values().unique()

  visualizacion_seleccionada = st.multiselect(
    label="Filtrar por Mes de avistamiento", 
    options=Visualizacion,
    help="Selecciona el o los meses de avistamiento que desea visualizar",
    default=[] # También se puede indicar la variable "comunas", para llenar el listado
  )

    # Obtener los nombres unicos por mes
  Visualizacion = geo_puntos_visual["Año"].sort_values().unique()

  visualizacion_seleccionada2 = st.multiselect(
    label="Filtrar por Año de avistamiento", 
    options=Visualizacion,
    help="Selecciona el o los años de avistamiento que desea visualizar",
    default=[] # También se puede indicar la variable "comunas", para llenar el listado
  )
  st.write(geo_data.set_index("Código"))


geo_data = geo_puntos_visual

# Aplicar filtro de Mes
if visualizacion_seleccionada:
  geo_data = geo_puntos_visual.query("Mes == @visualizacion_seleccionada")

if visualizacion_seleccionada2:
  geo_data = geo_puntos_visual.query("Año == @visualizacion_seleccionada2")

if visualizacion_seleccionada and visualizacion_seleccionada2:
  geo_data = geo_puntos_visual[geo_puntos_visual['Mes'].isin(visualizacion_seleccionada) & geo_puntos_visual['Año'].isin(visualizacion_seleccionada2)]


avg_lat = np.median(geo_data["Latitud"])
avg_lng = np.median(geo_data["Longitud"])

puntos_mapa = pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=avg_lat,
        longitude=avg_lng,
        zoom=5.2,
        min_zoom=1,
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
            opacity=0.5,
            radius_scale=20,
            radius_min_pixels=3,
            get_fill_color=["Mes == 'Septiembre' ? 200 : 10", "Mes == 'Agosto' ? 10 : 100", 60, 230]
        ),
    ],
    tooltip={
        "html": "<b>Mes de avistamiento: </b> {Mes} <br/>"
                "<b> Año de avistamiento: </b>{Año} <br/>"
                "<b> Especie: </b> {Especie} <br/>"
                "<b>Tipo de registro: </b> {Tipo_registro} <br/>"
                "<b>Georreferencia (Lat, Lng): </b> [{Latitud}, {Longitud}] <br/>"
    }
)



with col_map:
    st.write(puntos_mapa)


st.write("Como podrán apreciar existen puntos geolocalizados en zonas del Océano Pácifico, esto es debido a un error en la toma de datos al momento de realizar el resgistro")