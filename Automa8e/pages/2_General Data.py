from PIL import Image
import pandas as pd
import streamlit as st
import altair as alt
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Automa8e", layout="wide", page_icon="images\page icon.png")

# logo
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
st.title("General Data")
st.markdown("_Visual Representation of Data Analytics_")

# Fetch data
engage = fetch_data()
kb = get_data()

# Filter data for "Needs Fixing" and "Answered" queries
df_needs_fixing = engage[engage["Answer Quality"] == "Needs Fixing"]
df_answered = engage[engage["Answer Quality"] == "Answered"]

# Prepare data for knowledge base count
kb_main_chart_data = kb["Main "].value_counts().reset_index()
kb_main_chart_data.columns = ["Main ", "Count"]

kb_sub_chart_data = kb["Sub"].value_counts().reset_index()
kb_sub_chart_data.columns = ["Sub", "Count"]

container = st.container()
left_col, right_col = container.columns(2)

with left_col:
    # Bar chart for user queries
    st.subheader("User Queries")
    user_chart_data = pd.concat([df_needs_fixing, df_answered]).groupby("Answer Quality").size().reset_index(name="Count")
    user_chart = alt.Chart(user_chart_data).mark_bar().encode(
        x='Answer Quality',
        y='Count',
        tooltip=['Answer Quality', 'Count'],
    )
    st.altair_chart(user_chart, use_container_width=True)

with right_col:
    # Bar chart for Main column of UserEngagement
    st.subheader("User Engagement - Main")
    main_chart = alt.Chart(kb_main_chart_data).mark_bar().encode(
        x='Main ',
        y='Count',
        tooltip=['Main ', 'Count'],
    )
    st.altair_chart(main_chart, use_container_width=True)

    # Bar chart for Sub column of UserEngagement
    st.subheader("User Engagement - Sub")
    sub_chart = alt.Chart(kb_sub_chart_data).mark_bar().encode(
        x='Sub',
        y='Count',
        tooltip=['Sub', 'Count'],
    )
    st.altair_chart(sub_chart, use_container_width=True)
