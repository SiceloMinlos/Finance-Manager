import streamlit as st
import sqlite3

st.set_page_config(initial_sidebar_state="collapsed")

# Use streamlit to display a header in the web app
st.markdown("<h1 style='text-align: center; color: #fff;'>Let's get you started</h1>",
            unsafe_allow_html=True)

# Use streamlit to display a form in the web app
form = """
  <form action="/" class="form">

    <input type="text" id="fname" name="firstname" placeholder="Your name">

    <input type="text" id="lname" name="lastname" placeholder="Your last name..">

    <button type="submit">Submit</button>

  </form>
"""
st.markdown(form, unsafe_allow_html=True)

# Connect to an SQLite database (create a new database if it doesn't exist)
connection = sqlite3.connect("userDatabase.db")
cursor = connection.cursor()

# Create a table to store the uploaded files (if it doesn't exist)
cursor.execute("""
CREATE TABLE IF NOT EXISTS uploaded_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    data BLOB
)
""")

# Use streamlit to allow file uploads
uploaded_files = st.file_uploader("Choose a CSV/XLMS file", accept_multiple_files=True)

# Keep track of the ID of each file that has been uploaded
file_ids = []

# Iterate over each uploaded file
for uploaded_file in uploaded_files:
    # Read the contents of the file
    bytes_data = uploaded_file.read()
    
    # Store the file in the database
    cursor.execute("""
    INSERT INTO uploaded_files (name, data)
    VALUES (?,?)
    """, (uploaded_file.name, bytes_data))
    connection.commit()
    
    # Get the ID of the file that was just uploaded
    file_id = cursor.lastrowid
    file_ids.append(file_id)

# If the user closes the file uploader, remove the associated files from the database
if not uploaded_files:
    for file_id in file_ids:
        cursor.execute("""
        DELETE FROM uploaded_files
        WHERE id=?
        """, (file_id,))
        connection.commit()

# Close the connection to the database
connection.close()

# Use streamlit to display custom CSS
def css(css_file):
    with open(css_file) as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)

hide_hamburger_and_footer = """

    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>

"""

st.markdown(hide_hamburger_and_footer, unsafe_allow_html=True)

css("css/styles.css")
