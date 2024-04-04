import streamlit as st
from streamlit_gsheets import GSheetsConnection

def handle_data_refresh():
    if 'refresh' not in st.session_state:
        st.session_state['refresh'] = False

    refresh_button = st.sidebar.button("Refresh Data")
    if refresh_button:
        st.session_state['refresh'] = True

    if st.session_state['refresh']:
        st.experimental_memo.clear()  # Clear cached data
        st.session_state['refresh'] = False  # Reset the refresh state
        st.experimental_rerun() 