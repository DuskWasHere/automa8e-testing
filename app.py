from PIL import Image
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Automa8e", layout = "wide")
    
pages = ["Chatbot", "General Data", "User Engagement", "User Review", "Ticket"]
logo = Image.open("logo (6).png")
resized_logo = logo.resize((200, 80), Image.LANCZOS)

engage_sheets = "https://docs.google.com/spreadsheets/d/1RlVREvEv4ibSHWHr1I0Jr_u0FiVcsPEVP4DXsdy44GM/edit?usp=sharing"
review_sheets = "https://docs.google.com/spreadsheets/d/1R7uDimwO0w6UZmKrbklgOHfueik9AEAaXPifBR6VeDI/edit?usp=sharing"

with st.sidebar:
  st.image(resized_logo)
  selected_page = st.radio("Menu", pages)
  
def embed_chatbot():
    # Embedding the chatbot using Streamlit's components
    components.html("""
<div style="width: 0; height: 0;" id="VG_OVERLAY_CONTAINER">
    <!-- Here is where Voiceglow renders the widget. -->
    <!-- Set render to 'full-width' then adjust the width and height to 500px (for example) to render the chatbot itself without the popup. -->
</div>

<!-- Remove 'defer' if you want widget to load faster (Will affect website loading) -->
<script defer>
    (function() {
        window.VG_CONFIG = {
            ID: "z6f8rrkg9",
            region: 'na', // 'eu' or 'na'corresponding to Europe and North America
            render: 'popup', // popup or full-width
            stylesheets: [
                // Base Voiceglow CSS
                "https://storage.googleapis.com/voiceglow-cdn/vg_live_build/styles.css",
                // Add your custom css stylesheets, Can also add relative URL ('/public/your-file.css)
            ],
        }
        var VG_SCRIPT = document.createElement("script");
        VG_SCRIPT.src = "https://storage.googleapis.com/voiceglow-cdn/vg_live_build/vg_bundle.js";
        document.body.appendChild(VG_SCRIPT);
    })()
</script>
""", height=500, width=500)

if selected_page == "Chatbot":
  def main():
      st.title("Automa8e Assistant")
      
      
      embed_chatbot()

  if __name__ == "__main__":
      main()
   
elif selected_page == "General Data":
  st.title("General Data")
  st.markdown("_Batman Data_")
    
elif selected_page == "User Engagement":
  st.title("User Engagement")
  st.markdown("This data is a collection of user engagements to gauge unanswered queries.")
  
  conn = st.connection("gsheets", type=GSheetsConnection)
  engage = conn.read(worksheet="Sheet1", usecols=list(range(2)))

  st.subheader("Unanswered User Queries")
  sql = '''
  SELECT
    "Question",
    "Answer Quality"
  FROM
    "Sheet1"
  WHERE
    "Answer Quality" = 'Needs Fixing'
  ORDER BY
    "Question";
  '''
  df_unanswered = conn.query(sql=sql)
  st.dataframe(df_unanswered)
  
  st.subheader("Answered User Queries")
  sql = '''
  SELECT
    "Question",
    "Answer Quality"
  FROM
    "Sheet1"
  WHERE
    "Answer Quality" = 'Answered'
  ORDER BY
    "Question";
  '''
  df_answered = conn.query(sql=sql)
  st.dataframe(df_answered)
      
elif selected_page == "User Review":
  st.title("User Review")
  st.markdown("This data is a collection of user testimonials with their sentiments on the product.")
  
  conn = st.connection("gsheets", type=GSheetsConnection)
  review = conn.read(worksheet="Reviews", usecols=list(range(4)))

  st.subheader("User Sentiment")
  sql = '''
  SELECT
    "Reviews",
    "Sentiment",
    "Sub"
  FROM
    Reviews
  WHERE
    "Sentiment" = 'Negative'
  ORDER BY
    "Reviews";
  '''
  df_sentiment = conn.query(sql=sql)
  st.dataframe(df_sentiment)

elif selected_page == "Ticket":
  st.title("Ticket")
  st.markdown("_Red Robin_")
