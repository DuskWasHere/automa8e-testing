import streamlit as st
from utils.google_sheets import fetch_data_from_sheet

def load_data_realtime(worksheet_name, usecols=None, interval_sec=30):
    """Load data from Google Sheets in quasi-real-time."""
    @st.cache_data(ttl=interval_sec)
    def _fetch_data():
        return fetch_data_from_sheet(worksheet_name, usecols)
    
    return _fetch_data()
