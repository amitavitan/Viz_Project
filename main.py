import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import re
from plotly.graph_objs import *
import plotly.graph_objects as go
import numpy as np
import plotly.figure_factory as ff
from sklearn.linear_model import LinearRegression

# Emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
# st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")
st.set_page_config(page_title='healthy_lifestyle', initial_sidebar_state='expanded', layout="wide", page_icon="running")


# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    data = pd.read_csv("healthy_lifestyle_city_2021.csv")
    # preprocess

    # replace pounds to shekels
    data['Cost of a bottle of water(City)'] = 4.24 * (
        data['Cost of a bottle of water(City)'].str.replace('£', '')).astype(
        float)
    data['Cost of a monthly gym membership(City)'] = 4.24 * (
        data['Cost of a monthly gym membership(City)'].str.replace('£', '')).astype(float)
    # replace % to float value
    data['Obesity levels(Country)'] = 0.01 * (data['Obesity levels(Country)'].str.replace('%', '')).astype(float)
    data = data.fillna(0)  # only != 0
    for col in data.columns:
        if col == "City":
            continue
        else:
            try:
                data[col] = data[col].astype(float)
            except:
                data[col] = data[col].str.replace('-', '0').astype(float)
                pass

    data.loc[[6, 11, 12, 16, 17, 20, 23, 25, 28, 30, 31], "Continent"] = "Asia"
    data.loc[[0, 2, 3, 4, 5, 7, 8, 15, 18, 19, 21, 27, 32, 34, 36, 37, 39, 42], "Continent"] = 'Europe'
    data.loc[[1, 10], "Continent"] = 'Australia'
    data.loc[[9, 14, 24, 26, 29, 33, 40, 41, 43], "Continent"] = ' North America'
    data.loc[[13, 35], "Continent"] = 'South America'
    data.loc[[22, 38], "Continent"] = 'Africa'
    iso_alpha3 = ['NLD', 'AUS', 'AUT', 'SWE', 'DNK', 'FIN', 'JPN', 'DEU', 'ESP', 'CAN', 'AUS', 'CHN', 'THA', 'ARG',
                  'CAN', 'ESP',
                  'IDN', 'KOR', 'DEU', 'CHE', 'ISR', 'TUR', 'EGY', 'TWN', 'USA', 'IND', 'USA', 'IRL', 'JPN', 'USA',
                  'HKG', 'CHN',
                  'BEL', 'USA', 'FRA', 'BRA', 'CHE', 'GBR', 'ZAF', 'ITA', 'USA', 'USA', 'RUS', 'MEX']
    data['iso_alpha'] = iso_alpha3

    return data


df = get_data_from_excel()
columns = list(df.columns)
columns.remove("City")
columns.remove("Rank")
columns.remove("Continent")
columns.remove('iso_alpha')


def clean_col_name(col_name, is_list=False):
    if is_list:
        return [re.sub("[\(\[].*?[\)\]]", "", col) for col in col_name]
    return re.sub("[\(\[].*?[\)\]]", "", col_name)


####################
### INTRODUCTION ###
####################

# ---- MAINPAGE ----
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns((.1, 2.3, .1, 1.3, .1))
with row0_1:
    st.title(':bar_chart: Lifestyle Dashboard - Healthy Habits :bar_chart:')
    st.markdown("##")
with row0_2:
    st.text("")
    st.subheader('Streamlit App by Amit Avitan & Emily Toyber')
row1_spacer1, row1_1, row1_spacer2 = st.columns((.1, 3.2, .1))
with row1_1:
    st.markdown("first paragraph - introduction")
    st.markdown("second paragraph - explanation and github repo")

####################
### SELECTION ###
####################

# ---- RAW DATA ----
st.markdown("")
see_data = st.expander('Click here to see the raw data 👉')
with see_data:
    st.dataframe(data=df.reset_index(drop=True))
st.text('')

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
st.sidebar.markdown("**Select the cities you want to analyze**👇")
container = st.container()
all = st.sidebar.checkbox("Select all", value=True)
if all:
    selected_cities = st.sidebar.multiselect("", df["City"].unique(), df["City"].unique())
else:
    selected_cities = st.sidebar.multiselect("", df["City"].unique())

# df_selection = df.query("City == @selected_cities")
df_selection = df.loc[df['City'].isin(selected_cities)]

st.subheader('Statistics - Columns Averages')
for i, place in enumerate(st.columns(int(len(columns) / 2))):
    with place:
        st.subheader(clean_col_name(columns[i]))
        avg = round(df_selection[df_selection[columns[i]] != 0][columns[i]].mean(), 2)
        st.markdown(f"{avg:,}")
st.markdown("""---""")

for i, place in enumerate(st.columns(int(len(columns) / 2))):
    with place:
        st.subheader(clean_col_name(columns[i + 5]))
        avg = round(df_selection[df_selection[columns[i + 5]] != 0][columns[i + 5]].mean(), 2)
        st.markdown(f"{avg:,}")
