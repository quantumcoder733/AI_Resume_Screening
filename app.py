"""Single-page Streamlit interface for the AI Resume Screening System."""

from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
import streamlit as st

from src.batch_screening import BatchScreeningResult, screen_resume_paths
from src.ai_feedback import (
    API_FAILURE_MESSAGE,
    MISSING_API_KEY_MESSAGE,
    generate_candidate_feedback,
)
from src.results_analysis import calculate_score_statistics, create_candidate_dataframe
from src.visualizations import (
    create_overall_score_chart,
    create_similarity_skill_match_chart,
)


def _screen_uploaded_resumes(uploaded_resumes, job_description: str) -> BatchScreeningResult:
    """Temporarily materialize uploads, then use the shared batch pipeline."""
    with TemporaryDirectory() as temporary_directory:
        temporary_root = Path(temporary_directory)
        resume_paths = []

        for index, uploaded_resume in enumerate(uploaded_resumes):
            # Separate folders preserve duplicate filenames during one upload.
            upload_directory = temporary_root / str(index)
            upload_directory.mkdir()
            resume_path = upload_directory / Path(uploaded_resume.name).name
            resume_path.write_bytes(uploaded_resume.getvalue())
            resume_paths.append(resume_path)

        return screen_resume_paths(resume_paths, job_description)


def _display_ranking(result: BatchScreeningResult, job_description: str) -> None:
    """Render rankings, candidate statistics, and skill details."""
    for failure in result.failures:
        st.warning(f"Skipped {failure.filename}: {failure.error_message}")

    if not result.candidates:
        st.error("No resumes could be analyzed. Please upload valid PDF resumes.")
        return

    dataframe = create_candidate_dataframe(result.candidates)
    statistics = calculate_score_statistics(dataframe)

    st.success(f"Ranked {statistics['candidate_count']} candidate(s).")
    st.subheader("Candidate ranking")
    st.dataframe(dataframe, hide_index=True)

    st.subheader("Score statistics")
    st.write(f"Average score: {statistics['average_score']:.2f}%")
    st.write(
        "Highest score: "
        f"{statistics['highest_score']:.2f}% "
        f"({statistics['highest_scoring_candidate']})"
    )
    st.write(
        "Lowest score: "
        f"{statistics['lowest_score']:.2f}% "
        f"({statistics['lowest_scoring_candidate']})"
    )
    st.write(
        "Score standard deviation: "
        f"{statistics['score_standard_deviation']:.2f}"
    )

    st.subheader("Screening and ranking visualizations")
    st.write("These charts visualize screening scores; they are not accuracy charts.")
    overall_score_figure = create_overall_score_chart(dataframe)
    comparison_figure = create_similarity_skill_match_chart(dataframe)
    st.pyplot(overall_score_figure)
    st.pyplot(comparison_figure)

    st.subheader("Candidate details")
    details_df = pd.DataFrame(
        {
            "Resume File Name": [candidate["filename"] for candidate in result.candidates],
            "Matched Skills": [
                ", ".join(candidate["matched_skills"])
                if candidate["matched_skills"]
                else "No matched skills"
                for candidate in result.candidates
            ],
            "Unmatched Skills": [
                ", ".join(candidate["missing_skills"])
                if candidate["missing_skills"]
                else "No missing skills"
                for candidate in result.candidates
            ],
        }
    )
    st.dataframe(details_df, hide_index=True)

    st.write("AI feedback")
    for rank, candidate in enumerate(result.candidates, start=1):
        st.write(candidate["filename"])
        if st.button("Generate AI Feedback", key=f"ai-feedback-{rank}"):
            feedback = generate_candidate_feedback(candidate, job_description)
            if feedback == MISSING_API_KEY_MESSAGE:
                st.info(feedback)
            elif feedback == API_FAILURE_MESSAGE:
                st.warning(feedback)
            else:
                st.write("AI feedback:")
                st.write(feedback)


def main() -> None:
    """Render the application."""
    st.title("AI Resume Screening System")
    st.write(
        "Upload one or more PDF resumes and enter a job description to compare "
        "candidates. Overall score = 40% resume similarity + 60% skill match."
    )

    job_description = st.text_area(
        "Job description",
        placeholder="Paste the role requirements and desired skills here...",
        height=220,
    )
    uploaded_resumes = st.file_uploader(
        "Upload one or more PDF resumes",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if st.button("Screen Resumes"):
        if not uploaded_resumes:
            st.warning("Please upload at least one PDF resume before screening.")
        elif not job_description.strip():
            st.warning("Please enter a job description before screening.")
        else:
            try:
                result = _screen_uploaded_resumes(uploaded_resumes, job_description)
            except Exception:
                st.error("The resumes could not be prepared for analysis. Please try again.")
            else:
                st.session_state["screening_result"] = result
                st.session_state["screening_job_description"] = job_description

    if "screening_result" in st.session_state:
        _display_ranking(
            st.session_state["screening_result"],
            st.session_state["screening_job_description"],
        )


if __name__ == "__main__":
    main()
