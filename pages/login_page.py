import streamlit as st
from db import login

with st.form("my_form"):
    id = st.text_input("id")
    password=st.text_input("password")

    # Every form must have a submit button.
    submitted = st.form_submit_button("로그인")
    if submitted:
        user_dict=login(id,password)
        if 'id' not in st.session_state:
            st.session_state['id'] = user_dict['id']
