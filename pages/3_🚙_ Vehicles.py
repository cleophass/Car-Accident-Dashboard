import streamlit as st
import utils

from utils import load_data, alignement
import plotly.express as px

st.set_page_config(layout="wide", page_icon="🚗", page_title="Vehicles")

choc_description = {
    -1: "Not specified",
    0: "None",
    1: "Front",
    2: "Front right",
    3: "Front left",
    4: "Rear",
    5: "Rear right",
    6: "Rear left",
    7: "Right side",
    8: "Left side",
    9: "Multiple impacts (rollover)",
}

grav_mapping = {
    1: "Unharmed",
    2: "Killed",
    3: "Hospitalized injury",
    4: "Slight injury",
}


def create_fig(df):
    df["choc"] = df["choc"].map(choc_description)
    df["grav"] = df["grav"].map(grav_mapping)

    # Grouper par 'choc' et 'grav' et calculer la taille de chaque groupe
    grouped = df.groupby(["choc", "grav"]).size().reset_index(name="count")

    # Normaliser le comptage pour chaque point d'impact (choc)
    count_normalized_series = (
        grouped.groupby("choc")["count"]
        .apply(lambda x: x / x.sum())
        .reset_index(level=0, drop=True)
    )
    grouped["count_normalized"] = count_normalized_series

    fig = px.histogram(
        grouped,
        x="choc",
        y="count_normalized",
        color="grav",
        labels={
            "choc": "Impact Point",
            "grav": "Injury Severity",
            "count_normalized": "Proportion d'accidents",
        },
        color_discrete_sequence=px.colors.qualitative.Set1,
    )
    fig.update_layout(
        width=900,
        height=500,
        legend=dict(font=dict(size=15)),
    )
    return fig


obs_mapping = {
    -1: "Not specified",
    0: "Not applicable",
    1: "Parked vehicle",
    2: "Tree",
    3: "Metal guardrail",
    4: "Concrete guardrail",
    5: "Other guardrail",
    6: "Building, wall, bridge pier",
    7: "Vertical signal support or emergency call post",
    8: "Post",
    9: "Urban furniture",
    10: "Parapet",
    11: "Island, refuge, high marker",
    12: "Curb",
    13: "Ditch, embankment, rock wall",
    14: "Other fixed obstacle on roadway",
    15: "Other fixed obstacle on sidewalk or shoulder",
    16: "Off-road without obstacle",
    17: "Pipe - aqueduct head",
}

obsm_mapping = {
    -1: "Not specified",
    0: "None",
    1: "Pedestrian",
    2: "Vehicle",
    4: "Rail vehicle",
    5: "Domestic animal",
    6: "Wild animal",
    9: "Other",
}


# Fonction pour créer un pie chart
def create_pie_chart(df, column, mapping):
    df[column] = df[column].map(mapping)
    fig = px.pie(df, names=column, hole=0.3)
    return fig


def display_vehicles():
    st.title("🚙 Analysis of Vehicles Accidents")
    alignement(3)

    selected_year = st.slider(
        "Select a year", min_value=2019, max_value=2021, value=2021, step=1
    )
    caracteristiques, lieux, users, vehicles = utils.load_data(selected_year)
    df = vehicles.merge(users, on="Num_Acc")
    df1 = df.copy()
    df2 = df.copy()

    # Pour afficher l'histogramme
    alignement(3)
    df1 = df1[df1.choc != -1]
    fig = create_fig(df1)

    st.markdown("### Accident severity by point of impact")
    st.plotly_chart(fig)

    alignement(3)
    # enlever 0 et -1 pour les colonnes obs et obsm
    df2 = df2[df2.obs != -1]
    df2 = df2[df2.obs != 0]
    df2 = df2[df2.obsm != -1]
    df2 = df2[df2.obsm != 0]
    df2 = df2[df2.obsm != 9]

    pie_chart_obs = create_pie_chart(df2, "obs", obs_mapping)

    st.markdown("### Fixed obstacle hit")
    st.plotly_chart(pie_chart_obs)
    alignement(2)

    st.markdown("### Mobile obstacle hit")
    pie_chart_obsm = create_pie_chart(df2, "obsm", obsm_mapping)
    st.plotly_chart(pie_chart_obsm)
    alignement(5)
    st.markdown(
        """
    ## Interpretation of the Analysis

    This analysis provides insights into various aspects of vehicle accidents:

    1. **Accident severity by point of impact:** The histogram illustrates the distribution of accident severity based on the point of impact. Understanding the common impact points in severe accidents can aid in vehicle design improvements.

    2. **Fixed obstacle hit:** The pie chart gives an overview of which fixed obstacles are most commonly hit in accidents. This information can be vital for city planning and infrastructure improvements.

    3. **Mobile obstacle hit:** This visualization provides insights into mobile obstacles that vehicles commonly collide with. It can be useful for traffic management and safety campaigns.

    It's crucial for policymakers, urban planners, and drivers to understand these patterns to make informed decisions and create safer roads.
    """,
        unsafe_allow_html=True,
    )


display_vehicles()
