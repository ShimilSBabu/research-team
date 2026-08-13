import streamlit as st
import requests

host="http://127.0.0.1"
port="8080"

st.title("The Agentic Research Team")

user_input=st.text_input(label="Research Topic:", placeholder="What do you want to research?")
if st.button(label="Research", width="stretch", type="primary"):
    response=requests.get(
        url=f"{host}:{port}/research?research_topic={user_input}"
    )
    st.markdown(response.json()["content"])