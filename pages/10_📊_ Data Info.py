# Import necessary libraries
import streamlit as st
import pandas as pd
from utils import load_data

st.set_page_config(layout="wide", page_icon="🚗", page_title="Data info")


characteristics, locations, users, vehicles = load_data(2021)
st.title("📊 Data Presentation")


st.write(
    "Link to the dataset: https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2021/#/community-reuses"
)

# Section "Accident Characteristics"
st.subheader("1.1. Accident Characteristics")
with st.expander("Show all"):
    st.write(
        "The dataset contains",
        characteristics.shape[0],
        "rows and",
        characteristics.shape[1],
        "columns.",
    )
    st.write("Here are the first 5 rows of the dataset:")
    st.dataframe(characteristics.head())
    st.write("Column descriptions:")
    st.write(
        """
    - **Num_Acc**: Accident number (unique identifier)
    - **jour, mois, an, hrmn**: Date and time of the accident
    - **lum**: Lighting conditions
    - **dep, com**: Department and municipality
    - **agg, int**: Aggregation zone and intersection type
    - **atm**: Atmospheric conditions
    - **col**: Type of collision
    - **adr**: Accident address
    - **lat, long**: Coordinates of the accident
    """
    )
    st.write("Here are the missing values in the dataset:")
    st.dataframe(characteristics.isna().sum())

# Section "Accident Locations"
st.subheader("1.2. Accident Locations")
with st.expander("Show all"):
    st.write(
        "The dataset contains",
        locations.shape[0],
        "rows and",
        locations.shape[1],
        "columns.",
    )
    st.write("Here are the first 5 rows of the dataset:")
    st.dataframe(locations.head())
    st.write("Column descriptions:")
    st.write(
        """
    - **catr, voie, v1, v2**: Road category and description
    - **circ**: Type of circulation
    - **nbv**: Number of lanes
    - **vosp, prof, pr, pr1, plan**: Road characteristics
    - **lartpc, larrout**: Roadway width
    - **surf**: Surface condition
    - **infra**: Infrastructure
    - **situ**: Situation
    - **vma**: Maximum allowed speed
    """
    )
    st.write("Here are the missing values in the dataset:")
    st.dataframe(locations.isna().sum())

# Section "Users in Accidents"
st.subheader("1.3. Users in Accidents")
with st.expander("Show all"):
    st.write(
        "The dataset contains", users.shape[0], "rows and", users.shape[1], "columns."
    )
    st.write("Here are the first 5 rows of the dataset:")
    st.dataframe(users.head())
    st.write("Column descriptions:")
    st.write(
        """
    - **place**: User's position in the vehicle
    - **catu**: User category
    - **grav**: Severity of injury
    - **sexe**: User's gender
    - **an_nais**: Year of birth
    - **trajet**: Type of journey
    - **secu1, secu2, secu3**: Safety equipment
    - **locp**: Pedestrian location
    - **actp**: Pedestrian action
    - **etatp**: Pedestrian condition (injury)
    """
    )
    st.write("Here are the missing values in the dataset:")
    st.dataframe(users.isna().sum())

# Section "Vehicles in Accidents"
st.subheader("1.4. Vehicles in Accidents")
with st.expander("Show all"):
    st.write(
        "The dataset contains",
        vehicles.shape[0],
        "rows and",
        vehicles.shape[1],
        "columns.",
    )
    st.write("Here are the first 5 rows of the dataset:")
    st.dataframe(vehicles.head())
    st.write("Column descriptions:")
    st.write(
        """
    - **id_vehicule**: Vehicle identifier
    - **senc**: Direction of travel
    - **catv**: Vehicle category
    - **obs, obsm, choc**: Fixed or mobile obstacle encountered
    - **manv**: Main maneuver before the accident
    - **motor**: Type of motorization
    - **occutc**: Number of occupants
    """
    )
    st.write("Here are the missing values in the dataset:")
    st.dataframe(vehicles.isna().sum())

# Section pour afficher le PDF
