import streamlit as st
from streamlit_gsheets import GSheetsConnection

@st.cache_data
def get_gsheets_conn():
    """Get a Google Sheets connection using Streamlit's connection API."""
    return st.connection("gsheets", type=GSheetsConnection)

def fetch_data_from_sheet(worksheet_name, usecols=None):
    """Fetch data from a specific Google Sheet worksheet."""
    conn = get_gsheets_conn()
    if usecols:
        return conn.read(worksheet=worksheet_name, usecols=usecols)
    return conn.read(worksheet=worksheet_name)
    pass