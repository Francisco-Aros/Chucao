import streamlit as st
import streamlit.components.v1 as components


#Configuración inicial de la página
st.set_page_config(
    page_icon=":thumbs_up:",
    layout="wide"
)

st.sidebar.write("Accesibilidad en la ciudad de Valdivia al año 2016")

st.write("### Valdivia, Los Ríos")
st.write("El motivo de esta web es poder geolocalizar los avistamientos del Scelorchilus rubecula, conocido popularmente como Chucao.")
st.write("Tal como es señalado en la web de Aves de Chile, el Chucao presenta una distrubución desde el sur de Colchagua hasta Aysén")
# Enlace a la página externa
st.write("Para obtener más información sobre el Chucao, visita la página web de [Aves de Chile](https://www.avesdechile.cl/174.htm) en la cual podrán encontrar información detallada de esta ave.", allow_markdown=True)

#Con el siguiente código en vez de que aparezca el enlace dentro de la misma línea de código, se saltará una línea y creará un nuevo hipervinculo en la palabra que se desee. st.markdown("[Aves de Chile](https://www.avesdechile.cl/174.htm)")
#Por otro lado, con el siguiente código, se creará una nueva línea en la visualización y aparecerá el enlace directo a la página web que se desea visitar. st.write('<a href="https://www.avesdechile.cl/174.htm" target="_blank">https://www.avesdechile.cl/174.htm</a>', unsafe_allow_html=True)


st.write("")
st.write("A continuación podrán apreciar un vídeo relacionado a diversas aves de neustro país y sus diferentes canticos, con el fin de poder diferenciarlos cuando nos encontremos en alguna visita o trabajo de campo.")

components.html("""
    <iframe width="860" height="520" 
    src="https://www.youtube.com/embed/kJf44ma0Rf8" 
    title="YouTube video player" frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; 
    web-share" allowfullscreen></iframe>
   """, height=520)

 #Se pueden agregar dos videos de youtube en el código dentro del mismo components.html, tan solo agregando dos vinculos generados por Youtube

st.write("Durante su navegación en esta página web podrá encontrar apartados con información mediante diversos gráficos realizados especialmente para esta ocación y mediante una visualización web.")
