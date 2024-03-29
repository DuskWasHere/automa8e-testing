from PIL import Image
import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from utils.google_sheets import handle_data_refresh

# Set page configuration
st.set_page_config(page_title="Automa8e - Ticket Management", layout="wide", page_icon="images/page_icon.png")

# Function to fetch data and cache it
@st.cache_data(ttl=300)
def fetch_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(worksheet="Support")
    return data

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
            <h1 style='text-align: center;'>Ticket Management</h1>
            <p style='text-align: center;'>Manage user tickets effectively.</p>
        """, unsafe_allow_html=True)

    # The third column is used to balance the layout. No content needed.

handle_data_refresh()

def filter_populated_data(df, columns):
    """Filter the dataframe to include only rows where specified columns are all non-empty."""
    return df.dropna(subset=columns)

def main():
    setup_ui()

    # Fetch data
    support_data = fetch_data()

    # Assuming you know the positions of the desired columns, select them directly.
    selected_columns_data = support_data.iloc[:, [1, 2, 3, 4]]

    # Optionally, set the column names for the selected data for clearer representation
    selected_columns_data.columns = ['Invitee Name', 'Invitee Email', 'User Complain', 'Phone Number']

    # Filter out only rows where the desired columns are all populated
    filtered_data = filter_populated_data(selected_columns_data, ['Invitee Name', 'Invitee Email', 'User Complain', 'Phone Number'])

    # Display the filtered, selected columns
    st.dataframe(filtered_data, use_container_width=True)

if __name__ == "__main__":
    main()
