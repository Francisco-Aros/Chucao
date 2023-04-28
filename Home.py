import streamlit as st
import streamlit.components.v1 as components

#Configuración inicial de la página
st.set_page_config(
    page_icon=":thumbs_up:",
    layout="wide"
)

st.sidebar.write("Accesibilidad en la ciudad de Valdivia al año 2016")

st.write("### Valdivia, Los Ríos")
st.write("En esta página web usted podrá observar datos referentes al grado de accesibilidad en algunos de los principales puntos de la ciudad de Valdivia.")
st.write("")
st.write("Reportaje de 24 Horas, TVN")

components.html("""
    <iframe width="900" height="500" 
    src="https://www.youtube.com/embed/0TxME69JIrU" 
    title="YouTube video player" frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen></iframe>
""", height=520)

st.write("Durante su navegación en esta página web podrá encontrar apartados con información mediante diversos gráficos realizados especialmente para esta ocación y mediante una visualización web.")
