from PIL import Image
import pandas as pd
import streamlit as st
import altair as alt
import time
from utils.google_sheets import fetch_data_from_sheet

# Set page configuration
st.set_page_config(page_title="Automa8e", layout="wide", page_icon="images\page icon.png")

# Load logo
logo = Image.open("images\logo (6).png")

# Main body
st.image(logo, width=250)
st.title("User Review")
st.markdown("_This data is a collection of user testimonials with their sentiments on the product._")

# Define function to fetch data from Google Sheets
@st.cache_data(ttl=300)
def fetch_data():
    return fetch_data_from_sheet("Review", usecols=list(range(4)))

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

# Fetch data
review = fetch_data()

# Filter Data
positive_kb = review[review['Sub'] == 'Positive']
negative_kb = review[review['Sub'] == 'Negative']

# Define all subcategories you want to display
positive_subcategories = [
    "Satisfaction", "Delight", "Excitement", "Appreciation"
]

negative_subcategories = [
    "Anger", "Frustration", "Confusion", "Disappointment"
]

# Group by 'Sub' column and count occurrences, ensuring all subcategories are present
positive_category_counts = positive_kb['Main'].value_counts().reindex(positive_subcategories, fill_value=0)
negative_category_counts = negative_kb['Main'].value_counts().reindex(negative_subcategories, fill_value=0)

# Convert to DataFrame for plotting
df_positive_category_counts = pd.DataFrame(positive_category_counts).reset_index()
df_positive_category_counts.columns = ['Main', 'Count']

df_negative_category_counts = pd.DataFrame(negative_category_counts).reset_index()
df_negative_category_counts.columns = ['Main', 'Count']

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
    positive = alt.Chart(df_positive_category_counts).mark_bar().encode(
        x='Main',
        y='Count'
    )
    st.altair_chart(positive, use_container_width=True)

    # Bar chart for negative reviews
    st.subheader("Negative Reviews")
    negative = alt.Chart(df_negative_category_counts).mark_bar().encode(
        x='Main',
        y='Count'
    )
    st.altair_chart(negative, use_container_width=True)
