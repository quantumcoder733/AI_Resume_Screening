import pytest

import src.ai_feedback as ai_feedback


CANDIDATE_RESULT = {
    "filename": "candidate.pdf",
    "matched_skills": ["python", "pandas"],
    "missing_skills": ["sql"],
    "resume_similarity": 70.0,
    "skill_match": 80.0,
    "overall_score": 76.0,
}


class FakeResponse:
    text = "Strengths: Python and Pandas. Improve SQL evidence."


class FakeClient:
    last_request = None

    class Models:
        def generate_content(self, **kwargs):
            FakeClient.last_request = kwargs
            return FakeResponse()

    models = Models()


class FakeGenai:
    Client = lambda api_key: FakeClient()


def test_missing_api_key_returns_clear_status(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    result = ai_feedback.generate_candidate_feedback(CANDIDATE_RESULT)

    assert result == ai_feedback.MISSING_API_KEY_MESSAGE


def test_successful_response_is_returned(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(ai_feedback, "genai", FakeGenai)

    result = ai_feedback.generate_candidate_feedback(CANDIDATE_RESULT)

    assert result.startswith("Strengths:")


def test_api_failure_returns_safe_status(monkeypatch):
    class FailingClient:
        def __init__(self, api_key):
            raise RuntimeError("network failure")

    class FailingGenai:
        Client = FailingClient

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(ai_feedback, "genai", FailingGenai)

    result = ai_feedback.generate_candidate_feedback(CANDIDATE_RESULT)

    assert result == ai_feedback.API_FAILURE_MESSAGE
    assert "test-key" not in result


def test_prompt_contains_existing_screening_information(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(ai_feedback, "genai", FakeGenai)

    ai_feedback.generate_candidate_feedback(
        CANDIDATE_RESULT,
        job_description="Python and SQL analyst",
    )

    prompt = FakeClient.last_request["contents"]
    assert "python, pandas" in prompt
    assert "sql" in prompt
    assert "70.0" in prompt
    assert "80.0" in prompt
    assert "76.0" in prompt
    assert "Python and SQL analyst" in prompt
    assert "Do not calculate or change any score" in prompt


def test_feedback_module_does_not_calculate_screening_score():
    assert not hasattr(ai_feedback, "calculate_overall_score")
    assert not hasattr(ai_feedback, "calculate_similarity")
