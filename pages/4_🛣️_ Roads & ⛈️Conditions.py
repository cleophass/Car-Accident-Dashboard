import streamlit as st
from utils import load_data, alignement
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_icon="🚗", page_title="Roads & ⛈️Conditions")


surf_mapping = {
    -1: "Not specified",
    1: "Normal",
    2: "Wet",
    3: "Puddles",
    4: "Flooded",
    5: "Snow-covered",
    6: "Mud",
    7: "Icy",
    8: "Greasy substance – oil",
    9: "Other",
}

grav_mapping = {
    1: "Unharmed",
    2: "Killed",
    3: "Hospitalized injury",
    4: "Slight injury",
}

lum_mapping = {
    1: "Daylight",
    2: "Twilight or dawn",
    3: "Night without public lighting",
    4: "Night with public lighting off",
    5: "Night with public lighting on",
}


def create_fig(df):
    df["surf"] = df["surf"].map(surf_mapping)
    df["grav"] = df["grav"].map(grav_mapping)

    # Filter out unwanted categories
    df = df[~df["surf"].isin(["Other", "Not specified"])]

    fig = px.histogram(
        df,
        x="surf",
        color="grav",
        labels={
            "surf": "Road Surface Condition",
            "grav": "Injury Severity",
            "count": "Number of Accidents",
        },
        color_discrete_sequence=px.colors.qualitative.Set1,
    )
    fig.update_layout(
        yaxis_type="log",
        width=800,
        height=500,
        legend=dict(font=dict(size=15)),
    )
    return fig


def create_pie_chart(df):
    # Apply the mapping to the 'surf' column
    df["surf"] = df["surf"].map(surf_mapping)

    # Filter out unwanted categories
    df = df[~df["surf"].isin(["Other", "Not specified"])]

    surf_counts = df["surf"].value_counts().reset_index()
    surf_counts.columns = ["surf", "count"]
    fig = px.pie(surf_counts, names="surf", values="count")

    fig.update_traces(textinfo="percent")
    fig.update_layout(width=400, height=400)
    return fig


def create_normalized_histogram(df):
    df["surf"] = df["surf"].map(surf_mapping)
    df["grav"] = df["grav"].map(grav_mapping)

    # Filter out unwanted categories
    df = df[~df["surf"].isin(["Other", "Not specified"])]

    grouped = df.groupby(["surf", "grav"]).size().reset_index(name="count")

    # Modification ici
    count_normalized_series = (
        grouped.groupby("surf")["count"]
        .apply(lambda x: x / x.sum())
        .reset_index(level=0, drop=True)
    )
    grouped["count_normalized"] = count_normalized_series

    fig = px.histogram(
        grouped,
        x="surf",
        y="count_normalized",
        color="grav",
        labels={
            "surf": "Road Surface Condition",
            "grav": "Injury Severity",
            "count_normalized": "Proportion of Accidents",
        },
        color_discrete_sequence=px.colors.qualitative.Set1,
    )
    fig.update_layout(width=500)
    return fig


def create_vma_fig(df):
    df["grav"] = df["grav"].map(grav_mapping)
    grouped = (
        df[df["vma"] < 130].groupby(["vma", "grav"]).size().reset_index(name="count")
    )

    # Modification ici
    count_normalized_series = (
        grouped.groupby("vma")["count"]
        .apply(lambda x: x / x.sum())
        .reset_index(level=0, drop=True)
    )
    grouped["count_normalized"] = count_normalized_series

    fig = go.Figure()
    for grav in grouped["grav"].unique():
        subset = grouped[grouped["grav"] == grav]
        fig.add_trace(
            go.Scatter(
                x=subset["vma"],
                y=subset["count_normalized"],
                mode="lines",
                name=grav,
                line=dict(width=4),
            )
        )
    fig.update_layout(
        xaxis_title="VMA",
        yaxis_title="Proportion of Accidents",
        width=800,
        height=500,
        template="plotly_white",
    )
    return fig


def create_lum_pie_chart(df):
    df["lum"] = df["lum"].map(lum_mapping)
    lum_counts = df["lum"].value_counts().reset_index()
    lum_counts.columns = ["lum", "count"]
    fig = px.pie(lum_counts, names="lum", values="count")
    fig.update_traces(textinfo="percent")
    fig.update_layout(width=400, height=400)
    return fig


