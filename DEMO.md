# Demo Guide

Use this script when presenting the Persona-Adaptive Customer Support Agent.

## 1. Problem Statement

Customer support agents often answer very different users with the same generic tone. This project adapts support answers to three personas while grounding responses in a knowledge base.

## 2. Architecture Walkthrough

```text
User message
-> persona detection
-> ChromaDB retrieval
-> Gemini adaptive response
-> escalation engine
-> human handoff summary
-> Streamlit UI
```

## 3. Commands To Run Before Demo

```powershell
python -m pip install -r requirements.txt
python scripts\generate_support_pdf.py
python scripts\ingest_knowledge_base.py
python -m pytest
python scripts\validate_project.py
python -m streamlit run app.py
```

## 4. Demo Questions

Technical Expert:

```text
The API returns 403_FORBIDDEN for our OAuth token. Which scope or endpoint should I check?
```

Frustrated User:

```text
I am frustrated and still cannot access my account.
```

Business Executive:

```text
Give me a concise summary of business impact, risk, timeline, and owner for slow dashboards.
```

Escalation:

```text
Can you approve my refund?
```

## 5. What To Point Out

- Persona detection is explainable and shows matched signals.
- Retrieval shows source documents and confidence scores.
- Gemini response style changes by persona.
- Sensitive topics trigger escalation even when retrieval confidence is acceptable.
- Human handoff summary gives the next human agent useful context.

## 6. Expected Test Result

```text
26 passed
```

