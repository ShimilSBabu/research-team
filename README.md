# The Agentic Research Team

[![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.2.x-4B8BBE)](https://langchain-ai.github.io/langgraph/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.61%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

A research automation system that decomposes a user query into subtopics, gathers evidence from the web, fact-checks the output, and writes a polished research report. The project combines a LangGraph workflow, Mistral LLM calls, Tavily search, and a lightweight Streamlit frontend for interactive report generation and PDF export.

## What the project does

This repository implements an agentic research pipeline that:

- accepts a research question from a user,
- breaks the task into smaller subtopics,
- searches the web for supporting evidence,
- summarizes and verifies the findings,
- writes a structured report,
- critiques the quality of the draft and iterates as needed,
- exposes both an API and UI for end users.

The core orchestration lives in the LangGraph graph under [src/graph.py](src/graph.py), while the agent behavior and prompts are defined in [src/agents](src/agents) and [src/prompt_factory](src/prompt_factory).

## Why the project is useful

This project is useful for teams and researchers who need a fast, semi-automated way to generate evidence-backed reports from a broad topic. It reduces manual research work by coordinating specialized agents for:

- decomposition,
- retrieval,
- fact checking,
- writing,
- critique and iterative revision.

Key benefits:

- fast synthesis of research across multiple sub-questions,
- evidence-driven output grounded in web results,
- a web UI for prompt-driven report generation,
- PDF generation for downloadable research output,
- ability to expose the workflow through a REST endpoint.

## Project structure

- [main.py](main.py): FastAPI service exposing the research endpoint.
- [frontend/streamlit_app.py](frontend/streamlit_app.py): Streamlit interface for submitting topics and downloading reports.
- [frontend/helper_functions.py](frontend/helper_functions.py): PDF creation and Gmail email dispatch helpers.
- [src/graph.py](src/graph.py): LangGraph workflow definition.
- [src/agents](src/agents): specialized agent nodes for decomposition, research, fact checking, writing, and critique.
- [src/tools/web_search.py](src/tools/web_search.py): Tavily-based web search wrapper.
- [src/utils/config.py](src/utils/config.py): environment-driven runtime configuration.

## Requirements

- Python 3.14+
- Access to Mistral API keys
- Tavily API key
- Optional Gmail credentials for sending reports by email

## Getting started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd research_team
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -U pip
pip install -e .
```

The project uses the dependencies declared in [pyproject.toml](pyproject.toml).

### 4. Configure environment variables

Copy the example environment file and fill in the values you need:

```bash
copy .env.example .env
```

Then edit `.env` and provide at least:

```env
MISTRAL_API_KEY_1=""
MISTRAL_API_KEY_2=""
MISTRAL_API_KEY_3=""
TRAVILY_API_KEY=""
```

The app also expects optional email settings for the Streamlit send-email option:

```env
RECEIVER_EMAIL_ID="your-address@example.com"
GMAIL_CREDENTIALS_PATH="frontend/credentials.json"
GMAIL_TOKEN_PATH="frontend/token.json"
```

A complete example is available in [.env.example](.env.example).

### 5. Start the backend API

```bash
python main.py
```

This launches the FastAPI app and exposes the endpoint:

```text
GET /research?research_topic=your+topic+here
```

Example:

```bash
curl "http://127.0.0.1:8080/research?research_topic=What%20are%20the%20main%20benefits%20of%20agentic%20AI%3F"
```

### 6. Start the Streamlit frontend

From another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

The app opens a research topic form and lets the user:

- submit a topic,
- wait for the research workflow to complete,
- view the markdown report,
- download the PDF,
- send the PDF by email if Gmail credentials are configured.

## Usage example

### API usage

```python
import requests

response = requests.get(
    "http://127.0.0.1:8080/research",
    params={"research_topic": "Impact of agentic AI on software teams"},
    timeout=120,
)

print(response.json())
```

### UI usage

1. Open the Streamlit app.
2. Enter a research question in the text box.
3. Click Research.
4. Review the generated report and use the available download/email actions.

## Help and support

If you need support or want to learn more:

- review the project code and agent prompts in [src](src),
- check the issue tracker in GitHub,
- open a discussion or bug report in the repository,
- refer to the source documentation in [src/prompt_factory](src/prompt_factory).

For contributors, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Maintainers and contribution guidelines

This project is designed for iterative improvement of the research workflow, prompt quality, and automation quality.

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request. If you are planning a change to prompts, search behavior, orchestration, or the UI, keep the update scoped and explain the effect on the research pipeline.
