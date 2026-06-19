# Persona-Adaptive Customer Support Agent

An internship assignment project that builds a persona-aware customer support assistant using Python, Gemini API, LangChain, ChromaDB, Streamlit, and RAG.

## Features

- Persona detection: Technical Expert, Frustrated User, Business Executive
- Knowledge base loading for PDF, TXT, and Markdown files
- Chunking and Gemini embeddings
- Persistent ChromaDB vector storage
- Top-k retrieval with confidence scoring
- Persona-adaptive Gemini response generation
- Escalation logic for low confidence, sensitive topics, repeated failures, and missing documentation
- Human handoff summary
- Streamlit UI

## Architecture

```text
data/raw documents
-> ingestion pipeline
-> ChromaDB vector store
-> retrieval
-> persona detection
-> adaptive response generation
-> escalation decision
-> human handoff summary
-> Streamlit UI
```

## Project Structure

```text
.
├── app.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── chroma/
├── scripts/
├── src/
│   └── persona_support_agent/
├── tests/
├── DEMO.md
├── DEPLOYMENT.md
├── requirements.txt
└── README.md
```

## Setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Set `GOOGLE_API_KEY` in `.env`.

## Build The Knowledge Base

```powershell
python scripts\generate_support_pdf.py
python scripts\ingest_knowledge_base.py
```

The ingestion script loads documents from `data/raw`, chunks them, embeds them with Gemini, writes `data/processed/chunks_manifest.json`, and stores vectors in `data/chroma`.

## Run Tests

```powershell
python -m pytest
python scripts\validate_project.py
```

Expected result:

```text
26 passed
Validation passed.
```

## Run The App

```powershell
python -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Useful CLI Checks

```powershell
python scripts\detect_persona.py "The API returns 403_FORBIDDEN for our OAuth token"
python scripts\query_knowledge_base.py "How do I reset my password?"
python scripts\answer_question.py "Can you approve my refund?"
python scripts\create_handoff_summary.py "Can you approve my refund?"
```

## Demo Prompts

```text
The API returns 403_FORBIDDEN for our OAuth token. Which scope or endpoint should I check?
I am frustrated and still cannot access my account.
Give me a concise summary of business impact, risk, timeline, and owner for slow dashboards.
Can you approve my refund?
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md). For Streamlit Community Cloud, deploy `app.py`, commit `requirements.txt`, and add `GOOGLE_API_KEY` through Streamlit secrets rather than committing secrets to Git.

## Suggested Final Commit

```text
docs: finalize testing deployment and demo guide
```
