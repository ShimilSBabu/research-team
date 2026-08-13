import streamlit as st
import requests, os

from helper_functions import markdown_to_pdf, send_pdf_email

host="http://127.0.0.1"
port="8080"
response=False

st.title("The Agentic Research Team")

user_input=st.text_input(label="Research Topic:", placeholder="What do you want to research?")
if st.button(label="Research", width="stretch", type="primary"):
    response=False
    markdown_flag=False
    response=requests.get(
        url=f"{host}:{port}/research?research_topic={user_input}"
    )

if response:
    markdown_text=(response.json()["content"])
    pdf_bytes = markdown_to_pdf(markdown_text)
    column_1, column_2=st.columns(2)
    with column_1:
        st.download_button(
            label="Download Research Report",
            data=pdf_bytes,
            file_name="Research Report.pdf",
            mime="application/pdf",
            width="stretch")

    with column_2:
        if st.button(label="Display Research Report", width="stretch", type="primary"):
            if markdown_flag:
                markdown_flag=False 
            else:
                markdown_flag=True
    message_id=send_pdf_email(
        pdf_bytes=pdf_bytes,
        recipient=os.getenv("RECEIVER_EMAIL_ID"),
        subject="Research Report",
        body="Please find your report attached.",
        filename="research_report.pdf",
    )

    if markdown_flag:
        st.markdown(markdown_text)