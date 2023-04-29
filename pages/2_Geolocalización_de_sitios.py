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
            get_fill_color=["Provincia == 'Llanquihue' ? 200 : 10", "Provincia == 'Llanquihue' ? 0 : 100", 60, 230]
        ),
    ],
    tooltip={
        "html": "<b>Mes de avistamiento: </b> {Mes} <br/>"
                "<b> Especie: </b> {Especie} <br/>"
                "<b>Tipo de registro: </b> {Tipo_registro} <br/>"
                "<b>Georreferencia (Lat, Lng): </b> [{Latitud}, {Longitud}] <br/>"
    }
)




st.write(puntos_mapa)

st.write("Como podrán apreciar existen puntos geolocalizados en zonas del Océano Pácifico, esto es debido a un error en la toma de datos al momento de realizar el resgistro")