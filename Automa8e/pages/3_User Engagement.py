from PIL import Image
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Automa8e", layout="wide", page_icon="images\page icon.png")

# Load logo
logo = Image.open("images\logo (6).png")
st.image(logo, width=250)

# Define function to fetch data from Google Sheets for "Feedback" sheet
@st.cache_data()
def fetch_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Feedback", usecols=list(range(2)))
    return df

# Define function to fetch data from Google Sheets for "UserEngagement" sheet
@st.cache_data()
def get_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="UserEngagement")
    return df

# Main body
st.title("User Engagement")
st.markdown("_This data is a collection of user engagements to gauge unanswered queries._")

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

