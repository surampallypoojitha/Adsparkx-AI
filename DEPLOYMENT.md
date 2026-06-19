# Deployment Notes

This project is designed to run locally for internship evaluation. It can also be deployed to Streamlit Community Cloud with extra setup.

## Local Run

```powershell
python -m pip install -r requirements.txt
python scripts\generate_support_pdf.py
python scripts\ingest_knowledge_base.py
python -m streamlit run app.py
```

## Environment Variables

Required:

```text
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-2.5-flash
GEMINI_EMBEDDING_MODEL=gemini-embedding-2-preview
CHROMA_PERSIST_DIR=data/chroma
CHROMA_COLLECTION_NAME=persona_support_kb
```

## Streamlit Community Cloud

Streamlit Community Cloud deploys from a GitHub repository. The app entry point is:

```text
app.py
```

Before deployment:

1. Push the repository to GitHub.
2. Make sure `requirements.txt` is committed.
3. Add `GOOGLE_API_KEY` in Streamlit secrets.
4. Run ingestion in the deployed environment or commit a prepared knowledge base strategy.

Important: `data/chroma` is ignored by Git because it is generated local vector data. For a production-style deployment, create a startup ingestion path, use a hosted vector database, or include a controlled prebuilt vector store artifact.

## Streamlit Secrets

For local Streamlit secrets, create `.streamlit/secrets.toml` and do not commit it:

```toml
GOOGLE_API_KEY = "your_google_api_key_here"
```

This project also supports `.env`, which is simpler for local development.