def create_lum_histogram(df):
    df["lum"] = df["lum"].map(lum_mapping)
    df["grav"] = df["grav"].map(grav_mapping)

    # Grouper par 'lum' et 'grav' et calculer la taille de chaque groupe
    grouped = df.groupby(["lum", "grav"]).size().reset_index(name="count")

    # Normaliser le comptage pour chaque condition d'éclairage (lum)
    count_normalized_series = (
        grouped.groupby("lum")["count"]
        .apply(lambda x: x / x.sum())
        .reset_index(level=0, drop=True)
    )
    grouped["count_normalized"] = count_normalized_series

    fig = px.histogram(
        grouped,
        x="lum",
        y="count_normalized",
        color="grav",
        labels={
            "lum": "Conditions d’éclairage",
            "grav": "Gravité de l'accident",
            "count_normalized": "Proportion d'accidents",
        },
        color_discrete_sequence=px.colors.qualitative.Set1,
    )
    fig.update_layout(width=500)
    return fig


def display_road():
    st.title("🛣️ Analysis of road-related accidents and weather conditions")
    selected_year = st.sidebar.slider(
        "Select a year", min_value=2019, max_value=2021, value=2021, step=1
    )
    carac, locations, users, _ = load_data(selected_year)
    df = users.merge(locations, on="Num_Acc")
    df = df.merge(carac, on="Num_Acc")
    df1 = df.copy()
    df2 = df.copy()
    df3 = df.copy()
    alignement(5)
    st.markdown("## Number of accidents by road surface condition")
    alignement(4)

    normalized_view = st.toggle("See it real representation in dataset!", value=False)

    if normalized_view:
        st.markdown(
            "### Accident distribution by road condition"
        )  # Title for the fig chart
        fig = create_fig(df1)
        st.plotly_chart(fig)
    else:
        col1, col2 = st.columns(2)  # Create two columns

        col1.markdown("### Accident distribution pie chart by road condition")
        # Adding space to align the pie chart with the histogram
        for _ in range(2):
            col1.write("\n")

        # Title for the pie chart
        pie_chart = create_pie_chart(df1)
        col1.plotly_chart(pie_chart)  # Display pie chart in the first column

        col2.markdown(
            "### Normalized accident distribution by road condition"
        )  # Title for the histogram chart
        normalized_hist = create_normalized_histogram(df3)
        col2.plotly_chart(normalized_hist)  # Display histogram in the second column

    alignement(4)

    st.markdown("## Number of accidents by VMA")
    alignement(2)

    st.markdown(
        "### Distribution of Accidents by Vehicle Maximum Authorized Speed (VMA)"
    )  # Title for the VMA chart
    vma_fig = create_vma_fig(df2)
    st.plotly_chart(vma_fig)

    alignement(4)
    st.markdown("## Distribution of accidents by lighting conditions")
    alignement(2)
    col1, col2 = st.columns(2)  # Création de deux colonnes

    # Pie Chart pour la colonne lum

    col1.markdown("### pie chart of accidents by lighting conditions")
    df4 = df.copy()
    lum_pie_chart = create_lum_pie_chart(df4)
    col1.plotly_chart(lum_pie_chart)

    # Histogramme pour grav en fonction de lum
    col2.markdown("### Sevrity of accident severity by lighting Conditions")

    df5 = df.copy()
    lum_hist = create_lum_histogram(df5)
    col2.plotly_chart(lum_hist)
    alignement(5)
    st.markdown(
        """
    ## Interpretation & Insights

    The given visuals delve deep into the accidents concerning various road and weather conditions:

    1. **Road Surface Condition:** Understanding how different road conditions, whether it's wet, flooded, icy, or greasy, impact the severity of accidents is crucial. As seen, certain surfaces might have higher occurrences of severe injuries or fatalities.

    2. **Vehicle Maximum Authorized Speed (VMA):** This depicts the relationship between the authorized speed of vehicles involved and the accident's severity. A clear insight can be how speeds correlate with fatal accidents.

    3. **Lighting Conditions:** The lighting conditions during which accidents occur can greatly influence their outcomes. It's observable that accidents happening at night without public lighting might have different injury severities compared to those in broad daylight.

    By understanding these insights, policymakers can design better road safety measures. Drivers can also be more cautious depending on the prevailing conditions. Whether it's slowing down on icy roads or being extra alert in areas without proper lighting, these insights can aid in accident prevention and safety enhancement.

    """,
        unsafe_allow_html=True,
    )


display_road()
