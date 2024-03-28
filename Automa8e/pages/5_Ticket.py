from PIL import Image
import pandas as pd
import streamlit as st
import time
from utils.google_sheets import fetch_data_from_sheet

st.set_page_config(page_title="Automa8e", layout="wide", page_icon="images\page icon.png")

# Load logo
logo = Image.open("images\logo (6).png")
st.image(logo, width=250)

@st.cache_data(ttl=300)
def fetch_data():
    return fetch_data_from_sheet("Support", usecols=list(range(5)))

# Initialize a session state variable to track refresh action
if 'refresh' not in st.session_state:
    st.session_state.refresh = False

# Sidebar button for data refresh
if st.button("Refresh Data"):
    # Toggle the refresh state to True when the button is clicked
    st.session_state.refresh = not st.session_state.refresh

# Check if the refresh action is True, and if so, rerun the app
if st.session_state.refresh:
    st.experimental_memo.clear()  # Clear cached data
    st.session_state.refresh = False  # Reset the refresh state to avoid recursion
    st.experimental_rerun()  # Rerun the app to refresh data

support_data = fetch_data()

# Main body
st.title("Ticket")
st.markdown("_This database contains user requests for assistance from an agent._")

# Display the entire dataset
st.dataframe(support_data, use_container_width=True)
