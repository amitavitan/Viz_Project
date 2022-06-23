import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import chart_studio.plotly as py
from plotly.graph_objs import *

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
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


    return data


df = get_data_from_excel()
columns = list(df.columns)
columns.remove("City")
columns.remove("Rank")

st.dataframe(df)

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)
#
# col_chart = st.sidebar.multiselect(
#     "Select the Customer Type:",
#     options=df.columns,
#     default=df.columns,
# )
#
# gender = st.sidebar.multiselect(
#     "Select the Gender:",
#     options=df["Gender"].unique(),
#     default=df["Gender"].unique()
# )

df_selection = df.query("City == @city")

# ---- MAINPAGE ----
st.title(":bar_chart: Healthy Lifestyle Dashboard")
st.markdown("##")
# TOP KPI's
# avg_sunshine = round(df_selection["Sunshine hours(City)"].mean(), 3)
# average_hours_worked = round((1/365)*df_selection["Annual avg. hours worked"].mean(), 1)
# # star_rating = "☀️" * int(round(average_hours_worked, 0))
# average_bottle_cost = round(df_selection["Cost of a bottle of water(City)"].mean(), 2)

# left_column, middle_column, right_column = st.columns(3)
# with left_column:
#     st.subheader("AVG Sunshine:")
#     st.subheader(f"{avg_sunshine:,}")
# with middle_column:
#     st.subheader("Average Hours Worked Per Day:")
#     st.subheader(f"{average_hours_worked}")
# with right_column:
#     st.subheader("Average Bottle Cost:")
#     st.subheader(f"IL ₪ {average_bottle_cost}")
# st.markdown("""---""")
print(st.columns(3))

for i, place in enumerate(st.columns(int(len(columns)/2))):
    with place:
        st.subheader(columns[i])
        avg = round(df_selection[df_selection[columns[i]] != 0][columns[i]].mean(), 2)
        st.subheader(f"{avg:,}")
st.markdown("""---""")

for i, place in enumerate(st.columns(int(len(columns)/2))):
    with place:
        st.subheader(columns[i+5])
        avg = round(df_selection[df_selection[columns[i+5]] != 0][columns[i+5]].mean(), 2)
        st.subheader(f"{avg:,}")
st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
# sales_by_product_line = (
#     df.groupby(by=["Life expectancy(years) (Country)"]).sum()[["Happiness levels(Country)"]].sort_values(by="Happiness levels(Country)")
# )

fig_product_sales = px.bar(
    df_selection,
    x="City",
    y="Cost of a bottle of water(City)",
    # orientation="h",
    title=f"<b>{col_chart} Per City</b>",
    color_discrete_sequence=["#0083B8"] * len(df_selection),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
# print(fig_product_sales)

# SALES BY HOUR [BAR CHART]
# sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
# fig_hourly_sales = px.bar(
#     sales_by_hour,
#     x=sales_by_hour.index,
#     y="Total",
#     title="<b>Sales by hour</b>",
#     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
#     template="plotly_white",
# )
# fig_hourly_sales.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )

trace1 = {
  "type": "heatmap",
  "x": columns,
  "y": columns,
  "z": [
    [1.0, 0.0421226815469731, 0.031178169969044295, 0.05900702384323323, -0.409533145874167, -0.33940695612164506, 0.18670181427887142], [0.0421226815469731, 1.0, 0.11684678549417286, 0.15936121140219361, 0.16831144977024404, 0.14158363352461317, -0.03066753253934124], [0.031178169969044295, 0.11684678549417286, 1.0, 0.5936883225858387, 0.3371292154829527, 0.24951161775091865, -0.01849904265944017], [0.05900702384323323, 0.15936121140219361, 0.5936883225858387, 1.0, 0.37813903095566864, 0.2781009904663162, -0.0956039084488694], [-0.409533145874167, 0.16831144977024404, 0.3371292154829527, 0.37813903095566864, 1.0, 0.7172266582920588, -0.290106449655687], [-0.33940695612164506, 0.14158363352461317, 0.24951161775091865, 0.2781009904663162, 0.7172266582920588, 1.0, -0.28262591579580115], [0.18670181427887142, -0.03066753253934124, -0.01849904265944017, -0.0956039084488694, -0.290106449655687, -0.28262591579580115, 1.]
]}
data = [trace1]
layout = {"title": "Features Correlation Matrix"}
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
