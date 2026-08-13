import streamlit as st
import requests, os
from dotenv import load_dotenv

from helper_functions import markdown_to_pdf, send_pdf_email

load_dotenv()

host="http://127.0.0.1"
port="8080"
response_flag=False
markdown_flag=False

st.title("The Agentic Research Team")
if "show_markdown" not in st.session_state:
    st.session_state.show_markdown = False
if "show_buttons" not in st.session_state:
    st.session_state.show_buttons = False
if "markdown_text" not in st.session_state:
    st.session_state.markdown_text = False
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = False

user_input=st.text_input(label="Research Topic:", placeholder="What do you want to research?")

if st.button(label="Research", width="stretch", type="primary"):
    st.session_state.show_buttons = False
    st.session_state.show_markdown = False

    response=requests.get(
        url=f"{host}:{port}/research?research_topic={user_input}"
    )
    st.session_state.show_buttons = True
    st.session_state.markdown_text=(response.json()["content"])
    pdf_bytes = markdown_to_pdf(st.session_state.markdown_text)
    st.session_state.pdf_bytes=pdf_bytes
    
if st.session_state.show_buttons:
    column_1, column_2, column_3=st.columns(3)

    with column_1:
        st.download_button(
            label="Download Research Report",
            data=st.session_state.pdf_bytes,
            file_name="Research Report.pdf",
            mime="application/pdf",
            width="stretch")

    with column_2:
        if st.button(label="Display Research Report", width="stretch"):
            st.session_state.show_markdown = not st.session_state.show_markdown

    with column_3:
        if st.button(label="Send Email", width="stretch"):
            message_id=send_pdf_email(
                    pdf_bytes=st.session_state.pdf_bytes,
                    recipient=os.getenv("RECEIVER_EMAIL_ID"),
                    subject="Research Report",
                    body="Please find your report attached.",
                    filename="research_report.pdf",
                )   
            
    if st.session_state.show_markdown:
        st.markdown(st.session_state.markdown_text)