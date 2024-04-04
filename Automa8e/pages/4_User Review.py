from PIL import Image
import streamlit as st
import altair as alt
from streamlit_gsheets import GSheetsConnection
from utils.google_sheets import handle_data_refresh

# Set page configuration
st.set_page_config(page_title="User Reviews - Automa8e", layout="wide", page_icon="images/page_icon.png")

logo = Image.open("images/logo (6).png")
st.image(logo, width=200)

# Function to fetch data and cache it
@st.cache_data(ttl=300)
def fetch_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(worksheet="Review")
    return data

def setup_ui():
    # Use Streamlit columns to layout the logo and the title + subtitle
    col1, col2, col3 = st.columns([1, 3, 1])

    # Assuming the logo is not too wide, adjust the width as needed
    with col1:
        st.write(" ")

    # Place the title and subtitle in the middle column
    with col2:
        st.markdown("""
            <h1 style='text-align: center;'>User Reviews - Insights</h1>
            <p style='text-align: center;'><em>Explore user sentiments and feedback on our product.</em></p>
        """, unsafe_allow_html=True)

    # The third column is used to balance the layout. No content needed.
setup_ui()

handle_data_refresh()

# Create bar charts for reviews with Altair
def create_review_chart(data, title):
    chart_data = data.groupby("Main").size().reset_index(name="Count")
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Main', sort='-y'),
        y='Count',
        color='Main',
        tooltip=['Main', 'Count'],
    ).properties(title=title, width=350)
    return chart

# Fetching data
reviews = fetch_data()

# Layout adjustments for reviews
col1, col2 = st.columns([1.1, 1])

with col1:
    st.subheader("Detailed Reviews")
    # Use of expander for detailed review visualization
    with st.expander("See Positive Reviews"):
        positive_reviews = reviews[reviews["Sub"] == "Positive"]
        st.dataframe(positive_reviews[['Reviews', 'Sub', 'Main']], height=300, width=1500)

    with st.expander("See Negative Reviews"):
        negative_reviews = reviews[reviews["Sub"] == "Negative"]
        st.dataframe(negative_reviews[['Reviews', 'Sub', 'Main']], height=300, width=1500)

# Display charts with enhanced customization
with col2:
    st.subheader("Review Analysis")
    pos_chart = create_review_chart(positive_reviews, "Positive Reviews Overview")
    neg_chart = create_review_chart(negative_reviews, "Negative Reviews Overview")

    st.altair_chart(pos_chart, use_container_width=True)
    st.altair_chart(neg_chart, use_container_width=True)