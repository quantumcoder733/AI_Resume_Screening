def calculate_overall_score(
    resume_similarity,
    skill_match
):
    """
    Calculate the overall candidate score.

    Resume similarity contributes 40%.
    Skill match contributes 60%.
    """

    overall_score = (
        resume_similarity * 0.40
        +
        skill_match * 0.60
    )

    return overall_score