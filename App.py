import streamlit as st
from PIL import Image

st.set_page_config(layout="wide", page_icon="🚗", page_title="Accidents in France")


st.title("🚙 Analysis of Road Accidents in France :car:")


# Merge DataFrames on the 'Num_Acc' column
from utils import load_data

characteristics, locations, users, vehicles = load_data(2021)
data_complete = (
    characteristics.merge(users, on="Num_Acc")
    .merge(locations, on="Num_Acc")
    .merge(vehicles, on="Num_Acc")
)

# Calculate the total number of accidents after merging
total_accidents = len(data_complete["Num_Acc"].unique())

# Calculate the total number of deaths after merging
total_deaths = len(data_complete[data_complete["grav"] == 2]["Num_Acc"].unique())

st.markdown(
    f"""
<div style="display: inline-block;border: 5px solid blue;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total Accidents: <span style="color: blue; font-weight: bold;">{total_accidents}</span></h2></div>
<div style="display: inline-block;border: 5px solid red;border-radius: 25px;padding: 10px 20px;margin: 5px;margin-top: 50px;"><h2 style="margin: 5px;">Total Deaths:     <span style="color: red; font-weight: bold;">{total_deaths}</span></h2></div>
""",
    unsafe_allow_html=True,
)


# Introduction et présentation du projet
st.write(
    """
<div style="max-width: 800px;">

## Introduction

##### Welcome to my detailed project analyzing road accidents in France.

###### Every year, thousands of individuals are impacted by road accidents, and understanding the underlying factors is vital to enhancing road safety. With the growing population and ever-changing mobility, it's essential to take informed measures based on solid data to ensure the safety of all road users.

###### This dashboard is the culmination of rigorous exploration of vast datasets on road incidents collected between 2005 and 2021. By examining this data, we can gain valuable insights into trends, recurring patterns, and contributive factors of accidents.

###### My motivation behind this project is threefold. Firstly, by visualizing this data, we can pinpoint high-risk areas and times where caution is paramount. Secondly, it can assist policymakers and local authorities in understanding where to focus their efforts in terms of infrastructure and awareness. Finally, as citizens, we gain awareness and understanding, which in turn can lead to more cautious behavior on the roads.

###### As you navigate through this dashboard, you will uncover detailed statistics, visualizations, and analyses. My hope is that this information fosters a collective awareness and inspires actions to reduce the number of accidents on our roads.

</div>
""",
    unsafe_allow_html=True,
)

image = Image.open("assets/accident2.jpg")
st.write("<div style='text-align:center'>", unsafe_allow_html=True)
st.image(image, caption="Image de sensibilisation à la sécurité routière.", width=850)
st.write("</div>", unsafe_allow_html=True)
st.write(
    """
## Objectifs
L'objectif principal est d'identifier des tendances, des schémas et des points à améliorer 
en matière de sécurité routière. En ayant une meilleure compréhension de ces incidents, 
nous pouvons envisager des solutions pour réduire leur nombre à l'avenir.

## Méthodologie
J'ai commencé par collecter les données à partir du lien fourni, puis j'ai effectué un nettoyage 
et une transformation préliminaires. En utilisant Streamlit, j'ai construit ce dashboard interactif 
pour visualiser facilement les différentes facettes des données. 
"""
)
