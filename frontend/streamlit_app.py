from frontend_utils import logging_config
from frontend_utils.helper_functions import markdown_to_pdf, send_pdf_email
from frontend_utils.config import BACKEND_ENDPOINT, RECEIVER_EMAIL_ID

import streamlit as st
import requests
from logging import getLogger

logger=getLogger(__name__)

logger.info(msg="Streamlit launching.")
st.title("The Agentic Research Team")
if "show_markdown" not in st.session_state:
    st.session_state.show_markdown = False
if "show_buttons" not in st.session_state:
    st.session_state.show_buttons = False
if "markdown_text" not in st.session_state:
    st.session_state.markdown_text = False
if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = False

# # # Test version
# logger.info(msg="Loading test configuration.")
# st.session_state.show_buttons = True
# st.session_state.markdown_text = """- **Overreliance on Industry Reports and Blogs**: While the report cites a range of sources, many of them are industry blogs or reports (e.g., Tredence, AIMultiple, DruidAI) rather than peer-reviewed academic research. This reliance on non-academic sources weakens the report's credibility. The report should incorporate more peer-reviewed studies or independent analyses to balance the narrative.

# - **Lack of Technical Depth**: The report provides a high-level overview of Agentic AI but lacks technical details on how these systems work. For example:
#   - The discussion of LLMs as cognitive cores (Section 2) does not delve into the limitations of current LLM architectures, such as their inability to reason beyond statistical patterns or their susceptibility to adversarial attacks.
#   - The challenges section (Section 6) mentions scalability and interoperability but does not provide concrete examples of how these issues manifest in real-world deployments.

# - **Unsupported Leaps in Reasoning**:
#   - The report assumes that the adoption of Agentic AI will lead to seamless integration with existing systems without addressing the technical and organizational barriers to adoption. For example, the claim that "Agentic AI is transforming healthcare" (Section 5.1) is not supported by a detailed analysis of how these systems are being integrated into existing healthcare workflows or the resistance they may face from healthcare professionals.

# - **Inconsistencies in Citations**: Some citations are outdated or irrelevant. For example, the IBM citation on ethics and governance (Section 2.2) is from 2024, which may not reflect the latest developments in the field. The report should prioritize more recent and relevant sources.
# critic_response["content"].critic_score (<class 'float'>): 0.65"""
# st.session_state.pdf_bytes = markdown_to_pdf(st.session_state.markdown_text)

user_input=st.text_input(label="Research Topic:", placeholder="What do you want to research?")

if st.button(label="Research", width="stretch", type="primary"):
    st.session_state.show_buttons = False
    st.session_state.show_markdown = False
    logger.info(msg="Contacting backend.")
    response=requests.get(
        url=f"{BACKEND_ENDPOINT}research?research_topic={user_input}"
    )
    if response.status_code==200:
        logger.info(msg="Response received from backend.")
        st.session_state.show_buttons = True
        st.session_state.markdown_text=response.json()["content"]
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
            
    if st.session_state.show_markdown:
        st.markdown(st.session_state.markdown_text)