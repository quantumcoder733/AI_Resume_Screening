"""Pandas and NumPy helpers for batch screening results."""

import numpy as np
import pandas as pd


DISPLAY_COLUMNS = [
    "Candidate",
    "Resume Similarity",
    "Skill Match",
    "Overall Score",
]


def create_candidate_dataframe(candidates: list[dict]) -> pd.DataFrame:
    """Convert screening results into a ranked, beginner-friendly DataFrame."""
    rows = [
        {
            "Candidate": candidate["filename"],
            "Resume Similarity": candidate["resume_similarity"],
            "Skill Match": candidate["skill_match"],
            "Overall Score": candidate["overall_score"],
        }
        for candidate in candidates
    ]
    dataframe = pd.DataFrame(rows, columns=DISPLAY_COLUMNS)

    if dataframe.empty:
        return pd.DataFrame(columns=["Rank", *DISPLAY_COLUMNS])

    dataframe = dataframe.sort_values(
        "Overall Score",
        ascending=False,
        kind="stable",
    ).reset_index(drop=True)
    dataframe.insert(0, "Rank", np.arange(1, len(dataframe) + 1))
    return dataframe


def calculate_score_statistics(dataframe: pd.DataFrame) -> dict:
    """Calculate understandable overall-score statistics with NumPy."""
    if dataframe.empty:
        return {
            "candidate_count": 0,
            "average_score": None,
            "highest_score": None,
            "lowest_score": None,
            "score_standard_deviation": None,
            "highest_scoring_candidate": None,
            "lowest_scoring_candidate": None,
        }

    scores = dataframe["Overall Score"].to_numpy(dtype=float)
    highest_index = int(np.argmax(scores))
    lowest_index = int(np.argmin(scores))

    return {
        "candidate_count": len(scores),
        "average_score": float(np.mean(scores)),
        "highest_score": float(np.max(scores)),
        "lowest_score": float(np.min(scores)),
        "score_standard_deviation": float(np.std(scores)),
        "highest_scoring_candidate": dataframe.iloc[highest_index]["Candidate"],
        "lowest_scoring_candidate": dataframe.iloc[lowest_index]["Candidate"],
    }
