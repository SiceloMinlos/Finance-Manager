import streamlit as st
import sqlite3

st.set_page_config(initial_sidebar_state="collapsed")

# Use streamlit to display a header in the web app
st.markdown("<h1 style='text-align: center; color: #fff;'>Let's get you started</h1>",
            unsafe_allow_html=True)

# name = st.text_input("Name")
with st.form(key = 'user_info'):
    st.markdown("<h4 style='text-align: center; color: #565656;'>User Information</h4>",
      unsafe_allow_html=True)

    first_name = st.text_input(label="First_name")
    last_name = st.text_input(label="Last_name")
    uploaded_files = st.file_uploader("Choose a CSV/XLMS file", accept_multiple_files=True)

    submit_form = st.form_submit_button(label="Submit", help="Click to register!")

def check_empty_fields(submit_form, first_name, last_name, uploaded_files):
    """
    Check if all the fields are non-empty.
    
    Args:
    submit_form: bool
    first_name: str
    last_name: str
    uploaded_files: list of files
    
    Returns: None
    """
    if submit_form:
        if first_name and last_name and uploaded_files:
            st.success(f"Success {first_name}, Please navigate to [Analysis](/Analysis)", icon="🔥")
        else:
            st.warning("Please fill all the fields", icon="🚨")

def add_user_info(first_name, last_name, uploaded_files):
    """
    Connect to an SQLite database and store the uploaded files.
    
    Args:
    id: int
    first_name: str
    last_name: str
    uploaded_files: list of files
    
    Returns: None
    """
    connection = sqlite3.connect("userDatabase.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS uploaded_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        data BLOB,
        file_name
    )
    """)

    file_ids = []
  
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()

        cursor.execute("""
        SELECT id FROM uploaded_files WHERE id = 1
        """)

        result = cursor.fetchone()

        if result:
            cursor.execute("""
            UPDATE uploaded_files SET first_name = ?, last_name = ?, data = ?, file_name = ? WHERE id = 1
            """, (first_name, last_name, bytes_data, uploaded_file.name))
        else:
            cursor.execute("""
            INSERT INTO uploaded_files (first_name, last_name, data, file_name)
            VALUES (?,?,?,?)
            """, (first_name, last_name, bytes_data, uploaded_file.name))

        connection.commit()
        
    connection.close()

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
  check_empty_fields(submit_form, first_name, last_name, uploaded_files)
  add_user_info(first_name, last_name, uploaded_files)

