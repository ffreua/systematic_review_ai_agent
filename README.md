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
export OPENAI_API_KEY=sk-...   # on Windows PowerShell: $env:OPENAI_API_KEY='sk-...'

# (optional) choose model
export OPENAI_MODEL=gpt-4.1-mini

streamlit run app.py
```

Then open the local URL that Streamlit prints (e.g., http://localhost:8501).

## Deploy (free options)

### 1) Streamlit Community Cloud (free)
1. Push this folder to a **public GitHub repo**.
2. Go to https://streamlit.io/cloud and sign in.
3. "New app" → pick your repo → set **Main file** = `app.py`.
4. In **Advanced settings → Secrets**, paste:
   ```
   OPENAI_API_KEY = "sk-..."
   OPENAI_MODEL = "gpt-4.1-mini"
   ```
5. Deploy. Share the URL with others.

### 2) Hugging Face Spaces (Streamlit)
1. Create a new **Space** → SDK = **Streamlit**.
2. Upload all files from this project (or link your Git repo).
3. In **Settings → Secrets**, add `OPENAI_API_KEY`.
4. The Space will build and run automatically.

### Notes
- Keep your API key secret. Never hardcode it.
- Large PDFs: reading text from PDFs can be imperfect; consider uploading the full text or improving
  the parser (e.g., `pymupdf`).
- Costs: choose smaller models like `gpt-4.1-mini` for cheaper runs.

---

Developed by **Dr Fernando Freua**. Copyright 2025.
