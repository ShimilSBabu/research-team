from frontend_utils import logging_config
from frontend_utils.helper_functions import markdown_to_pdf, send_pdf_email
from frontend_utils.config import BACKEND_ENDPOINT, RECEIVER_EMAIL_ID

import streamlit as st
import websocket
import json
from logging import getLogger

logger=getLogger(__name__)

logger.info(msg="Streamlit launching.")
st.title("The Agentic Research Team")
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_markdown" not in st.session_state:
    st.session_state.show_markdown = True
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
    logger.info(msg="Contacting backend.")
    placeholder = st.empty()

    ws = websocket.create_connection(
        f"ws://{BACKEND_ENDPOINT}/research"
    )
    ws.send(user_input)

    while True:
        raw = ws.recv()
        if raw:
            data = json.loads(raw)
            logger.info(msg=f"Data received  ({type(data)}): {data}")
            if data.get("type") == "Done":
                logger.info(msg="Finished receiving results. Disconnecting connection.")
                break
            if data.get("type") == "error":
                st.error(data["message"])
                logger.info(msg="Error receiving results. Disconnecting connection.")
                break
            for node, text in data.items():
                logger.info(msg=f"Processing data received from backend.")
                if text:
                    if not st.session_state.show_markdown:
                        st.session_state.show_markdown = True
                    st.session_state.markdown_text=text
                if st.session_state.show_markdown:
                    placeholder.markdown(text)
    logger.info(msg="Clossing WebSocket connection.")
    ws.close()
    placeholder.markdown("")

    logger.info(msg="Response received from backend.")
    st.session_state.show_buttons = True
    logger.info(msg=f"Generating the PDF from markdown.\n{st.session_state.markdown_text}")
    pdf_bytes = markdown_to_pdf(st.session_state.markdown_text)
    logger.info(msg="PDF Generated.")
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
            logger.info(msg="Switching the markdown display configuration.")

    with column_3:
        if st.button(label="Send Email", width="stretch"):
            logger.info(msg="Sending email.")
            try:
                message_id=send_pdf_email(
                        pdf_bytes=st.session_state.pdf_bytes,
                        recipient=RECEIVER_EMAIL_ID,
                        subject="Research Report",
                        body="Please find your report attached.",
                        filename="research_report.pdf",
                    )   
                logger.info(msg="Email sent successfully.")
            except:
                logger.exception(msg="Failed to send email.")
            
placeholder = st.empty()

if st.session_state.show_markdown:
    if st.session_state.markdown_text:
        logger.info(msg="Displaying markdown.")
        placeholder.markdown(st.session_state.markdown_text)
else:
    logger.info(msg="Hiding markdown.")
    placeholder.markdown("")