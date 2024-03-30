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
    # Answered User Queries
    st.subheader("Answered User Queries")
    df_answered = feedback_data[feedback_data["Answer Quality"] == "Answered"][fil]
    st.dataframe(df_answered, use_container_width=True)

with right_col:
    # Unanswered User Queries
    st.subheader("Unanswered User Queries")
    df_unanswered = feedback_data[feedback_data["Answer Quality"] == "Needs Fixing"][fil]
    st.dataframe(df_unanswered, width=550)

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
    
def fetch_all_data_from_gsheets(worksheet):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # Fetch all data without specifying columns to ensure we get the entire sheet.
        data = conn.read(worksheet=worksheet)
        return data
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return pd.DataFrame()

# Fetch all data from your specific worksheet
data = fetch_all_data_from_gsheets('UserEngagement')

# Adjust here to select columns A, B, C, D based on zero-based index positions
columns_of_interest = data.iloc[:, 0:4]  # Now correctly selects columns A, B, C, D

# Renaming columns for clarity based on your latest correction
columns_of_interest.columns = ['Question', 'Response', 'Main', 'Sub']

# Filter out columns that are completely empty
columns_of_interest = columns_of_interest.dropna(axis=1, how='all')

# Sort the DataFrame based on the 'Main' column for visual grouping
columns_of_interest = columns_of_interest.dropna(subset=['Question', 'Response', 'Main', 'Sub'], how='all')

# Now, display the DataFrame with only populated rows
st.subheader("User Engagement Data")
st.dataframe(columns_of_interest, use_container_width=True)


# Filter functionality
def adjust_column_name(df, partial_name):
    for col in df.columns:
        if partial_name.lower() in col.lower():
            return col
    return partial_name  # Fallback to the original if not found

main_col_name = adjust_column_name(engagement_data, "Main")
sub_col_name = adjust_column_name(engagement_data, "Sub")

# Sidebar widget for filtering by Main category
main_categories = engagement_data[main_col_name].unique()
selected_main_category = st.sidebar.selectbox('Select a Main Category:', ['All'] + list(main_categories))

def display_filtered_data(engagement_data, selected_main_category):
    if selected_main_category != 'All':
        filtered_data = engagement_data[engagement_data[main_col_name] == selected_main_category]
    else:
        filtered_data = engagement_data

    # Group by "Main" category after filtering
    main_categories = filtered_data.groupby(main_col_name)[sub_col_name].value_counts().unstack().fillna(0)

    for main_category in main_categories.index:
        st.subheader(f"{main_category}: Total({main_categories.loc[main_category].sum()})")
        
        sub_category_data = pd.DataFrame(main_categories.loc[main_category]).reset_index()
        sub_category_data.columns = ['Sub Category', 'Count']

        sub_chart = alt.Chart(sub_category_data).mark_bar().encode(
            x='Sub Category',
            y='Count',
            color='Sub Category',
            tooltip=['Sub Category', 'Count']
        ).interactive().properties(title=f"{main_category} - Sub Categories Distribution")
        st.altair_chart(sub_chart, use_container_width=True)

# Call the function to display filtered categories and their charts
display_filtered_data(engagement_data, selected_main_category)