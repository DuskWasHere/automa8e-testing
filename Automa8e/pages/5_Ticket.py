from PIL import Image
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Automa8e", layout="wide", page_icon="images\page icon.png")

# Load logo
logo = Image.open("images\logo (6).png")
st.image(logo, width=250)

# Define function to fetch data from Google Sheets
@st.cache_data()
def fetch_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Support", usecols=list(range(5)))
    return df

# Main body
st.title("Ticket")
st.markdown("_This database contains user requests for assistance from an agent._")

# Fetch data
support = fetch_data()

# Drop the 'Event Type' column
support = support.drop(columns=['Event Type'])

# Display the entire dataset
st.dataframe(support, use_container_width=True)
