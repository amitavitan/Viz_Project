import pandas as pd
import streamlit as st
import plotly.figure_factory as ff


data = pd.read_csv("healthy_lifestyle_city_2021.csv")
st.set_page_config(page_title='Tomi', initial_sidebar_state='expanded', layout="wide", page_icon="running")
st.dataframe(data)
# st.write(data.columns)

# st.bar_chart(data[['City', 'Sunshine hours(City)']])
hist_data = [data['Sunshine hours(City)']]

group_labels = ['Group 1']

# Create distplot with custom bin_size
fig = ff.create_distplot(hist_data, group_labels, bin_size=[.1])

# Plot!
st.plotly_chart(fig, use_container_width=True)