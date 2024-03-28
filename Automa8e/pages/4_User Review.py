from PIL import Image
import pandas as pd
import streamlit as st
import altair as alt
from streamlit_gsheets import GSheetsConnection

# Set page configuration
st.set_page_config(page_title="Automa8e", layout="wide", page_icon="images\page icon.png")

# Load logo
logo = Image.open("images\logo (6).png")

# Define function to fetch data from Google Sheets
@st.cache_data
def fetch_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read(worksheet="Review")

# Main body
st.image(logo, width=250)
st.title("User Review")
st.markdown("_This data is a collection of user testimonials with their sentiments on the product._")

# Fetch data
review = fetch_data()

container = st.container()
left_col, right_col = container.columns(2)

with left_col:
    filtered = ["Reviews", "Sub", "Main"]

    # Positive Reviews
    st.subheader("Positive Reviews")
    df_pos = review[review["Sub"] == "Positive"][filtered]
    st.dataframe(df_pos, use_container_width=True)
    
    # Negative Reviews
    st.subheader("Negative Reviews")
    df_neg = review[review["Sub"] == "Negative"][filtered]
    st.dataframe(df_neg, use_container_width=True)

with right_col:
    # Bar chart for positive reviews
    st.subheader("Positive Reviews")
    pos_chart_data = df_pos.groupby("Main").size().reset_index(name="Count")
    pos_chart = alt.Chart(pos_chart_data).mark_bar().encode(
        x='Main',
        y='Count',
        tooltip=['Main', 'Count'],
    )
    st.altair_chart(pos_chart, use_container_width=True)
    
    # Bar chart for negative reviews
    st.subheader("Negative Reviews")
    neg_chart_data = df_neg.groupby("Main").size().reset_index(name="Count")
    neg_chart = alt.Chart(neg_chart_data).mark_bar().encode(
        x='Main',
        y='Count',
        tooltip=['Main', 'Count'],
    )
    st.altair_chart(neg_chart, use_container_width=True)