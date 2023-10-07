# Discussing Gender
# Discussing the position in the car
# Pedestrian Action + Pedestrian Location: pedestrian status

import plotly.express as px
import streamlit as st
from utils import load_data


st.set_page_config(layout="wide", page_icon="🚗", page_title="Users")
journey_mapping = {
    1: "Home – Work",
    2: "Home – School",
    3: "Shopping",
    4: "Professional",
    5: "Drive",
    9: "Other",
}
injury_mapping = {
    1: "Unharmed",
    2: "Killed",
    3: "Hospitalized injury",
    4: "Slight injury",
}


def create_fig(df):
    # Apply the mapping to the DataFrame
    df["trajet"] = df["trajet"].map(journey_mapping)
    df["grav"] = df["grav"].map(injury_mapping)

    # Creation of the histogram
    fig = px.histogram(
        df,
        x="trajet",
        color="grav",
        labels={
            "trajet": "Reason for Journey",
            "grav": "Injury Severity",
            "count": "Number of Times",
        },
        color_discrete_sequence=px.colors.qualitative.Set1,
    )

    # Using a logarithmic scale for the Y-axis
    fig.update_layout(yaxis_type="log", width=1200, height=600)

    return fig


def create_fig_sex(df):
    # Groupement des données par sexe et comptage du nombre d'occurrences
    df_copy = df.copy()
    # drop line where value = -1
    df_copy = df_copy[df_copy["sexe"] != -1]

    # Mapping des codes de sexe à des chaînes de caractères pour une meilleure lisibilité
    sex_mapping = {1: "Male", 2: "Female"}
    sex_counts = df_copy["sexe"].value_counts().reset_index(name="count")
    sex_counts["index"] = sex_counts["index"].map(sex_mapping)

    fig = px.pie(
        sex_counts,
        values="sexe",
        names="index",
        hole=0.7,  # Ajoutez un trou au milieu du diagramme à secteurs pour en faire un diagramme en anneau
        color_discrete_sequence=[
            "#0068C9",
            "#83C9FF",
        ],  # Spécifiez les couleurs à utiliser
    )
    fig.update_layout(
        legend=dict(
            font=dict(
                size=20,  # Définir la taille de la police de la légende ici
            )
        )
    )

    # Mettez à jour les paramètres de mise en page supplémentaires

    # Affichez le graphique

    return fig


def create_normalized_accident_chart(df):
    # Suppression des lignes où le sexe ou la gravité est null
    df = df[df["sexe"].notnull() & df["grav"].notnull()]

    # Mapping des codes de sexe et de gravité
    sex_mapping = {1: "Male", 2: "Female"}
    grav_mapping = {
        1: "Unharmed",
        2: "Killed",
        3: "Hospitalized injury",
        4: "Slight injury",
    }

    df["sexe"] = df["sexe"].map(sex_mapping)
    df["grav"] = df["grav"].map(grav_mapping)

    # Calcul des totaux pour chaque combinaison de sexe et de gravité
    grouped = df.groupby(["sexe", "grav"]).size().reset_index(name="count")

    # Normalisation des comptages en fonction de la proportion de chaque sexe dans le dataset
    grouped.loc[grouped["sexe"] == "Male", "count_normalized"] = grouped["count"] / (
        1 - 0.316
    )
    grouped.loc[grouped["sexe"] == "Female", "count_normalized"] = (
        grouped["count"] / 0.316
    )

    # Création du graphique
    fig = px.bar(
        grouped,
        x="sexe",
        y="count_normalized",
        color="grav",
        barmode="group",
    )

    fig.update_layout(
        legend=dict(
            font=dict(
                size=20,  # Définir la taille de la police de la légende ici
            )
        )
    )
    # Affichage du graphique
    return fig


# Utilisation de la fonction


def create_journey_reason_pie_chart(df):
    # Apply the mapping
    df["trajet"] = df["trajet"].map(journey_mapping)

    journey_counts = df["trajet"].value_counts().reset_index()
    journey_counts.columns = ["trajet", "count"]
    fig = px.pie(journey_counts, names="trajet", values="count")
    fig.update_traces(textinfo="percent")
    return fig


def create_normalized_journey_reason_histogram(df):
    df["grav"] = df["grav"].map(injury_mapping)
    df["trajet"] = df["trajet"].map(journey_mapping)  # Apply the mapping here

    grouped = df.groupby(["trajet", "grav"]).size().reset_index(name="count")
    grouped["count_normalized"] = grouped.groupby("trajet")["count"].apply(
        lambda x: x / x.sum()
    )
    fig = px.histogram(
        grouped,
        x="trajet",
        y="count_normalized",
        color="grav",
        labels={
            "trajet": "Journey Reason",
            "grav": "Injury Severity",
            "count_normalized": "Proportion of Accidents",
        },
        color_discrete_sequence=px.colors.qualitative.Set1,
    )
    fig.update_layout(
        width=800,
        height=600,
    )
    return fig


def display_users():
    st.title("🚙 Analysis of user's info 🚗")

    _, locations, users, _ = load_data(2021)
    # Merge DataFrames on the 'Num_Acc' column
    df = users.merge(locations, on="Num_Acc")
    df1 = df.copy()
    df2 = df.copy()
    df3 = df.copy()
    df4 = df.copy()
    df5 = df.copy()
    st.markdown("""## Distribution des accidents par sexe """)
    st.write("\n\n\n\n")
    col1, col2 = st.columns(2)  # Créez deux colonnes

    with col1:  # Utilisez la première colonne
        st.markdown("""### Pourcentage d'hommes et de femmes dans le dataset""")

        fig_sx = create_fig_sex(df1)
        st.plotly_chart(fig_sx)

    st.write("\n\n\n\n")

    with col2:  # Utilisez la deuxième colonne
        st.markdown("""### Répartition normalisée des accidents par gravité""")
        fig_sx2 = create_normalized_accident_chart(df2)
        st.plotly_chart(fig_sx2)

    fig = create_fig(df3)
    st.write("\n\n\n\n")
    st.markdown("## Distribution of journey reasons with injury severity")

    normalized_view = st.toggle("See normalized representation!", value=False)

    if normalized_view:
        col1, col2 = st.columns(2)  # Create two columns
        for _ in range(5):  # Adjust the alignment if needed
            col1.write("\n")

        pie_chart = create_journey_reason_pie_chart(df4)
        col1.plotly_chart(pie_chart)  # Display pie chart in the first column

        normalized_hist = create_normalized_journey_reason_histogram(df5)
        col2.plotly_chart(normalized_hist)  # Display histogram in the second column
    else:
        st.plotly_chart(fig)


display_users()
