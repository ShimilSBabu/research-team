import streamlit as st
import requests

from helper_functions import markdown_to_pdf

host="http://127.0.0.1"
port="8080"

st.title("The Agentic Research Team")

user_input=st.text_input(label="Research Topic:", placeholder="What do you want to research?")
if st.button(label="Research", width="stretch", type="primary"):
    response=requests.get(
        url=f"{host}:{port}/research?research_topic={user_input}"
    )
    markdown_text=(response.json()["content"])
    pdf_bytes = markdown_to_pdf(markdown_text)
    st.download_button(
        label="Download Research Report",
        data=pdf_bytes,
        file_name="Research Report.pdf",
        mime="application/pdf",
        width="stretch")
    st.markdown(markdown_text)