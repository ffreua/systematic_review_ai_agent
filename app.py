import os
import json
from typing import Any, Dict
import streamlit as st

# OpenAI (>=1.40) new SDK
from openai import OpenAI

from models import ExtractionSchema
from utils import (
    extract_text_from_pdf,
    chunk_text,
    build_system_prompt,
    build_user_prompt,
    render_markdown_report
)

st.set_page_config(page_title="Systematic Review Agent", page_icon="📚", layout="wide")

st.title("📚 Systematic Review Agent")
st.caption("Analyze scientific articles and extract structured evidence using the OpenAI API.")

# Sidebar: configuration
st.sidebar.header("Settings")
default_model = st.sidebar.text_input("OpenAI model", value=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
api_key = st.sidebar.text_input("OPENAI_API_KEY", type="password", value=os.getenv("OPENAI_API_KEY", ""))
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
max_output_tokens = st.sidebar.number_input("Max output tokens", min_value=512, max_value=200000, value=5000, step=256)

st.sidebar.markdown("---")
st.sidebar.write("**Output options**")
download_as = st.sidebar.selectbox("Download format", ["JSON", "Markdown"])

# Input section
st.subheader("1) Provide your article")
tab_pdf, tab_text = st.tabs(["Upload PDF", "Paste text"])

article_text = ""

with tab_pdf:
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if pdf_file is not None:
        with st.spinner("Reading PDF..."):
            article_text = extract_text_from_pdf(pdf_file)

with tab_text:
    text_input = st.text_area("Paste full-text article (or abstract)", height=260, placeholder="Paste the scientific article text here...")
    if text_input:
        article_text = text_input

st.subheader("2) Run extraction")
col1, col2 = st.columns([1, 1])
with col1:
    force_english = st.checkbox("Force output in English", value=True)
with col2:
    allow_unknown = st.checkbox("Allow 'unknown' for missing fields", value=True)

run = st.button("Analyze Article", type="primary", disabled=(not api_key or not article_text))

# Main action
if run:
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)

        # Prepare text and prompts
        text_for_model = chunk_text(article_text)
        system_prompt = build_system_prompt(force_english=force_english, allow_unknown=allow_unknown)
        user_prompt = build_user_prompt(text_for_model)

        # JSON schema for strict structured output
        schema = ExtractionSchema.json_schema()

        # Call Responses API with JSON schema output (IMPORTANT: use `instructions`, not `system`)
        with st.spinner("Querying the model..."):
            response = client.responses.create(
                model=default_model,
                instructions=system_prompt,
                input=user_prompt,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "systematic_review_extraction",
                        "schema": schema,
                        "strict": True
                    }
                }
            )

        # Get structured JSON string
        content = getattr(response, "output_text", None)

        if not content:
            st.error("No structured output returned from the model.")
        else:
            try:
                data = json.loads(content)
            except Exception:
                cleaned = content.strip().strip("`")
                data = json.loads(cleaned)

            st.success("Extraction complete!")
            st.subheader("Result (structured)")
            st.json(data, expanded=False)

            st.subheader("Result (markdown report)")
            md = render_markdown_report(data)
            st.markdown(md)

            if download_as == "JSON":
                st.download_button("⬇️ Download JSON", data=json.dumps(data, indent=2), file_name="extraction.json", mime="application/json")
            else:
                st.download_button("⬇️ Download Markdown", data=md, file_name="extraction.md", mime="text/markdown")

    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.caption("Developed by Dr Fernando Freua. Copyright 2025")
