import re
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    initial_sidebar_state="collapsed",
    page_title="Data Analysis",
    layout="wide",
)

st.markdown("<h1 style='text-align: center; color: #fff;'>Analysis</h1>",
            unsafe_allow_html=True)
st.markdown("##")

@st.cache
def getDataFromExcel():
    df = pd.read_excel(
        io='files/data.xlsx',
        engine='openpyxl',
        sheet_name='Worksheet',
        skiprows=0,
        usecols='A:C',
        nrows=13,
    )

    # Define a function to clean the data

    def clean_data(data):
        data = data[1:]
        data = re.split(r",(?!(?:[^,\[\]]+,)*[^,\[\]]+])", data, 0)
        return int(float("".join(data[0:])))


    # Clean both the income and expenses columns
    df["Income"] = df["Income"].apply(clean_data)
    df["Expenses"] = df["Expenses"].apply(clean_data)
            
    return df

df = getDataFromExcel()


st.markdown("<h4 style='text-align: left; color: #454545;'>Filters</h4>",
            unsafe_allow_html=True)

month = st.multiselect(
    "Select Months:",
    options=df["Month"].unique(),
    default=df["Month"].unique(),

)

filteredData = df.query(
    "Month == @month"
)

st.markdown("<h2 style='text-align: center; color: #fff; font-weight: bold'>Key Data</h3>",
            unsafe_allow_html=True)

st.markdown("##")

# Key Data
total_Yearly_Income = int(filteredData["Income"].sum())
total_Yearly_Expense = int(filteredData["Expenses"].sum())
# best month
filteredData["Net_Income"] = filteredData["Income"] - filteredData["Expenses"]
max_month = filteredData.loc[filteredData["Net_Income"].idxmax(), "Month"]

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Income:")
    st.subheader(f"R {total_Yearly_Income:,}")
with middle_column:
    st.subheader("Total Expense:")
    st.subheader(f"R {total_Yearly_Expense:,}")
with right_column:
    st.subheader("Best Month:")
    st.subheader(f"{max_month:}")

st.markdown("---")

monthly_figure = px.bar(
    filteredData,
    x="Month",
    y="Net_Income",
    color_discrete_sequence=["#0083B8"] * len(filteredData),
    title="Income by Net Income"
    )

net_income_figure = px.bar(
    filteredData,
    x="Month",
    y="Income",
    color_discrete_sequence=["#0083B8"] * len(filteredData),
    title="Income by Month"
    )

left_column, right_column = st.columns(2)
left_column.plotly_chart(monthly_figure, use_container_width=True)
right_column.plotly_chart(net_income_figure, use_container_width=True)

hide_hamburger_and_footer = """

    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>

"""

st.markdown(hide_hamburger_and_footer, unsafe_allow_html=True)