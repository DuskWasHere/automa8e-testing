from PIL import Image
import pandas as pd
import streamlit as st
import requests
import streamlit.components.v1 as components
import altair as alt
from streamlit_lottie import st_lottie
from streamlit_gsheets import GSheetsConnection
from utils.google_sheets import handle_data_refresh
from utils.google_sheets import handle_data_refresh

st.set_page_config(page_title="Automa8e", layout = "wide", page_icon = "images\page icon.png")

# logo
logo = Image.open("images\logo (6).png")
st.image(logo, width=250)

# Function to fetch data and cache it
@st.cache_data(ttl=300)
def fetch_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    data = conn.read(worksheet="Support")
    return data
  
handle_data_refresh()

# animation
def load_anim(url):
  r = requests.get(url)
  if r.status_code != 200:
    return None
  return r.json()

anim = load_anim("https://lottie.host/81a6ce70-e829-4023-8394-4c659bafe651/HWw7G2Fq9p.json")
 
# chatbot embedding 
def embed_chatbot():
    components.html("""
<script type="text/javascript">
  (function(d, t) {
    var v = d.createElement(t), s = d.getElementsByTagName(t)[0];
    v.onload = function() {
      window.voiceflow.chat.load({
        verify: { projectID: '65f8348ce18439e83b8f6611' },
        url: 'https://general-runtime.voiceflow.com',
        versionID: 'production'
      }).then(() => {
        window.voiceflow.chat.open();
      });
    };
    v.src = "https://cdn.voiceflow.com/widget/bundle.mjs"; v.type = "text/javascript"; s.parentNode.insertBefore(v, s);
  })(document, 'script');
</script>
""", height=800)


# main body
with st.container():
  left_column, right_column = st.columns(2)
  with left_column:
    st_lottie(anim, speed=1, height=500, width=500, key="automa8e")

  with right_column:
    def main():
        embed_chatbot()

    if __name__ == "__main__":
        main()
