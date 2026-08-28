from pathlib import Path

from src.analyzer import analyze_resume
from src.batch_screening import screen_resume_paths, screen_resumes
from src.pdf_extractor import extract_text_from_pdf


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_RESUME = PROJECT_ROOT / "data" / "resumes" / "resume1.pdf"
JOB_DESCRIPTION = """
We are looking for a Python developer with experience in SQL, Pandas, NumPy,
Machine Learning, TensorFlow, Docker and AWS.
"""


def test_extract_text_from_sample_pdf():
    assert extract_text_from_pdf(SAMPLE_RESUME).strip()


def test_analyze_resume_returns_serializable_result():
    result = analyze_resume(SAMPLE_RESUME, JOB_DESCRIPTION)

    assert {
        "resume_similarity",
        "skill_match",
        "overall_score",
        "matched_skills",
        "missing_skills",
    } <= result.keys()
    assert 0 <= result["overall_score"] <= 100
    assert isinstance(result["matched_skills"], list)
    assert isinstance(result["missing_skills"], list)
    assert result["matched_skills"] == sorted(result["matched_skills"])
    assert result["missing_skills"] == sorted(result["missing_skills"])


def test_screen_resumes_uses_the_project_resume_directory():
    result = screen_resumes(JOB_DESCRIPTION)

    assert result.candidates
    assert result.candidates[0]["filename"] == SAMPLE_RESUME.name
    assert result.candidates == sorted(
        result.candidates,
        key=lambda result: result["overall_score"],
        reverse=True,
    )


def test_screen_resume_paths_sorts_candidates_by_overall_score(monkeypatch):
    lower_score_resume = Path("lower-score.pdf")
    higher_score_resume = Path("higher-score.pdf")
    monkeypatch.setattr("src.batch_screening.Path.is_file", lambda _path: True)

    def fake_analyze_resume(resume_path, _job_description):
        score = 20 if Path(resume_path).name == lower_score_resume.name else 80
        return {
            "overall_score": score,
            "resume_similarity": score,
            "skill_match": score,
            "matched_skills": [],
            "missing_skills": [],
        }

    monkeypatch.setattr("src.batch_screening.analyze_resume", fake_analyze_resume)
    result = screen_resume_paths([lower_score_resume, higher_score_resume], JOB_DESCRIPTION)

    assert [candidate["filename"] for candidate in result.candidates] == [
        higher_score_resume.name,
        lower_score_resume.name,
    ]
    assert result.failures == []


def test_screen_resume_paths_preserves_candidates_when_one_file_fails(monkeypatch):
    valid_resume = Path("valid.pdf")
    invalid_resume = Path("invalid.pdf")
    analyzed_paths = []
    monkeypatch.setattr("src.batch_screening.Path.is_file", lambda _path: True)

    def fake_analyze_resume(resume_path, _job_description):
        analyzed_paths.append(Path(resume_path).name)
        if Path(resume_path).name == invalid_resume.name:
            raise ValueError("Unreadable PDF")
        return {
            "overall_score": 75,
            "resume_similarity": 60,
            "skill_match": 85,
            "matched_skills": ["python"],
            "missing_skills": ["sql"],
        }

    monkeypatch.setattr("src.batch_screening.analyze_resume", fake_analyze_resume)
    result = screen_resume_paths([valid_resume, invalid_resume], JOB_DESCRIPTION)

    assert analyzed_paths == [valid_resume.name, invalid_resume.name]
    assert [candidate["filename"] for candidate in result.candidates] == [valid_resume.name]
    assert len(result.failures) == 1
    assert result.failures[0].filename == invalid_resume.name
    assert result.failures[0].error_message == "Unreadable PDF"
