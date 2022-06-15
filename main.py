import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

data = pd.read_csv("healthy_lifestyle_city_2021.csv")
st.set_page_config(page_title='Tomi', initial_sidebar_state='expanded', layout="wide", page_icon="running")
st.dataframe(data)
# st.write(data.columns)

# st.bar_chart(data[['City', 'Sunshine hours(City)']])
columns = data.columns.tolist()

selected_columns = st.multiselect("select column", columns, default="location")
s = data[selected_columns[0]].str.strip().value_counts()