import pytest

from src.results_analysis import calculate_score_statistics, create_candidate_dataframe
from src.text_cleaner import clean_text


def test_clean_text_normalizes_pdf_whitespace():
    assert clean_text(" Python\n\n  SQL\tPandas ") == "Python SQL Pandas"


def test_create_candidate_dataframe_ranks_candidates_by_overall_score():
    candidates = [
        {
            "filename": "lower.pdf",
            "resume_similarity": 20.0,
            "skill_match": 40.0,
            "overall_score": 32.0,
        },
        {
            "filename": "higher.pdf",
            "resume_similarity": 80.0,
            "skill_match": 90.0,
            "overall_score": 86.0,
        },
    ]

    dataframe = create_candidate_dataframe(candidates)

    assert dataframe.columns.tolist() == [
        "Rank",
        "Candidate",
        "Resume Similarity",
        "Skill Match",
        "Overall Score",
    ]
    assert dataframe["Candidate"].tolist() == ["higher.pdf", "lower.pdf"]
    assert dataframe["Rank"].tolist() == [1, 2]


def test_calculate_score_statistics_uses_overall_scores():
    dataframe = create_candidate_dataframe(
        [
            {
                "filename": "first.pdf",
                "resume_similarity": 60.0,
                "skill_match": 80.0,
                "overall_score": 72.0,
            },
            {
                "filename": "second.pdf",
                "resume_similarity": 40.0,
                "skill_match": 60.0,
                "overall_score": 52.0,
            },
        ]
    )

    statistics = calculate_score_statistics(dataframe)

    assert statistics["candidate_count"] == 2
    assert statistics["average_score"] == pytest.approx(62.0)
    assert statistics["highest_score"] == pytest.approx(72.0)
    assert statistics["lowest_score"] == pytest.approx(52.0)
    assert statistics["score_standard_deviation"] == pytest.approx(10.0)
    assert statistics["highest_scoring_candidate"] == "first.pdf"
    assert statistics["lowest_scoring_candidate"] == "second.pdf"


def test_calculate_score_statistics_handles_an_empty_dataframe():
    dataframe = create_candidate_dataframe([])

    statistics = calculate_score_statistics(dataframe)

    assert statistics["candidate_count"] == 0
    assert statistics["average_score"] is None
