from PIL import Image
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from utils.google_sheets import handle_data_refresh

# Set page configuration
st.set_page_config(page_title="Automa8e", layout="wide", page_icon="images\page icon.png")

# Function to fetch data and cache it
@st.cache_data(ttl=300)
def fetch_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Feedback", usecols=list(range(2)))
    return df

# Function to fetch data and cache it
@st.cache_data(ttl=300)
def get_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="UserEngagement")
    return df

def setup_ui():
    # Use Streamlit columns to layout the logo and the title + subtitle
    col1, col2, col3 = st.columns([1, 3, 1])

    # Assuming the logo is not too wide, adjust the width as needed
    with col1:
        logo = Image.open("images/logo (6).png")
        st.image(logo, width=200)

    # Place the title and subtitle in the middle column
    with col2:
        st.markdown("""
            <h1 style='text-align: center;'>User Engagement</h1>
            <p style='text-align: center;'>This data is a collection of user engagements to gauge unanswered queries.</p>
        """, unsafe_allow_html=True)

    # The third column is used to balance the layout. No content needed.
setup_ui()

handle_data_refresh()

# Fetch data
engage = fetch_data()
fil = ["Question", "Answer Quality"]
kb = get_data()
filtered = ["Question", "Main ", "Sub"]

container = st.container()
left_col, right_col = container.columns(2)

with left_col:
    # Unanswered User Queries
    st.subheader("Unanswered User Queries")
    df_unanswered = engage[engage["Answer Quality"] == "Needs Fixing"][fil]
    st.dataframe(df_unanswered, use_container_width=True)

with right_col:
    # Answered User Queries
    st.subheader("Answered User Queries")
    df_answered = engage[engage["Answer Quality"] == "Answered"][fil]
    st.dataframe(df_answered, use_container_width=True)


# Displaying all columns from "UserEngagement" sheet
st.subheader("Helpsite Knowledge Base")
df_kb = kb[filtered]
st.dataframe(df_kb, use_container_width=True)

