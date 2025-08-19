# Systematic Review Agent (Streamlit + OpenAI)

Analyze scientific articles (PDF or pasted text) and extract a complete structured evidence report,
covering Study Information, Patient Demographics, Interventions, Outcomes, Diagnostics/Imaging,
Clinical Features, Methodological Quality (bias), and evidence frameworks (GRADE, PICO, PRISMA, Cochrane).

## Features
- Streamlit UI (upload PDF or paste text)
- OpenAI Responses API with strict JSON Schema output
- Markdown report + JSON download
- Handles unknown/missing data gracefully

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt

# set your key
export OPENAI_API_KEY=sk-...
# on Windows PowerShell: $env:OPENAI_API_KEY='sk-...'

# (optional) choose model
export OPENAI_MODEL=gpt-4.1-mini
- gpt-4.1-min -> good and less cost

streamlit run app.py
```

Then open the local URL that Streamlit prints (e.g., http://localhost:8501).


### Notes
- Keep your API key secret.
- You can make an API KEY at: https://platform.openai.com/ (You'll pay for tokens)
- Large PDFs: reading text from PDFs can be imperfect; consider uploading the full text or improving
  the parser (e.g., `pymupdf`).
- Costs: choose smaller models like `gpt-4.1-mini` for cheaper runs.
- Any doubts? fernando.freua@hc.fm.usp.br

---

Developed by **Dr Fernando Freua**. 
AI Prompt by **Dr Thiago Guimarães**. 
Copyright 2025.
