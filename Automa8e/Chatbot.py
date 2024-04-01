from PIL import Image
import pandas as pd
import streamlit as st
import requests
import streamlit.components.v1 as components
import altair as alt
from streamlit_lottie import st_lottie
from streamlit_gsheets import GSheetsConnection
from utils.google_sheets import handle_data_refresh

st.set_page_config(page_title="Automa8e", layout = "wide", page_icon = "images\page icon.png")
  
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
<div style="width: 100%; height: 800px; margin: 0; padding: 0;" id="VG_OVERLAY_CONTAINER">
    <!-- Here is where Voiceglow renders the widget. -->
    <!-- Set render to 'full-width' then adjust the width and height to 500px (for example) to render the chatbot itself without the popup. -->
</div>

<!-- Remove 'defer' if you want widget to load faster (Will affect website loading) -->
<script defer>
    (function() {
        window.VG_CONFIG = {
            ID: "z6f8rrkg9",
            region: 'na', // 'eu' or 'na' corresponding to Europe and North America
            render: 'full-width', // Set render to 'full-width' to load chatbot automatically
            stylesheets: [
                // Base Voiceglow CSS
                "https://storage.googleapis.com/voiceglow-cdn/vg_live_build/styles.css",
                // Add your custom css stylesheets, Can also add relative URL ('/public/your-file.css)
            ],
        }
        var VG_SCRIPT = document.createElement("script");
        VG_SCRIPT.src = "https://storage.googleapis.com/voiceglow-cdn/vg_live_build/vg_bundle.js";
        document.body.appendChild(VG_SCRIPT);
    })();
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
