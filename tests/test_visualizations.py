import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from src.results_analysis import create_candidate_dataframe
from src.visualizations import (
    create_overall_score_chart,
    create_similarity_skill_match_chart,
)


def _candidate_dataframe():
    return create_candidate_dataframe(
        [
            {
                "filename": "first.pdf",
                "resume_similarity": 70.0,
                "skill_match": 80.0,
                "overall_score": 76.0,
            },
            {
                "filename": "second.pdf",
                "resume_similarity": 40.0,
                "skill_match": 50.0,
                "overall_score": 46.0,
            },
        ]
    )


def test_overall_score_chart_uses_candidate_scores():
    figure = create_overall_score_chart(_candidate_dataframe())
    axis = figure.axes[0]

    assert axis.get_title() == "Overall Screening Score by Candidate"
    assert axis.get_ylabel() == "Overall Score (%)"
    assert [bar.get_height() for bar in axis.patches] == [76.0, 46.0]

    plt.close(figure)


def test_similarity_skill_match_chart_has_two_score_series():
    figure = create_similarity_skill_match_chart(_candidate_dataframe())
    axis = figure.axes[0]

    assert axis.get_title() == "Resume Similarity and Skill Match by Candidate"
    assert axis.get_ylabel() == "Score (%)"
    assert [bar.get_height() for bar in axis.patches] == [70.0, 40.0, 80.0, 50.0]
    assert [item.get_text() for item in axis.get_legend().get_texts()] == [
        "Resume Similarity",
        "Skill Match",
    ]

    plt.close(figure)
