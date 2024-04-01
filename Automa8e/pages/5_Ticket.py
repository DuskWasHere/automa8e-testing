from PIL import Image
import pandas as pd
import streamlit as st
import altair as alt
from streamlit_gsheets import GSheetsConnection
from utils.google_sheets import handle_data_refresh

# Set page configuration
st.set_page_config(page_title="Automa8e - Ticket Management", layout="wide", page_icon="images/page_icon.png")

logo = Image.open("images/logo (6).png")
st.image(logo, width=200)

# Function to fetch data and cache it
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
            <h1 style='text-align: center;'>Ticket Management</h1>
            <p style='text-align: center;'><em>Manage user tickets effectively.</em></p>
        """, unsafe_allow_html=True)

    # The third column is used to balance the layout. No content needed.

handle_data_refresh()

def filter_populated_data(df, columns):
    """Filter the dataframe to include only rows where specified columns are all non-empty."""
    return df.dropna(subset=columns)

# Fetch data
support_data = fetch_data("Support", usecols=list(range(8)))

def main():
    setup_ui()

    # Sidebar widget for filtering by Main category
    main_categories = support_data['Main'].dropna().unique()  # Drop NaN values to avoid float issues
    main_categories = [str(category) for category in main_categories]  # Convert all categories to strings
    selected_main_category = st.sidebar.selectbox(
        'Select a Main Category:',
        ['All'] + sorted(main_categories),  # Now sorting a list of strings
        key='main_category_filter'
    )

    # Apply filter based on sidebar selection
    if selected_main_category != 'All':
        filtered_data = support_data[support_data['Main'] == selected_main_category]
    else:
        filtered_data = support_data

    # Display Ticket Management - Main Categories bar graph
    main_summary = support_data["Main"].value_counts().reset_index(name='Count')
    main_chart = alt.Chart(main_summary).mark_bar().encode(
        x=alt.X('index:N', title='Main Category'),
        y=alt.Y('Count:Q', title='Frequency'),
        color='index:N',
        tooltip=['index', 'Count']
    ).interactive().properties(title="Main Categories Distribution (Ticket)")

    # Display Ticket Management - Sub Categories bar graph
    sub_summary = support_data["Sub"].value_counts().reset_index(name='Count')
    sub_chart = alt.Chart(sub_summary).mark_bar().encode(
        x=alt.X('index:N', title='Sub Category'),
        y=alt.Y('Count:Q', title='Frequency'),
        color='index:N',
        tooltip=['index', 'Count']
    ).interactive().properties(title="Sub Categories Distribution (Ticket)")

    # Use Streamlit columns to display graphs side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ticket Management - Main Categories")
        st.altair_chart(main_chart, use_container_width=True)

    with col2:
        st.subheader("Ticket Management - Sub Categories")
        st.altair_chart(sub_chart, use_container_width=True)

    # Display the filtered DataFrame without the Event Type column
    st.subheader("Ticket Management Data")
    st.dataframe(filtered_data.drop(columns=['Event Type']), use_container_width=True)

    # Display bar graphs for each main category with x = sub category
    display_main_category_bar_charts(filtered_data)

def display_main_category_bar_charts(data):
    """Display bar graphs for each main category with x = sub category."""
    main_categories = data['Main'].dropna().unique()
    for category in main_categories:
        filtered_data = data[data['Main'] == category]
        sub_summary = filtered_data["Sub"].value_counts().reset_index(name='Count')
        sub_chart = alt.Chart(sub_summary).mark_bar().encode(
            x=alt.X('index:N', title='Sub Category'),
            y=alt.Y('Count:Q', title='Frequency'),
            color='index:N',
            tooltip=['index', 'Count']
        ).interactive().properties(title=f"{category} - Sub Categories Distribution (Ticket)")
        st.subheader(f"{category} - Sub Categories Distribution")
        st.altair_chart(sub_chart, use_container_width=True)

if __name__ == "__main__":
    main()
