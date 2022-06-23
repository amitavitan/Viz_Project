import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
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

df_selection = df.query("City == @city")

# ---- MAINPAGE ----
st.title(":bar_chart: Healthy Lifestyle Dashboard")
st.markdown("##")

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

col_chart = st.selectbox(
    "Select Column For Graphs:",
    options=columns,
    index=0,
)
print(col_chart)

# bar plot
fig_product_sales = px.bar(
    df_selection,
    x="City",
    y=col_chart,
    # orientation="h",
    title=f"<b>{col_chart} Per City</b>",
    color_discrete_sequence=["#0083B8"] * len(df_selection),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# correlation matrix plot
df_corr = df_selection.corr()  # Generate correlation matrix
fig_corr_matrix = go.Figure()
fig_corr_matrix.add_trace(
    go.Heatmap(
        x=df_corr.columns,
        y=df_corr.index,
        z=np.array(df_corr)
    )
)
x = list(df_corr.columns)
y = list(df_corr.index)
z = np.array(df_corr)
fig_corr_matrix = ff.create_annotated_heatmap(
    z,
    x=x,
    y=y ,
    annotation_text=np.around(z, decimals=2),
    hoverinfo='z',
    colorscale='RdPu',
    showscale=True
    )


mid = st.columns(2)
# left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
mid[0].plotly_chart(fig_product_sales, use_container_width=True)
mid[1].plotly_chart(fig_corr_matrix, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            body {
            background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
            background-size: cover;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
