import streamlit as st
from utils import load_data
import folium
from folium.plugins import FastMarkerCluster, HeatMap
from streamlit_folium import folium_static
import numpy as np

st.set_page_config(layout="wide", page_icon="🚗", page_title="Location")


def display_fast_marker_cluster(city_data, city_coordinates):
    lats = city_data["lat"]
    lons = city_data["long"]
    m = folium.Map(location=city_coordinates, tiles="Cartodb Positron", zoom_start=12)
    FastMarkerCluster(data=list(zip(lats, lons))).add_to(m)
    folium.LayerControl().add_to(m)
    folium_static(m, width=900, height=600)


def display_heatmap(city_data, city_coordinates):
    city_map = folium.Map(location=city_coordinates, zoom_start=12)
    heat_data = [[row["lat"], row["long"]] for index, row in city_data.iterrows()]
    city_map.add_child(HeatMap(heat_data, radius=15))
    folium_static(city_map, width=900, height=600)


def display_location():
    # Sélection de la ville
    st.title("📌 Analysis of Location's Accidents")
    st.write("\n")
    city = st.radio("Choose a city", ("Paris", "Lyon", "Marseille", "Bordeaux", "Nice"))

    city_coords = {
        "Paris": (48.8566, 2.3522, 75),
        "Lyon": (45.7578, 4.8320, 69),
        "Marseille": (43.2965, 5.3698, 13),
        "Bordeaux": (44.8378, -0.5792, 33),
        "Nice": (43.7102, 7.2620, 6),
    }

    caracteristiques, _, _, _ = load_data(2021)
    city_data = caracteristiques[caracteristiques["dep"] == city_coords[city][2]]
    city_coordinates = city_coords[city][:2]

    st.title(f" Zoom on {city} ")

    accident_count = len(city_data)
    st.markdown(
        """
        <style>
        .red-text {
            color: red;
            font-size:30px !important;
            font-weight: bold;  
        }
        .big-text {
            font-size:30px !important;
            font-weight: bold;  
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<span class='big-text'>Number of accidents in {} : </span><span class='red-text'>{}</span>".format(
            city, accident_count
        ),
        unsafe_allow_html=True,
    )

    # Un bouton switch pour choisir entre Fast Marker Cluster et Heatmap
    is_heatmap = st.toggle("Try another map !", value=False)

    if is_heatmap:
        display_heatmap(city_data, city_coordinates)
    else:
        display_fast_marker_cluster(city_data, city_coordinates)

    st.markdown(
        """
    ## Map Interpretation

    The interactive map displays accident locations in the chosen city. There are two visualization modes:

    1. [**Fast Marker Cluster:**](https://github.com/Leaflet/Leaflet.markercluster) Accidents are shown as clusters. Zoom in to break these down for specific locations. Each cluster's number denotes total accidents in that vicinity. This visual helps spot areas with denser accidents.

    2. [**Heatmap:**](https://python-visualization.github.io/folium/latest/reference.html) Displays accident densities continuously. Warmer colors (reds, oranges) mark high accident zones, while cooler colors (blues) show lower ones. This gives a generalized view of accident hotspots.

    To navigate: 
    - Click and drag to move around.
    - Use zoom controls or mouse scroll for zooming.

    Understanding these visuals provides insights into accident-prone zones in the city. Not just for analysts or policymakers, but also for drivers and pedestrians to remain alert in these areas.
    """,
        unsafe_allow_html=True,
    )


display_location()
