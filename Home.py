import streamlit as st
from PIL import Image
from utils import load_data, alignement

st.set_page_config(layout="wide", page_icon="🚗", page_title="Accidents in France")


st.title("💥 Analysis of Road Accidents in France")


# Merge DataFrames on the 'Num_Acc' column
from utils import load_data

alignement(3)
selected_year = st.slider(
    "Select a year", min_value=2019, max_value=2021, value=2021, step=1
)
characteristics, locations, users, vehicles = load_data(selected_year)
alignement(1)
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
<div style="max-width: 800px;">

## Objectives

##### Welcome to the continuation of our deep dive into road accidents.

###### The paramount objective of this analysis is to discern trends, patterns, and areas requiring improvement in road safety. It is through a nuanced understanding of these accidents that we can conceptualize and design effective strategies aimed at diminishing their occurrence in future.

###### Delving deep into such data is imperative. Each statistic not only represents an accident but potentially a life altered. By shedding light on these figures, we aspire to instigate changes – both at the policy level and among the general public.

###### The incentives fueling this research are manifold. Not only does it aim to spotlight areas and periods of high risk, but it also equips decision-makers with invaluable information, guiding infrastructure developments and awareness campaigns. Moreover, for the everyday traveler, it serves as a poignant reminder of the perils of the road, possibly fostering safer road behaviors.

###### As we proceed, we'll delve deeper into specific aspects of road safety, employing visual aids and data-driven insights. Through collective cognizance and actionable intelligence, we hope to journey towards safer roads for all.

Made by Cléophas Fournier
</div>
""",

    unsafe_allow_html=True,
)
