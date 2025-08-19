import io
from typing import Dict, Any, List
from pypdf import PdfReader

def extract_text_from_pdf(uploaded_file) -> str:
    # uploaded_file is a BytesIO coming from Streamlit
    reader = PdfReader(uploaded_file)
    texts = []
    for page in reader.pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            pass
    return "\n".join(texts).strip()

def chunk_text(text: str, max_chars: int = 150_000) -> str:
    # Simple truncation for very long texts to avoid hitting context limits
    if len(text) > max_chars:
        return text[:max_chars]
    return text

def build_system_prompt(force_english: bool = True, allow_unknown: bool = True) -> str:
    base = """You are an expert in systematic reviews. Extract every requested field in a strictly structured JSON format.
- Use established evidence frameworks (GRADE, PICO, PRISMA, Cochrane risk of bias) when applicable.
- If the article does not report a field, {unknown_rule}.
- Be precise and concise. Do not invent data.
- Prefer quantitative values when available (effect sizes, confidence intervals, p-values).
- Keep units.
- Cite details exactly as written in the article when relevant.
- The final answer MUST be valid JSON and match the provided schema exactly.
"""
    unknown_rule = "write 'unknown'" if allow_unknown else "leave it blank"
    lang = "All output must be in English." if force_english else "Output language should follow the input."
    return base.format(unknown_rule=unknown_rule) + "\n" + lang

def build_user_prompt(article_text: str) -> str:
    # The user prompt contains the article text
    return f"""Analyze the following scientific article and extract the information according to the schema.

---BEGIN ARTICLE TEXT---
{article_text}
---END ARTICLE TEXT---
"""

def render_markdown_report(data: Dict[str, Any]) -> str:
    # Convert the structured dict into a readable markdown report
    def g(d: Dict[str, Any], key: str, default: str = "—"):
        v = d.get(key)
        return v if (isinstance(v, str) and v.strip()) else (str(v) if v is not None else default)

    si = data.get("study_information", {})
    pd = data.get("patient_demographics", {})
    idur = data.get("intervention_and_duration", {})
    outc = data.get("outcomes", {})
    tests = data.get("diagnostic_and_imaging_tests", {})
    clin = data.get("clinical_features", {})
    qual = data.get("methodological_quality", {})
    frameworks = data.get("evidence_frameworks", {})
    summary = data.get("study_summary", "—")

    md = f"""# Study Extraction

## Study Information
- **Study (author, year):** {g(si, "study")}
- **Design:** {g(si, "design")}
- **Number of patients:** {g(si, "number_of_patients")}
- **Number of controls:** {g(si, "number_of_controls")}
- **Country:** {g(si, "country")}

## Patient Demographics
- **Current age:** {g(pd, "current_age")}
- **Age at onset:** {g(pd, "age_at_onset")}
- **Age at treatment initiation:** {g(pd, "age_at_treatment_initiation")}
- **Sex:** {g(pd, "sex")}
- **Family History:** {g(pd, "family_history")}
- **Parental consanguinity:** {g(pd, "parental_consanguinity")}

## Intervention and Duration
- **Intervention:** {g(idur, "intervention")}
- **Duration / Replacement time:** {g(idur, "duration_or_replacement_time")}

## Outcomes
- **Motor outcome:** {g(outc, "motor_outcome")}
- **Primary outcome?:** {g(outc, "is_primary_outcome")}
- **Result (magnitude, significance):** {g(outc, "result_magnitude_significance")}

## Diagnostic and Imaging Tests
- **Molecular:** {g(tests, "molecular")}
- **Specific Biochemical test:** {g(tests, "specific_biochemical_test")}
- **Biochemical test after treatment:** {g(tests, "biochemical_test_after_treatment")}
- **General relevant blood test:** {g(tests, "general_relevant_blood_test")}
- **Brain CT:** {g(tests, "brain_ct")}
- **Brain MRI:** {g(tests, "brain_mri")}
- **Spinal MRI:** {g(tests, "spinal_mri")}
- **Electroneuromyography:** {g(tests, "electroneuromyography")}
- **Electroencephalogram:** {g(tests, "electroencephalogram")}

## Clinical Features
- **Developmental History:** {g(clin, "developmental_history")}
- **Cognitive Impairment:** {g(clin, "cognitive_impairment")}
- **Neuropsychiatric:** {g(clin, "neuropsychiatric")}
- **Epileptic Seizures:** {g(clin, "epileptic_seizures")}
- **Movement Disorders:** {g(clin, "movement_disorders")}
- **Cerebellar Ataxia:** {g(clin, "cerebellar_ataxia")}
- **Sensory Ataxia:** {g(clin, "sensory_ataxia")}
- **Muscle Strength:** {g(clin, "muscle_strength")}
- **Pyramidal Signs:** {g(clin, "pyramidal_signs")}
- **Sensory Symptoms:** {g(clin, "sensory_symptoms")}
- **Static Balance:** {g(clin, "static_balance")}
- **Gait:** {g(clin, "gait")}
- **Wheelchair-Bound:** {g(clin, "wheelchair_bound")}
- **Visual Disturbances:** {g(clin, "visual_disturbances")}
- **Hearing Impairment:** {g(clin, "hearing_impairment")}
- **Eye Movements:** {g(clin, "eye_movements")}
- **Dysarthria:** {g(clin, "dysarthria")}
- **Vertigo:** {g(clin, "vertigo")}
- **OVR:** {g(clin, "ovr")}
- **Dysphagia:** {g(clin, "dysphagia")}
- **Skin:** {g(clin, "skin")}
- **Gastrointestinal:** {g(clin, "gastrointestinal")}
- **Endocrinological:** {g(clin, "endocrinological")}
- **Cardiac:** {g(clin, "cardiac")}
- **Genitourinary:** {g(clin, "genitourinary")}
- **Orthopedic:** {g(clin, "orthopedic")}
- **Other important information:** {g(clin, "other_important_information")}

## Methodological Quality
- **Adherence to protocol?:** {g(qual, "adherence_to_protocol")}
- **ITT analysis?:** {g(qual, "itt_analysis")}
- **Missing patient data (>10–20%)?:** {g(qual, "missing_patient_data_over_10_20_percent")}
- **Randomization bias:** {g(qual, "randomization_bias")}
- **Protocol deviations:** {g(qual, "protocol_deviations")}
- **Missing outcomes:** {g(qual, "missing_outcomes")}
- **Measurement bias:** {g(qual, "measurement_bias")}
- **Selective reporting:** {g(qual, "selective_reporting_of_outcomes")}
- **Representative population?:** {g(qual, "representative_population")}
- **Representative intervention?:** {g(qual, "representative_intervention")}
- **Representative outcomes?:** {g(qual, "representative_outcomes")}
- **Conflicts of interest?:** {g(qual, "conflicts_of_interest")}
- **Risk of bias & limitations:** {g(qual, "risk_of_bias_and_limitations")}
- **Indirect evidence:** {g(qual, "indirect_evidence")}
- **Publication bias:** {g(qual, "publication_bias")}
- **Other considerations:** {g(qual, "other_considerations")}

## Evidence Frameworks
- **GRADE system:** {g(frameworks, "grade_system")}
- **PICO:** {g(frameworks, "pico")}
- **PRISMA (flow/criteria):** {g(frameworks, "prisma_flow_or_criteria")}
- **Cochrane Risk of Bias:** {g(frameworks, "cochrane_risk_of_bias")}

## Study Summary
{summary}
"""
    return md
