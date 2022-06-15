import pandas as pd
import streamlit as st


data = pd.read_csv("healthy_lifestyle_city_2021.csv")
st.set_page_config(page_title='Tomi', initial_sidebar_state='expanded', layout="wide", page_icon="running")
st.dataframe(data)
# st.write(data.columns)

# st.bar_chart(data[['City', 'Sunshine hours(City)']])
selected_ciry = st.radio('Pick one', list(data['City']), horizontal=True)
if selected_ciry == 'Tel Aviv':
    st.write('You selected Tel Aviv.')
    st.bar_chart(data['Sunshine hours(City)'])
else:
    st.write("You didn't select comedy.")

# st.bar_chart(chart_data)