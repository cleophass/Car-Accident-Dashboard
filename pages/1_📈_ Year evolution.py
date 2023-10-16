import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_icon="🚗", page_title="Yearly Evolution")

GRAVITY_MAPPING = {
    1: "Uninjured",
    2: "Killed",
    3: "Injured and hospitalized",
    4: "Minor injuries",
}


def convert_year(year):
    year = int(str(year).replace(",", ""))
    if 0 <= year < 100:
        return 2000 + year
    return year


def aggregate_accidents_by_year():
    all_data = []

    for year in range(2017, 2022):
        df_characteristics = pd.read_csv(
            f"assets/{year}/caracteristiques-{year}.csv",
            sep=";" if year > 2018 else ",",
            encoding="latin1",
        )
        df_users = pd.read_csv(
            f"assets/{year}/usagers-{year}.csv",
            sep=";" if year > 2018 else ",",
            encoding="latin1",
        )

        df_merged = pd.merge(df_characteristics, df_users, on="Num_Acc", how="inner")
        df_merged["an"] = df_merged["an"].apply(convert_year)
        all_data.append(df_merged)

    df_combined = pd.concat(all_data, ignore_index=True)
    return df_combined


def create_yearly_severity_graph(df):
    df["severity_text"] = df["grav"].map(GRAVITY_MAPPING)
    yearly_severity_counts = (
        df.groupby(["an", "severity_text"])
        .size()
        .reset_index(name="number_of_accidents")
    )

    fig = px.line(
        yearly_severity_counts,
        x="an",
        y="number_of_accidents",
        color="severity_text",
        title="Evolution of Accident Severity by Year",
    )

    return fig


def create_yearly_graph(df):
    yearly_counts = df.groupby("an").size().reset_index(name="number_of_accidents")

    fig = px.line(
        yearly_counts,
        x="an",
        y="number_of_accidents",
        title="Evolution of Number of Accidents by Year",
    )

    fig.update_layout(
        xaxis=dict(
            tickvals=yearly_counts["an"].unique(),
            tickangle=0,
        )
    )

    return fig


def display_year():
    st.title("📈 Yearly Evolution")

    graph_choice = st.radio(
        "Choose a graph type:", ["Count of Accidents", "Severity of Accidents"]
    )

    df = aggregate_accidents_by_year()

    if graph_choice == "Count of Accidents":
        fig = create_yearly_graph(df)
        st.markdown("## Graph showcasing the evolution of accident counts by year")
    else:
        fig = create_yearly_severity_graph(df)
        st.markdown("## Graph showcasing the evolution of accident severity by year")

    st.plotly_chart(
        fig, use_container_width=True
    )  # Ensuring both figures are of the same size


display_year()