st.markdown("""---""")

################
### ANALYSIS ###
################
row2_spacer1, row2_1, row2_spacer2 = st.columns((.2, 7.1, .2))
with row2_1:
    st.subheader('Analysis per City')
row3_spacer1, row3_1, row3_spacer2, row3_2 = st.columns((.2, 2.2, .4, 6))
with row3_1:
    st.markdown(
        'Investigate a variety of stats for each city. In which city is life expectancy highest? Which city has the most air pollution?')
    plot_x_per_city_selected = st.selectbox("Which lifestyle parameter do you want to analyze?", options=columns,
                                            index=0)
    title = clean_col_name(plot_x_per_city_selected)
with row2_spacer2:
    fig_product_sales = px.bar(
        df_selection,
        x="City",
        y=plot_x_per_city_selected,
        title=f'<b>{title} Per City</b>',
        color_discrete_sequence=["rgb(73,0,106)"] * len(df_selection),
        template="plotly_white",
    )
    fig_product_sales.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    avg = round(df_selection[df_selection[plot_x_per_city_selected] != 0][plot_x_per_city_selected].mean(), 2)
    fig_product_sales.add_hline(y=avg, line_dash="dot")
    st.plotly_chart(fig_product_sales, use_container_width=True)

row6_1, space6, row_6_2 = st.columns((10, 0.5, 6))
with row6_1:
    world_fig = px.scatter_geo(df, locations="iso_alpha", color="Continent",
                               hover_name="City", size=plot_x_per_city_selected,
                               projection="natural earth",
                               title=f'<b>{title} Per City & Continent Map</b>')
    world_fig.update_layout(autosize=True, margin=dict(l=10, r=10, t=30, b=30), plot_bgcolor="rgba(0,0,0,0)",
                            legend=dict(
                                y=0,
                                x=1,
                                title=''
                            ))
    st.plotly_chart(world_fig, use_container_width=True)
with row_6_2:
    st.subheader('Map Description:')
    st.markdown("In the map on the left you can see the distribution of the selected lifestyle parameter according to the countries in the world. \n The size is determined by the value in each country. The larger the values, the larger the shape size.")
st.markdown("""---""")

row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.subheader('Correlation Of Attributes')
    col1 = st.selectbox("Choose lifestyle parameter to analyze:", options=columns, index=0)
    col2 = st.selectbox("Select another lifestyle parameter to investigate the relationship:", options=columns, index=1)
    if col1 == col2:
        st.warning('Pay Attention! You Should Select Two Different Columns')
    X = df_selection[(df_selection[col1] != 0) & (df_selection[col2] != 0)]
    title1 = clean_col_name(col1)
    title2 = clean_col_name(col2)
row5_spacer1, row5_1 = st.columns((30, 30))
with row5_spacer1:
    df_corr = df_selection.corr()  # Generate correlation matrix
    fig_corr_matrix = go.Figure()
    fig_corr_matrix.add_trace(go.Heatmap(x=df_corr.columns, y=df_corr.index, z=np.array(df_corr)))
    x = clean_col_name(list(df_corr.columns), is_list=True)
    y = clean_col_name(list(df_corr.index), is_list=True)
    z = np.array(df_corr)
    fig_corr_matrix = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=np.around(z, decimals=2), hoverinfo='z',
                                                  colorscale='RdPu', showscale=True)
    fig_corr_matrix.update_layout(autosize=True, margin=dict(l=10, r=10, t=10, b=10))
    fig_corr_matrix.add_trace(
        go.Scatter(mode="markers", x=[title1], y=[title2], marker_symbol=[100], marker_color="Yellow",
                   marker_line_width=4, marker_size=40,
                   hovertemplate='x: %{x}<br>y: %{y}<br>z: Chosen Parameters <extra></extra>'))
    st.plotly_chart(fig_corr_matrix, use_container_width=True)
    fig_corr_matrix.update_layout(autosize=True, margin=dict(l=10, r=10, t=30, b=30), plot_bgcolor="rgba(0,0,0,0)")
with row5_1:
    trend_line = LinearRegression().fit(np.array(df_selection[col1]).reshape(-1, 1),
                                        np.array(df_selection[col2])).predict(
        np.array(df_selection[col1]).reshape(-1, 1))
    fig_trend = px.scatter(data_frame=df_selection, x=col1, y=col2, color="Continent")
    fig_trend.update_traces(marker_line_width=1, marker_size=12)
    fig_trend.add_trace(
        go.Scatter(x=df_selection[col1], y=trend_line, mode="lines", name="Trend Line",
                   line={'dash': 'dash', 'color': 'black'}))
    st.plotly_chart(fig_trend, use_container_width=True)
    fig_trend.update_layout(autosize=True, margin=dict(l=30, r=30, t=30, b=30), plot_bgcolor="rgba(0,0,0,0)")

st.markdown("""---""")

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
