from pathlib import Path

from src.pdf_extractor import extract_text_from_pdf
from src.skill_extractor import extract_skills
from src.matcher import calculate_similarity
from src.scorer import calculate_overall_score

def analyze_resume(resume_path: str | Path, job_description: str) -> dict:
    """Analyze one resume against a job description.

    The public result uses sorted lists so it can be serialized directly by a
    future UI or API. Set operations remain internal to the calculation.
    """

    # Extract resume text
    resume_text = extract_text_from_pdf(
        resume_path
    )

    # Extract skills
    resume_skills = set(
        extract_skills(resume_text)
    )

    required_skills = set(
        extract_skills(job_description)
    )

    # Skill comparison
    matched_skills = (
        resume_skills & required_skills
    )

    missing_skills = (
        required_skills - resume_skills
    )

    # Skill percentage
    if required_skills:

        skill_match = (
            len(matched_skills)
            /
            len(required_skills)
        ) * 100

    else:

        skill_match = 0

    # Text similarity
    resume_similarity = calculate_similarity(
        resume_text,
        job_description
    )

    # Overall score
    overall_score = calculate_overall_score(
        resume_similarity,
        skill_match
    )

    return {
        "resume_similarity": resume_similarity,
        "skill_match": skill_match,
        "overall_score": overall_score,
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
    }
