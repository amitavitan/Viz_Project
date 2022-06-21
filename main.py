import pandas as pd
import streamlit as st

# data = pd.read_csv("healthy_lifestyle_city_2021.csv")
# # preprocess
#
# # replace pounds to shekels
# data['Cost of a bottle of water(City)'] = 4.24 * (data['Cost of a bottle of water(City)'].str.replace('£', '')).astype(
#     float)
# data['Cost of a monthly gym membership(City)'] = 4.24 * (
#     data['Cost of a monthly gym membership(City)'].str.replace('£', '')).astype(float)
# # replace % to float value
# data['Obesity levels(Country)'] = 0.01 * (data['Obesity levels(Country)'].str.replace('%', '')).astype(float)


# st.write(data.columns)
# chart_data = pd.DataFrame(
#     data['City'],
#     columns=["a", "b", "c"])
# # st.bar_chart(data[['City', 'Sunshine hours(City)']])
# selected_ciry = st.radio('Pick one', list(data['City']), horizontal=True)
# if selected_ciry == 'Tel Aviv':
#     st.write('You selected Tel Aviv.')
#     st.bar_chart(data['Sunshine hours(City)'])
# else:
#     st.write("You didn't select comedy.")

# st.bar_chart(chart_data)
# @Email:  contact@pythonandvba.com
# @Website:  https://pythonandvba.com
# @YouTube:  https://youtube.com/c/CodingIsFun
# @Project:  Sales Dashboard w/ Streamlit


import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
# st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")


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
    return data


df = get_data_from_excel()
st.set_page_config(page_title='Tomi', initial_sidebar_state='expanded', layout="wide", page_icon="running")
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

df_selection = df.query(
    "City == @city"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")
print("0")
# TOP KPI's
avg_sunshine = round(df["Sunshine hours(City)"].mean(), 3)
average_hours_worked = round(df["Annual avg. hours worked"].mean(), 1)
star_rating = ":star:" * int(round(average_hours_worked, 0))
average_bottle_cost = round(df["Cost of a bottle of water(City)"].mean(), 2)
print("1")
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("AVG Sunshine:")
    st.subheader(f"{avg_sunshine:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_hours_worked} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"IL ₪ {average_bottle_cost}")
print("2")
st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
# sales_by_product_line = (
#     df.groupby(by=["Life expectancy(years) (Country)"]).sum()[["Happiness levels(Country)"]].sort_values(by="Happiness levels(Country)")
# )
fig_product_sales = px.bar(
    df_selection,
    x="City",
    y="Happiness levels(Country)",
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(df_selection),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

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

left_column, right_column = st.columns(2)
# left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
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
