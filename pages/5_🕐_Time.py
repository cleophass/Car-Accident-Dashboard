import streamlit as st
import utils
import plotly.express as px
from utils import load_data, alignement
import pandas as pd

# comment every line below to explain what's happening
st.set_page_config(layout="wide", page_icon="🚗", page_title="Time")

# map each month number to its name
month_mapping = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "Septembre",
    10: "October",
    11: "November",
    12: "December",
}
# map each injury severity number to its name
grav_mapping = {
    1: "Unharmed",
    2: "Killed",
    3: "Hospitalized injury",
    4: "Slight injury",
}


def create_fig_hour(df):
    hourly_counts = df.groupby(["hour", "grav"]).size().reset_index(name="counts")

    fig = px.line(
        hourly_counts,
        x="hour",
        y="counts",
        color="grav",
        labels={
            "hour": "Hour of the Day",
            "counts": "Number of Accidents",
            "grav": "Injury Severity",
        },
        color_discrete_sequence=px.colors.qualitative.Set1,
    )
    fig.update_traces(mode="lines")
    fig.update_layout(
        width=900,
        height=400,
        legend=dict(
            title=None,
            font=dict(
                size=15,
            ),
        ),
    )
    return fig


def create_fig_month(df):
    df["mois"] = df["mois"].map(month_mapping)
    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "Septembre",
        "October",
        "November",
        "December",
    ]
    monthly_counts = df.groupby(["mois", "grav"]).size().reset_index(name="counts")
    monthly_counts["mois"] = pd.Categorical(
        monthly_counts["mois"], categories=month_order, ordered=True
    )
    monthly_counts = monthly_counts.sort_values(by="mois")
    fig = px.line(
        monthly_counts,
        x="mois",
        y="counts",
        color="grav",
        labels={
            "mois": "Month of the Year",
            "counts": "Number of Accidents",
            "grav": "Injury Severity",
        },
        color_discrete_sequence=px.colors.qualitative.Set1,
    )
    fig.update_traces(mode="lines")
    fig.update_layout(
        width=900,
        height=400,
        legend=dict(
            title=None,
            font=dict(
                size=15,
            ),
        ),
    )
    return fig


def display_time():
    st.title("🕐 Analysis of Accidents by Time")
    alignement(3)

    selected_year = st.slider(
        "Select a year", min_value=2019, max_value=2021, value=2021, step=1
    )
    caracteristiques, _, users, _ = load_data(selected_year)

    # Merge the dataframes
    merged_df = caracteristiques.merge(users, on="Num_Acc")
    merged_df["grav"] = merged_df["grav"].map(grav_mapping)

    alignement(5)

    st.markdown("### Number of accidents by hour")
    fig1 = create_fig_hour(merged_df)
    st.plotly_chart(fig1)

    # in merged_df order by asc column mois

    st.markdown("### Number of accidents by time of the year")
    fig2 = create_fig_month(merged_df)
    st.plotly_chart(fig2)


display_time()
