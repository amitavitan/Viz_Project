import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

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
    title="<b>Sales by Product Line</b>",
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

mid = st.columns(1)
# left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
mid.plotly_chart(fig_product_sales, use_container_width=True)
col_chart = st.columns.multiselect(
    "Select Column:",
    options=columns,
    default=columns,
)
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
