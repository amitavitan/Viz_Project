import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import re
from plotly.graph_objs import *
import plotly.graph_objects as go
import numpy as np
import plotly.figure_factory as ff


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

    return data


df = get_data_from_excel()
columns = list(df.columns)
columns.remove("City")
columns.remove("Rank")
columns.remove("Continent")


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
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
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
for i, place in enumerate(st.columns(int(len(columns)/2))):
    with place:
        st.subheader(clean_col_name(columns[i]))
        avg = round(df_selection[df_selection[columns[i]] != 0][columns[i]].mean(), 2)
        st.markdown(f"{avg:,}")
st.markdown("""---""")

for i, place in enumerate(st.columns(int(len(columns)/2))):
    with place:
        st.subheader(clean_col_name(columns[i+5]))
        avg = round(df_selection[df_selection[columns[i+5]] != 0][columns[i+5]].mean(), 2)
        st.markdown(f"{avg:,}")
st.markdown("""---""")


################
### ANALYSIS ###
################
row4_spacer1, row4_1, row4_spacer2 = st.columns((.2, 7.1, .2))
with row4_1:
    st.subheader('Analysis per City')
row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3 = st.columns((.2, 2.3, .4, 4.4, .2))
with row5_1:
    st.markdown('Investigate a variety of stats for each city. In which city is life expectancy highest? Which city has the most air pollution?')
    plot_x_per_city_selected = st.selectbox("Which lifestyle parameter do you want to analyze?", options=columns, index=0)
    title = clean_col_name(plot_x_per_city_selected)
with row5_2:
    fig_product_sales = px.bar(
        df_selection,
        x="City",
        y=plot_x_per_city_selected,
        title=f'<b>{title} Per City</b>',
        color_discrete_sequence=["#e6005c"] * len(df_selection),
        template="plotly_white",
    )
    fig_product_sales.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    avg = round(df_selection[df_selection[plot_x_per_city_selected] != 0][plot_x_per_city_selected].mean(), 2)
    fig_product_sales.add_hline(y=avg, line_dash="dot")
    st.plotly_chart(fig_product_sales, use_container_width=True)

st.markdown("""---""")

row6_spacer1, row6_1, row6_spacer2 = st.columns((.2, 7.1, .2))
with row6_1:
    st.subheader('Correlation Of Attributes')
row7_spacer1, row7_1, row7_spacer2, row7_2, row7_spacer3 = st.columns((.08, 4.1, .4, 3.5, .2))
with row7_1:
    df_corr = df_selection.corr()  # Generate correlation matrix
    fig_corr_matrix = go.Figure()
    fig_corr_matrix.add_trace(go.Heatmap(x=df_corr.columns, y=df_corr.index, z=np.array(df_corr)))
    x = clean_col_name(list(df_corr.columns), is_list=True)
    y = clean_col_name(list(df_corr.index), is_list=True)
    print(x)
    print("--------")
    print(y)
    z = np.array(df_corr)
    fig_corr_matrix = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=np.around(z, decimals=2), hoverinfo='z', colorscale='RdPu', showscale=True)
    fig_corr_matrix.update_layout(autosize=True, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_corr_matrix, use_container_width=True)
with row7_2:
    st.subheader('Correlation Of Attributes')


st.markdown("""---""")

row8_spacer1, row8_1, row8_spacer2, row8_2, row8_spacer3 = st.columns((.2, 3.5, .4, 3.5, .2))
with row8_1:
    st.subheader('Analysis per Matchday')
    selected_col1 = st.selectbox("Select lifestyle parameter do you want to analyze?", options=columns, index=0)
    selected_col2 = st.selectbox("Select another lifestyle parameter do you want to analyze?", options=columns, index=1)
    x1 = df_selection[df_selection[selected_col1] != 0].groupby('Continent')[selected_col1].agg(['mean']).reset_index("Continent")
    x2 = df_selection[df_selection[selected_col2] != 0].groupby('Continent')[selected_col2].agg(['mean']).reset_index("Continent")

    title1 = clean_col_name(selected_col1)
    title2 = clean_col_name(selected_col2)
with row8_2:
    fig_bubble = go.Figure(data=[go.Scatter(
        x=x1['Continent'],
        y=x1['mean'],
        mode='markers',
        marker=dict(
            color=x2['mean'],
            size=40,
            showscale=True,
            colorscale="RdPu",
            colorbar=dict(title=title2),
            line=dict(width=2, color='DarkSlateGrey')
        )
    )])
    fig_bubble.update_layout(
        title=f"Continent Per {title1} Per {title2}",
        xaxis_title="Continent",
        yaxis_title=title1,
        legend_title="Legend Title",
        # font=dict(
        #     family="Caliberi",
        #     size=18,
        #     color="RebeccaPurple"
        # )
    )
    st.plotly_chart(fig_bubble, use_container_width=False)



# row9_spacer1, row9_1, row9_spacer2, row9_2, row9_spacer3  = st.columns((.2, 2.3, .4, 4.4, .2))
# with row9_1:

# with row9_2:
#     if all_teams_selected != 'Select teams manually (choose below)' or selected_teams:
#         plot_x_per_matchday(plot_x_per_matchday_selected, plot_x_per_matchday_type)
#     else:
#         st.warning('Please select at least one team')


############# correlation matrix plot
# df_corr = df_selection.corr()  # Generate correlation matrix
# fig_corr_matrix = go.Figure()
# fig_corr_matrix.add_trace(
#     go.Heatmap(
#         x=df_corr.columns,
#         y=df_corr.index,
#         z=np.array(df_corr)
#     )
# )
# x = list(df_corr.columns)
# y = list(df_corr.index)
# z = np.array(df_corr)
# fig_corr_matrix = ff.create_annotated_heatmap(
#     z,
#     x=x,
#     y=y ,
#     annotation_text=np.around(z, decimals=2),
#     hoverinfo='z',
#     colorscale='RdPu',
#     showscale=True
#     )
#
#
# mid = st.columns(2)
# # left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
# mid[0].plotly_chart(fig_product_sales, use_container_width=True)
# mid[1].plotly_chart(fig_corr_matrix, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
