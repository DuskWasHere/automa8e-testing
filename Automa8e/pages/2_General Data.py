from PIL import Image
import pandas as pd
import streamlit as st
import altair as alt
from streamlit_gsheets import GSheetsConnection
from utils.google_sheets import handle_data_refresh

# Set page configuration
st.set_page_config(page_title="Automa8e", layout="wide", page_icon="images/page_icon.png")

# Data fetching with error handling and caching
@st.cache_data(show_spinner=False)
def fetch_data(worksheet, usecols=None):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        data = conn.read(worksheet=worksheet, usecols=usecols)
        return data
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()

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
            <h1 style='text-align: center;'>General Data Insights</h1>
            <p style='text-align: center;'>Interactive visual representation of data analytics.</p>
        """, unsafe_allow_html=True)

    # The third column is used to balance the layout. No content needed.

handle_data_refresh()

def main():
    setup_ui()

    # Fetching data
    feedback_data = fetch_data("Feedback", usecols=list(range(2)))
    engagement_data = fetch_data("UserEngagement")
    # Assuming you have a way to fetch review_data
    review_data = fetch_data("Review")

    # Preparing data
    feedback_summary = feedback_data["Answer Quality"].value_counts().reset_index(name='Count')
    engagement_main_summary = engagement_data["Main "].value_counts().reset_index(name='Count')
    engagement_sub_summary = engagement_data["Sub"].value_counts().reset_index(name='Count')
    # Prepare your review data
    # Filter review_data for "Sub" being "Negative" or "Positive" and then prepare the summary
    filtered_review_summary = review_data[review_data['Sub'].isin(['Negative', 'Positive'])]

    # Group by "Main" and "Sub" to get counts
    review_summary = filtered_review_summary.groupby(['Main', 'Sub']).size().reset_index(name='Count')


    # Row 1: Feedback Summary and Positive/Negative Reviews Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Feedback Summary")
        feedback_chart = alt.Chart(feedback_summary).mark_bar().encode(
            x=alt.X('index:N', title='Answer Quality'),
            y=alt.Y('Count:Q', title='Count'),
            color='index:N',
            tooltip=['index', 'Count']
        ).interactive().properties(title="Feedback Overview")
        st.altair_chart(feedback_chart, use_container_width=True)

    with col2:
        st.subheader("Review Summary by Sentiment and Sub Categories")
        review_chart = alt.Chart(review_summary).mark_bar().encode(
            x=alt.X('Main:N', title='Sub Category'),
            y=alt.Y('Count:Q', title='Number of Reviews'),
            color=alt.Color('Sub:N', legend=alt.Legend(title="Sentiment")),
            tooltip=['Main', 'Sub', 'Count']
        ).interactive().properties(title="Reviews Overview")
        st.altair_chart(review_chart, use_container_width=True)

    # Row 2: User Engagement - Main Categories Visualization
    col1, _ = st.columns(2)
    with col1:
        st.subheader("User Engagement - Main Categories")
        main_chart = alt.Chart(engagement_main_summary).mark_bar().encode(
            x=alt.X('index:N', title='Sub Category'),
            y=alt.Y('Count:Q', title='Frequency'),
            color='index:N',
            tooltip=['index', 'Count']
        ).interactive().properties(title="Main Categories Distribution")
        st.altair_chart(main_chart, use_container_width=True)

    # Row 3: User Engagement - Sub Categories Visualization
    col1, _ = st.columns(2)
    with col1:
        st.subheader("User Engagement - Sub Categories")
        sub_chart = alt.Chart(engagement_sub_summary).mark_bar().encode(
            x=alt.X('index:N', title='Sub Category'),
            y=alt.Y('Count:Q', title='Frequency'),
            color='index:N',
            tooltip=['index', 'Count']
        ).interactive().properties(title="Sub Categories Distribution")
        st.altair_chart(sub_chart, use_container_width=True)

if __name__ == "__main__":
    main()
