import pandas as pd
import streamlit as st


data = pd.read_csv("healthy_lifestyle_city_2021.csv")
st.set_page_config(page_title='Tomi', initial_sidebar_state='expanded', layout="wide", page_icon="🏃🏻‍")
st.dataframe(data)