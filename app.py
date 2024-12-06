import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# Configuración inicial de la aplicación
st.title("Mapa Personalizado - Iquique, Chile")
st.write("Mapita con puntos de interes sobretodo para compritas.")

# Cargar datos desde un archivo CSV o usar datos de ejemplo
try:
    # Intentar cargar el archivo CSV si existe
    df = pd.read_csv("ubicaciones.csv")
except FileNotFoundError:
    # Datos de ejemplo si no existe el archivo CSV
    data = {
        "Nombre": ["Alojamiento 1", "Zofri", "Falabella", "Bar Playa", "Playa Cavancha"],
        "Categoria": ["Alojamiento", "Compras", "Compras", "Bares", "Playa"],
        "Latitud": [-20.2200, -20.2401, -20.2350, -20.2255, -20.2106],
        "Longitud": [-70.1500, -70.1350, -70.1400, -70.1550, -70.1482],
        "Descripcion": [
            "Nuestro alojamiento principal",
            "Centro comercial de Iquique",
            "Tienda por departamentos en la ciudad",
            "Bar frente al mar",
            "Principal playa turística de Iquique",
        ],
    }
    df = pd.DataFrame(data)

# Crear el mapa centrado en Iquique
mapa = folium.Map(location=[-20.2200, -70.1500], zoom_start=13)

# Agregar marcadores al mapa
for _, row in df.iterrows():
    folium.Marker(
        location=[row["Latitud"], row["Longitud"]],
        popup=f"{row['Nombre']} - {row['Descripcion']}",
        icon=folium.Icon(
            color="blue" if row["Categoria"] == "Compras" 
            else "green" if row["Categoria"] == "Alojamiento" 
            else "yellow" if row["Categoria"] == "Supermercado"
            else "red" if row["Categoria"] == "Bares" 
            else "purple" if row["Categoria"] == "Playa"
            else "gray"  # Por si hay categorías no especificadas
        ),
    ).add_to(mapa)

# Mostrar el mapa en Streamlit
st_data = st_folium(mapa, width=700, height=500)

# Instrucciones para editar puntos
st.write("### Cómo agregar más ubicaciones")
st.write(
    """
1. Descarga el archivo `ubicaciones.csv` desde abajo.
2. Agrega nuevas filas con los datos: `Nombre, Categoria, Latitud, Longitud, Descripcion`.
3. Guarda los cambios y recarga la aplicación para ver los nuevos puntos en el mapa.
"""
)

# Botón para descargar el archivo CSV
st.download_button(
    label="Descargar plantilla CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="ubicaciones.csv",
    mime="text/csv",
)
