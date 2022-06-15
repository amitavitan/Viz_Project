import pandas as pd
import streamlit as st


data = pd.read_csv("healthy_lifestyle_city_2021.csv")
st.dataframe(data)