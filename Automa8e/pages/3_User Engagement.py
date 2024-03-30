from PIL import Image
import pandas as pd
import streamlit as st
import altair as alt
from streamlit_gsheets import GSheetsConnection
from utils.google_sheets import handle_data_refresh

# Set page configuration
st.set_page_config(page_title="Automa8e", layout="wide", page_icon="images\page icon.png")

logo = Image.open("images/logo (6).png")
st.image(logo, width=200)

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
        st.write(" ")

    # Place the title and subtitle in the middle column
    with col2:
        st.markdown("""
            <h1 style='text-align: center;'>User Engagement</h1>
            <p style='text-align: center;'>This data is a collection of user engagements to gauge unanswered queries.</p>
        """, unsafe_allow_html=True)

    # The third column is used to balance the layout. No content needed.
setup_ui()

handle_data_refresh()

# Display feedback overview bar chart
st.subheader("Feedback Overview")
feedback_data = fetch_data("Feedback", usecols=list(range(2)))  # Fetch feedback data
engagement_data = fetch_data("UserEngagement")

feedback_summary = feedback_data["Answer Quality"].value_counts().reset_index(name='Count')
engagement_main_summary = engagement_data["Main "].value_counts().reset_index(name='Count')
engagement_sub_summary = engagement_data["Sub"].value_counts().reset_index(name='Count')

feedback_chart = alt.Chart(feedback_summary).mark_bar().encode(
    x=alt.X('index:N', title='Answer Quality'),
    y=alt.Y('Count:Q', title='Count'),
    color='index:N',
    tooltip=['index', 'Count']
).interactive().properties(title="Feedback Overview")
st.altair_chart(feedback_chart, use_container_width=True)

# Fetch data
fil = ["Question", "Answer Quality"]
filtered = ["Question", "Main ", "Sub"]

container = st.container()
left_col, right_col = container.columns(2)

with left_col:
    # Unanswered User Queries
    st.subheader("Unanswered User Queries")
    df_unanswered = feedback_data[feedback_data["Answer Quality"] == "Needs Fixing"][fil]
    st.dataframe(df_unanswered, width=550)

with right_col:
    # Answered User Queries
    st.subheader("Answered User Queries")
    df_answered = feedback_data[feedback_data["Answer Quality"] == "Answered"][fil]
    st.dataframe(df_answered, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("User Engagement - Main Categories")
    main_chart = alt.Chart(engagement_main_summary).mark_bar().encode(
        x=alt.X('index:N', title='Sub Category'),
        y=alt.Y('Count:Q', title='Frequency'),
        color='index:N',
        tooltip=['index', 'Count']
    ).interactive().properties(title="Main Categories Distribution")
    st.altair_chart(main_chart, use_container_width=True)

with col2:
    st.subheader("User Engagement - Sub Categories")
    sub_chart = alt.Chart(engagement_sub_summary).mark_bar().encode(
        x=alt.X('index:N', title='Sub Category'),
        y=alt.Y('Count:Q', title='Frequency'),
        color='index:N',
        tooltip=['index', 'Count']
    ).interactive().properties(title="Sub Categories Distribution")
    st.altair_chart(sub_chart, use_container_width=True)
    
# Calculate total count for each main category and subcategory
total_main_category_count = engagement_main_summary['Count'].sum()
total_sub_category_count = engagement_sub_summary['Count'].sum()    

# Displaying all columns from "UserEngagement" sheet
st.subheader(f"Helpsite Knowledge Base: Total({total_main_category_count})")
df_kb = engagement_data[filtered]
st.dataframe(df_kb, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    # Display grand total for User Engagement - Main Categories
    st.subheader(f"Grand Total for User Engagement - Main Categories: Total({total_main_category_count})")
    for category, count in zip(engagement_main_summary['index'], engagement_main_summary['Count']):
        st.write(f"{category}: {count}")

with c2:
    # Display grand total for User Engagement - Sub Categories
    st.subheader(f"Grand Total for User Engagement - Sub Categories: Total({total_sub_category_count})")
    for category, count in zip(engagement_sub_summary['index'], engagement_sub_summary['Count']):
        st.write(f"{category}: {count}")
