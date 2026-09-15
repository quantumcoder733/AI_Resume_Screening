"""Optional natural-language feedback for an existing screening result."""

import os
from pathlib import Path

from dotenv import load_dotenv

try:
    from google import genai
except ImportError:  # Keep normal screening usable before dependencies are installed.
    genai = None


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv()
load_dotenv(PROJECT_ROOT / "key.env")

GEMINI_API_KEY_ENV = "GEMINI_API_KEY"
GEMINI_MODEL = "gemini-3.6-flash"
MISSING_API_KEY_MESSAGE = "Gemini API key is not configured."
API_FAILURE_MESSAGE = "AI feedback is temporarily unavailable. The screening result is still valid."


def generate_candidate_feedback(
    candidate_result: dict,
    job_description: str = "",
) -> str:
    """Explain an existing screening result with optional Gemini feedback.

    The model receives already-calculated values and does not calculate scores,
    rank candidates, or infer skills that are not supplied here.
    """
    api_key = os.getenv(GEMINI_API_KEY_ENV)
    if not api_key:
        return MISSING_API_KEY_MESSAGE

    if genai is None:
        return API_FAILURE_MESSAGE

    prompt = _build_feedback_prompt(candidate_result, job_description)

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        feedback = response.text
        if not isinstance(feedback, str) or not feedback.strip():
            return API_FAILURE_MESSAGE
        return feedback.strip()
    except Exception:
        return API_FAILURE_MESSAGE


def _build_feedback_prompt(candidate_result: dict, job_description: str) -> str:
    """Build a prompt from values already produced by the screening pipeline."""
    candidate_name = candidate_result.get(
        "filename",
        candidate_result.get("candidate", "Unknown candidate"),
    )
    matched_skills = ", ".join(candidate_result.get("matched_skills", [])) or "None supplied"
    missing_skills = ", ".join(candidate_result.get("missing_skills", [])) or "None supplied"

    return f"""
Explain this existing resume-screening result in concise, professional language.

Use only the supplied fields below. Do not calculate or change any score. Do not
rank the candidate. Do not invent skills, experience, achievements, or facts.
Clearly label the response with:
1. Candidate strengths
2. Important matched skills
3. Missing or relevant skills
4. Brief explanation of the screening result
5. Practical resume improvement suggestions based only on the supplied fields

Candidate: {candidate_name}
Matched skills: {matched_skills}
Missing skills: {missing_skills}
Resume similarity score: {candidate_result.get("resume_similarity", "Not supplied")}%
Skill-match score: {candidate_result.get("skill_match", "Not supplied")}%
Overall screening score: {candidate_result.get("overall_score", "Not supplied")}%
Job description, if supplied: {job_description or "Not supplied"}
""".strip()
