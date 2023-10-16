# Discussing Gender
# Discussing the position in the car
# Pedestrian Action + Pedestrian Location: pedestrian status

import plotly.express as px
import streamlit as st
from utils import load_data, alignement

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
    fig.update_layout(yaxis_type="log", width=800, height=500)

    return fig


def create_fig_sex(df):
    # Groupement des données par sexe et comptage du nombre d'occurrences

    # drop line where value = -1
    df_copy = df[df["sexe"] != -1]
    sex_counts = df_copy["sexe"].value_counts().reset_index()

    # Mapping des codes de sexe à des chaînes de caractères pour une meilleure lisibilité
    sex_mapping = {1: "Male", 2: "Female"}
    sex_counts["sexe"] = sex_counts["sexe"].map(sex_mapping)

    fig = px.pie(
        sex_counts,
        values="count",
        names="sexe",
        hole=0.5,  # Ajoutez un trou au milieu du diagramme à secteurs pour en faire un diagramme en anneau
        color_discrete_sequence=[
            "#0068C9",
            "#83C9FF",
        ],  # Spécifiez les couleurs à utiliser
    )
    fig.update_layout(
        width=500,
        height=400,
        legend=dict(
            font=dict(
                size=15,  # Définir la taille de la police de la légende ici
            )
        ),
    )

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

    total_entries = len(df)
    female_count = (df["sexe"] == "Female").sum()
    female_percentage = female_count / total_entries

    grouped.loc[grouped["sexe"] == "Male", "count_normalized"] = grouped["count"] / (
        1 - female_percentage
    )
    grouped.loc[grouped["sexe"] == "Female", "count_normalized"] = (
        grouped["count"] / female_percentage
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
        width=500,
        legend=dict(
            font=dict(
                size=15,  # Définir la taille de la police de la légende ici
            )
        ),
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
    fig.update_layout(width=400, height=400)
    return fig


def create_normalized_journey_reason_histogram(df):
    df["grav"] = df["grav"].map(injury_mapping)
    df["trajet"] = df["trajet"].map(journey_mapping)  # Apply the mapping here

    grouped = df.groupby(["trajet", "grav"]).size().reset_index(name="count")

    # Corrigez l'erreur en réinitialisant l'index
    count_normalized = (
        grouped.groupby("trajet")["count"]
        .apply(lambda x: x / x.sum())
        .reset_index(drop=True)
    )
    grouped["count_normalized"] = count_normalized

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
        width=500,
        height=600,
    )
    return fig


def display_users():
    st.title("👤 Analysis of User's Information ")
    selected_year = st.sidebar.slider(
        "Select a year", min_value=2019, max_value=2021, value=2021, step=1
    )
    _, locations, users, _ = load_data(selected_year)
    alignement(3)
    # Merge DataFrames on the 'Num_Acc' column
    df = users.merge(locations, on="Num_Acc")
    df1 = df.copy()
    df2 = df.copy()
    df3 = df.copy()
    df4 = df.copy()
    df5 = df.copy()

    st.markdown("## Accident Distribution by Gender")
    alignement(4)
    col1, col2 = st.columns(2)  # Create two columns

    with col1:  # Use the first column
        st.markdown("### Percentage of Men and Women in the Dataset")

        fig_sx = create_fig_sex(df1)
        st.plotly_chart(fig_sx)

    with col2:  # Use the second column
        st.markdown("### Normalized Distribution of Accidents by Severity")
        fig_sx2 = create_normalized_accident_chart(df2)
        st.plotly_chart(fig_sx2)

    fig = create_fig(df3)

    st.markdown("## Distribution of Journey Reasons with Injury Severity")
    alignement(4)
    normalized_view = st.toggle("See Normalized Representation!", value=False)

    if normalized_view:
        col1, col2 = st.columns(2)  # Create two columns
        col1.markdown("### Pie chart of journey reason")  # Title for the pie chart
        for _ in range(5):  # Adjust the alignment if needed
            col1.write("\n")

        pie_chart = create_journey_reason_pie_chart(df4)

        col1.plotly_chart(pie_chart)  # Display pie chart in the first column

        normalized_hist = create_normalized_journey_reason_histogram(df5)
        col2.markdown(
            "### Normalized Distribution by Injury Severity"
        )  # Title for the histogram chart
        col2.plotly_chart(normalized_hist)  # Display histogram in the second column
    else:
        st.markdown("### Distribution of accident by Journey Reason")
        st.plotly_chart(fig)

    st.markdown(
        """
    ## Interpretation

    In the analysis of user information related to accidents, various aspects have been highlighted:

    1. **Accident Distribution by Gender:** This provides insights into the distribution of accidents based on gender, giving a clearer picture of which gender might be involved in accidents more frequently or which gender faces severe accidents more often.

    2. **Distribution of Journey Reasons with Injury Severity:** By observing the reasons for the journey, and mapping it against the severity of injuries, we can ascertain patterns or correlations between the purpose of the journey and the risk of severe injuries.

    3. **Normalized Representation:** Normalized data offers a relative perspective. It helps to understand the proportional distribution of data categories and removes any biases due to the sheer volume of one category over another.

    It's essential to interpret these visuals not as a tool to stereotype or blame but as a means to understand patterns, identify potential problem areas, and create awareness. Policymakers, planners, and the general public can use this data to make informed decisions, design better road safety campaigns, or understand the risks associated with different scenarios.
    """,
        unsafe_allow_html=True,
    )


display_users()
