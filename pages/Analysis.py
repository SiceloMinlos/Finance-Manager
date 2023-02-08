import sqlite3, os, json, re
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(
    initial_sidebar_state="collapsed",
    page_title="Data Analysis",
    layout="wide",
)

st.markdown("<h1 style='text-align: center; color: #fff;'>Analysis</h1>",
            unsafe_allow_html=True)
st.markdown("#")

def getAnimation(filepath: str):
    """Load Lottie animation from a json file

    Args:
        filepath (str): Path to the json file

    Returns:
        dict: Lottie animation in json format
    """
    with open(filepath, "r") as f:
        return json.load(f)

@st.cache(suppress_st_warning=True)
def getDataFromFile():
    """Fetch data from an SQLite database and clean the data

    Returns:
        df (pandas.DataFrame): Cleaned data
    """
    # Connect to an SQLite database (create a new database if it doesn't exist)
    connection = sqlite3.connect("userDatabase.db")
    cursor = connection.cursor()

    cursor.execute("SELECT file_name, data FROM uploaded_files WHERE id=1")
    file = cursor.fetchone()

    extension = file[0].split(".")[1]

    if extension == 'csv':
        df = pd.read_csv(file[1])
    elif extension == 'xlsx':
        df = pd.read_excel(
            io=file[1],
            engine='openpyxl',
            sheet_name='Worksheet',
            skiprows=0,
            usecols='A:C',
            nrows=13,
        )
    else:
        st.markdown("<h1 style='text-align: center; color: #565656;'>An error occured</h1><br>"
        "<h4 style='text-align: center; color: #565656;'>Please ensure you inserted the correct file type!</h4>",
            unsafe_allow_html=True)
        st.write("Go back to [form](/)")
        st_lottie (
            getAnimation("files/error.json"), 
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height="500px",
            width=None,
            key="error"
        )
        raise ValueError("Unsupported file type.")

    # Define a function to clean the data
    def clean_data(data):
        data = data[1:]
        data = re.split(r",(?!(?:[^,\[\]]+,)*[^,\[\]]+])", data, 0)
        return int(float("".join(data[0:])))

    # Clean both the income and expenses columns
    df["Income"] = df["Income"].apply(clean_data)
    df["Expenses"] = df["Expenses"].apply(clean_data)
            
    return df

df = getDataFromFile()


def display_filters():
    """Displays the filters for the data visualization.

    Returns:
        None
    """
    st.markdown("<h4 style='text-align: left; color: #454545;'>Filters</h4>",
                unsafe_allow_html=True)

    month = st.multiselect(
        "Select Months:",
        options=df["Month"].unique(),
        default=df["Month"].unique(),

    )

    return month

month = display_filters()

filteredData = df.query(
    "Month == @month"
)

def display_data(filtered_data):
    """Displays the key data of the filtered data.

    Args:
        filtered_data (pandas.DataFrame): The filtered data from the original data.

    Returns:
        None
    """
    st.markdown("<h2 style='text-align: center; color: #fff; font-weight: bold'>Key Data</h3>",
                unsafe_allow_html=True)

    st.markdown("##")

    # Key Data
    total_yearly_income = int(filtered_data["Income"].sum())
    total_yearly_expense = int(filtered_data["Expenses"].sum())
    # best month
    filtered_data["Net_Income"] = filtered_data["Income"] - filtered_data["Expenses"]
    max_month = filtered_data.loc[filtered_data["Net_Income"].idxmax(), "Month"]

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Total Income:")
        st.subheader(f"R {total_yearly_income:,}")
    with middle_column:
        st.subheader("Total Expense:")
        st.subheader(f"R {total_yearly_expense:,}")
    with right_column:
        st.subheader("Best Month:")
        st.subheader(f"{max_month:}")

    st.markdown("---")

    monthly_figure = px.bar(
        filtered_data,
        x="Month",
        y="Net_Income",
        color_discrete_sequence=["#0083B8"] * len(filtered_data),
        title="Income by Net Income"
        )

    net_income_figure = px.bar(
        filtered_data,
        x="Month",
        y="Income",
        color_discrete_sequence=["#0083B8"] * len(filtered_data),
        title="Income by Month"
        )

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(monthly_figure, use_container_width=True)
    right_column.plotly_chart(net_income_figure, use_container_width=True)


def hide_ui_elements():
    """
    Hide the hamburger and footer of the streamlit app.
    
    Returns: None
    """
    hide_hamburger_and_footer = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_hamburger_and_footer, unsafe_allow_html=True)

if __name__ == "__main__":
    hide_ui_elements()
    display_data(filteredData)