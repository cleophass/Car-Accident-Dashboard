import streamlit as st
from utils import load_data
import plotly.express as px
import plotly.graph_objects as go
import streamlit_toggle as tog


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
        width=1200,
        height=600,
        legend=dict(font=dict(size=30)),
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
    return fig


def create_normalized_histogram(df):
    df["surf"] = df["surf"].map(surf_mapping)
    df["grav"] = df["grav"].map(grav_mapping)

    # Filter out unwanted categories
    df = df[~df["surf"].isin(["Other", "Not specified"])]

    grouped = df.groupby(["surf", "grav"]).size().reset_index(name="count")
    grouped["count_normalized"] = grouped.groupby("surf")["count"].apply(
        lambda x: x / x.sum()
    )
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
    fig.update_layout(
        width=800,
        height=600,
    )
    return fig


def create_vma_fig(df):
    df["grav"] = df["grav"].map(grav_mapping)
    grouped = (
        df[df["vma"] < 130].groupby(["vma", "grav"]).size().reset_index(name="count")
    )
    grouped["count_normalized"] = grouped.groupby("vma")["count"].apply(
        lambda x: x / x.sum()
    )
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
        width=1200,
        height=600,
        template="plotly_white",
    )
    return fig


def display_road():
    st.title("🚙 Analysis of Road-Related Accidents and Weather Conditions 🚗")
    _, locations, users, _ = load_data(2021)
    df = users.merge(locations, on="Num_Acc")
    df1 = df.copy()
    df2 = df.copy()
    df3 = df.copy()
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.markdown("## Number of Accidents by Road Surface Condition")
    normalized_view = tog.st_toggle_switch(
        label="See it real representation in dataset !",
        key="Key1",
        default_value=False,
        label_after=False,
        inactive_color="#D3D3D3",
        active_color="#11567f",
        track_color="#29B5E8",
    )
    if normalized_view:
        fig = create_fig(df1)
        st.plotly_chart(fig)
    else:
        col1, col2 = st.columns(2)  # Create two columns

        # Adding space to align the pie chart with the histogram
        for _ in range(5):
            col1.write("\n")

        pie_chart = create_pie_chart(df1)
        col1.plotly_chart(pie_chart)  # Display pie chart in the first column
        normalized_hist = create_normalized_histogram(df3)
        col2.plotly_chart(normalized_hist)  # Display histogram in the second column
    st.markdown("## Number of Accidents by VMA")
    vma_fig = create_vma_fig(df2)
    st.plotly_chart(vma_fig)


display_road()
