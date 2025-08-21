from typing import Any, Dict

# JSON Schema for OpenAI Structured Outputs (Chat Completions).
# Requirements:
# - additionalProperties: False at root and every object
# - required must include EVERY key in properties for each object (strict mode)
# - We'll keep everything required, and instruct the model to output "unknown" when not reported.

def ExtractionSchema() -> Dict[str, Any]:
    raise NotImplementedError("Use ExtractionSchema.json_schema()")

def _schema_dict() -> Dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "study_information": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "study": {"type": "string", "description": "Author(s) and year of publication"},
                    "design": {"type": "string"},
                    "number_of_patients": {"type": ["integer", "string"]},
                    "number_of_controls": {"type": ["integer", "string"]},
                    "country": {"type": "string"}
                },
                "required": [
                    "study",
                    "design",
                    "number_of_patients",
                    "number_of_controls",
                    "country"
                ]
            },
            "patient_demographics": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "current_age": {"type": "string"},
                    "age_at_onset": {"type": "string"},
                    "age_at_treatment_initiation": {"type": "string"},
                    "sex": {"type": "string"},
                    "family_history": {"type": "string"},
                    "parental_consanguinity": {"type": "string"}
                },
                "required": [
                    "current_age",
                    "age_at_onset",
                    "age_at_treatment_initiation",
                    "sex",
                    "family_history",
                    "parental_consanguinity"
                ]
            },
            "intervention_and_duration": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "intervention": {"type": "string"},
                    "duration_or_replacement_time": {"type": "string"}
                },
                "required": [
                    "intervention",
                    "duration_or_replacement_time"
                ]
            },
            "outcomes": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "motor_outcome": {"type": "string"},
                    "is_primary_outcome": {"type": "string"},
                    "result_magnitude_significance": {"type": "string"}
                },
                "required": [
                    "motor_outcome",
                    "is_primary_outcome",
                    "result_magnitude_significance"
                ]
            },
            "diagnostic_and_imaging_tests": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "molecular": {"type": "string"},
                    "specific_biochemical_test": {"type": "string"},
                    "biochemical_test_after_treatment": {"type": "string"},
                    "general_relevant_blood_test": {"type": "string"},
                    "brain_ct": {"type": "string"},
                    "brain_mri": {"type": "string"},
                    "spinal_mri": {"type": "string"},
                    "electroneuromyography": {"type": "string"},
                    "electroencephalogram": {"type": "string"}
                },
                "required": [
                    "molecular",
                    "specific_biochemical_test",
                    "biochemical_test_after_treatment",
                    "general_relevant_blood_test",
                    "brain_ct",
                    "brain_mri",
                    "spinal_mri",
                    "electroneuromyography",
                    "electroencephalogram"
                ]
            },
            "clinical_features": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "developmental_history": {"type": "string"},
                    "cognitive_impairment": {"type": "string"},
                    "neuropsychiatric": {"type": "string"},
                    "epileptic_seizures": {"type": "string"},
                    "movement_disorders": {"type": "string"},
                    "cerebellar_ataxia": {"type": "string"},
                    "sensory_ataxia": {"type": "string"},
                    "muscle_strength": {"type": "string"},
                    "pyramidal_signs": {"type": "string"},
                    "sensory_symptoms": {"type": "string"},
                    "static_balance": {"type": "string"},
                    "gait": {"type": "string"},
                    "wheelchair_bound": {"type": "string"},
                    "visual_disturbances": {"type": "string"},
                    "hearing_impairment": {"type": "string"},
                    "eye_movements": {"type": "string"},
                    "dysarthria": {"type": "string"},
                    "vertigo": {"type": "string"},
                    "ovr": {"type": "string"},
                    "dysphagia": {"type": "string"},
                    "skin": {"type": "string"},
                    "gastrointestinal": {"type": "string"},
                    "endocrinological": {"type": "string"},
                    "cardiac": {"type": "string"},
                    "genitourinary": {"type": "string"},
                    "orthopedic": {"type": "string"},
                    "other_important_information": {"type": "string"}
                },
                "required": [
                    "developmental_history",
                    "cognitive_impairment",
                    "neuropsychiatric",
                    "epileptic_seizures",
                    "movement_disorders",
                    "cerebellar_ataxia",
                    "sensory_ataxia",
                    "muscle_strength",
                    "pyramidal_signs",
                    "sensory_symptoms",
                    "static_balance",
                    "gait",
                    "cough",
                    "wheelchair_bound",
                    "visual_disturbances",
                    "hearing_impairment",
                    "eye_movements",
                    "dysarthria",
                    "vertigo",
                    "ovr",
                    "dysphagia",
                    "skin",
                    "gastrointestinal",
                    "endocrinological",
                    "cardiac",
                    "genitourinary",
                    "orthopedic",
                    "other_important_information"
                ]
            },
            "methodological_quality": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "adherence_to_protocol": {"type": "string"},
                    "itt_analysis": {"type": "string"},
                    "missing_patient_data_over_10_20_percent": {"type": "string"},
                    "randomization_bias": {"type": "string"},
                    "protocol_deviations": {"type": "string"},
                    "missing_outcomes": {"type": "string"},
                    "measurement_bias": {"type": "string"},
                    "selective_reporting_of_outcomes": {"type": "string"},
                    "representative_population": {"type": "string"},
                    "representative_intervention": {"type": "string"},
                    "representative_outcomes": {"type": "string"},
                    "conflicts_of_interest": {"type": "string"},
                    "risk_of_bias_and_limitations": {"type": "string"},
                    "indirect_evidence": {"type": "string"},
                    "publication_bias": {"type": "string"},
                    "other_considerations": {"type": "string"}
                },
                "required": [
                    "adherence_to_protocol",
                    "itt_analysis",
                    "missing_patient_data_over_10_20_percent",
                    "randomization_bias",
                    "protocol_deviations",
                    "missing_outcomes",
                    "measurement_bias",
                    "selective_reporting_of_outcomes",
                    "representative_population",
                    "representative_intervention",
                    "representative_outcomes",
                    "conflicts_of_interest",
                    "risk_of_bias_and_limitations",
                    "indirect_evidence",
                    "publication_bias",
                    "other_considerations"
                ]
            },
            "evidence_frameworks": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "grade_system": {"type": "string"},
                    "pico": {"type": "string"},
                    "prisma_flow_or_criteria": {"type": "string"},
                    "cochrane_risk_of_bias": {"type": "string"}
                },
                "required": [
                    "grade_system",
                    "pico",
                    "prisma_flow_or_criteria",
                    "cochrane_risk_of_bias"
                ]
            },
            "study_summary": {"type": "string"}
        },
        "required": [
            "study_information",
            "patient_demographics",
            "intervention_and_duration",
            "outcomes",
            "diagnostic_and_imaging_tests",
            "clinical_features",
            "methodological_quality",
            "evidence_frameworks",
            "study_summary"
        ]
    }

class ExtractionSchema:
    @staticmethod
    def json_schema() -> Dict[str, Any]:
        return _schema_dict()
