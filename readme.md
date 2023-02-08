
# Finance Manager

Managing your finances can be a hassle, especially when you have to deal with excel spreadsheets. This application makes it easy for you to manage your finances by taking in your excel spreadsheet file and creating simple, easy to understand graphs. With the application, you no longer have to worry about going through the hassle of reading and understanding data from an excel spreadsheet.

The application uses the Streamlit library, which provides a simple way to build web applications and run them on a localhost, without the need for extensive front-end development or hosting setup. Streamlit makes it easy to create user-friendly applications that allow users to quickly prototype and share their models and results with others.
## Installation

Before getting started, it's important to create and activate a virtual environment. This is done by running the following commands:

```bash
    python3 -m venv .venv
    source .venv/bin/activate
```

After creating the virtual environment, the following dependencies need to be installed:

```bash
    pip install streamlit
    pip install pandas
    pip install plotly
    pip install streamlit_lottie
    pip install openpyxl
```

Once the dependencies are installed, you can start the application by running the following command:

```bash
    streamlit run Form.py
```

And you're all set! The application will now be running on your localhost, ready for you to use.