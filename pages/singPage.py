import streamlit as st
from db import sing

with st.form("my_form"):
    id = st.text_input("id")
    password=st.text_input("password")

    # Every form must have a submit button.
    submitted = st.form_submit_button("회원가입")
    if submitted:
        sing(id,password)