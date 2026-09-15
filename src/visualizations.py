"""Simple Matplotlib charts for resume screening results."""

import matplotlib.pyplot as plt
import pandas as pd


def create_overall_score_chart(dataframe: pd.DataFrame):
    """Return a bar chart of each candidate's overall screening score."""
    figure, axis = plt.subplots(figsize=(8, 4.5))

    if dataframe.empty:
        axis.text(0.5, 0.5, "No candidate data available.", ha="center", va="center")
        axis.set_axis_off()
        return figure

    axis.bar(dataframe["Candidate"], dataframe["Overall Score"], color="#4C78A8")
    axis.set_title("Overall Screening Score by Candidate")
    axis.set_xlabel("Candidate")
    axis.set_ylabel("Overall Score (%)")
    axis.set_ylim(0, 100)
    axis.tick_params(axis="x", rotation=25)
    figure.tight_layout()
    return figure


def create_similarity_skill_match_chart(dataframe: pd.DataFrame):
    """Return a grouped bar chart for similarity and skill-match scores."""
    figure, axis = plt.subplots(figsize=(8, 4.5))

    if dataframe.empty:
        axis.text(0.5, 0.5, "No candidate data available.", ha="center", va="center")
        axis.set_axis_off()
        return figure

    positions = range(len(dataframe))
    bar_width = 0.35
    axis.bar(
        [position - bar_width / 2 for position in positions],
        dataframe["Resume Similarity"],
        width=bar_width,
        label="Resume Similarity",
        color="#4C78A8",
    )
    axis.bar(
        [position + bar_width / 2 for position in positions],
        dataframe["Skill Match"],
        width=bar_width,
        label="Skill Match",
        color="#59A14F",
    )
    axis.set_title("Resume Similarity and Skill Match by Candidate")
    axis.set_xlabel("Candidate")
    axis.set_ylabel("Score (%)")
    axis.set_ylim(0, 100)
    axis.set_xticks(list(positions), dataframe["Candidate"], rotation=25)
    axis.legend()
    figure.tight_layout()
    return figure
