import streamlit as st
import utils
import plotly.express as px

st.set_page_config(layout="wide", page_icon="🚗", page_title="Vehicles")

choc_description = {
    -1: "Non renseigné",
    0: "Aucun",
    1: "Avant",
    2: "Avant droit",
    3: "Avant gauche",
    4: "Arrière",
    5: "Arrière droit",
    6: "Arrière gauche",
    7: "Côté droit",
    8: "Côté gauche",
    9: "Chocs multiples (tonneaux)",
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

    # Ajouter toute filtration si nécessaire
    # df = df[~df["choc"].isin(["Certaines valeurs à exclure si nécessaire"])]

    fig = px.histogram(
        df,
        x="choc",
        color="grav",
        labels={
            "choc": "Impact Point",
            "grav": "Injury Severity",
            "count": "Number of Accidents",
        },
        color_discrete_sequence=px.colors.qualitative.Set1,
    )
    fig.update_layout(
        yaxis_type="log",
        width=1200,
        height=600,
        legend=dict(font=dict(size=30)),
    )
    return fig


# Adaptez les autres fonctions de la même manière...


def display_vehicles():
    # st.title("🚙 Analysis of Vehicles Accidents")
    # caracteristiques, users, lieux, vehicles = utils.load_data(2021)
    # df = vehicles.merge(users, on="Num_Acc")
    # df1 = df.copy()
    # df2 = df.copy()

    # # Pour afficher l'histogramme
    # fig = create_fig(df1)
    # st.plotly_chart(fig)

    # # Pour afficher le pie chart (en supposant que vous avez également adapté la fonction create_pie_chart)
    # # pie_chart = create_pie_chart(df2)
    # # st.plotly_chart(pie_chart)
    st.title("Coming soon...")


display_vehicles()
