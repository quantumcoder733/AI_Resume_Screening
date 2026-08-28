"""Streamlit interface for the AI Resume Screening System."""

from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import streamlit as st
from pypdf.errors import PdfReadError

from src.analyzer import analyze_resume
from src.batch_screening import BatchScreeningResult, screen_resume_paths


st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide",
)


def _score_progress(score: float, label: str) -> None:
    """Show a bounded score as a progress bar."""
    progress = min(max(score / 100, 0.0), 1.0)
    st.progress(progress, text=f"{label}: {score:.2f}%")


def _display_skills(title: str, skills: list[str], empty_message: str) -> None:
    """Display a skill collection as readable tags."""
    st.subheader(title)
    if skills:
        st.markdown(" ".join(f"`{skill}`" for skill in skills))
    else:
        st.caption(empty_message)


def _analyze_uploaded_resume(uploaded_resume, job_description: str) -> dict:
    """Analyze one upload through the existing pipeline and remove its temp file."""
    temporary_path: Path | None = None
    try:
        with NamedTemporaryFile(suffix=".pdf", delete=False) as temporary_file:
            temporary_file.write(uploaded_resume.getvalue())
            temporary_path = Path(temporary_file.name)

        return analyze_resume(temporary_path, job_description)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def _screen_uploaded_resumes(
    uploaded_resumes,
    job_description: str,
    progress_callback,
) -> BatchScreeningResult:
    """Temporarily materialize uploads, then use the shared batch pipeline."""
    with TemporaryDirectory() as temporary_directory:
        temporary_root = Path(temporary_directory)
        resume_paths = []

        for index, uploaded_resume in enumerate(uploaded_resumes):
            # A per-upload directory keeps duplicate filenames distinct while
            # preserving the original filename in the batch result.
            upload_directory = temporary_root / str(index)
            upload_directory.mkdir()
            resume_path = upload_directory / Path(uploaded_resume.name).name
            resume_path.write_bytes(uploaded_resume.getvalue())
            resume_paths.append(resume_path)

        return screen_resume_paths(
            resume_paths,
            job_description,
            progress_callback=progress_callback,
        )


def _display_single_result(result: dict) -> None:
    """Render the single-resume analysis result."""
    st.success("Analysis complete")
    overall_column, similarity_column, skills_column = st.columns(3)
    overall_column.metric("Overall Score", f"{result['overall_score']:.2f}%")
    similarity_column.metric("Resume Similarity", f"{result['resume_similarity']:.2f}%")
    skills_column.metric("Skill Match", f"{result['skill_match']:.2f}%")

    st.subheader("Score breakdown")
    _score_progress(result["overall_score"], "Overall Score")
    _score_progress(result["resume_similarity"], "Resume Similarity")
    _score_progress(result["skill_match"], "Skill Match")

    matched_column, missing_column = st.columns(2)
    with matched_column:
        _display_skills(
            "Matched Skills",
            result["matched_skills"],
            "No matching skills were identified.",
        )
    with missing_column:
        _display_skills(
            "Missing Skills",
            result["missing_skills"],
            "No missing required skills were identified.",
        )


def _display_ranking(result: BatchScreeningResult) -> None:
    """Render ranked candidates and any files skipped during analysis."""
    for failure in result.failures:
        st.warning(f"Skipped {failure.filename}: {failure.error_message}")

    if not result.candidates:
        st.error("No resumes could be analyzed. Please upload valid PDF resumes.")
        return

    st.success(f"Ranked {len(result.candidates)} candidate(s).")
    ranking_rows = [
        {
            "Rank": rank,
            "Candidate": candidate["filename"],
            "Overall Score": f"{candidate['overall_score']:.2f}%",
            "Resume Similarity": f"{candidate['resume_similarity']:.2f}%",
            "Skill Match": f"{candidate['skill_match']:.2f}%",
        }
        for rank, candidate in enumerate(result.candidates, start=1)
    ]
    st.dataframe(ranking_rows, hide_index=True, use_container_width=True)

    st.subheader("Candidate details")
    for rank, candidate in enumerate(result.candidates, start=1):
        with st.expander(f"#{rank} — {candidate['filename']}"):
            matched_column, missing_column = st.columns(2)
            with matched_column:
                _display_skills(
                    "Matched Skills",
                    candidate["matched_skills"],
                    "No matching skills were identified.",
                )
            with missing_column:
                _display_skills(
                    "Missing Skills",
                    candidate["missing_skills"],
                    "No missing required skills were identified.",
                )


def main() -> None:
    """Render the application."""
    st.markdown(
        """
        <style>
        .block-container { max-width: 1050px; padding-top: 3rem; }
        [data-testid="stMetricValue"] { font-size: 2rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.header("About this project")
        st.write(
            "Compare PDF resumes with a job description using TF-IDF "
            "similarity and skill coverage."
        )
        st.divider()
        st.subheader("Scoring methodology")
        st.write("Resume Similarity: **40%**")
        st.write("Skill Match: **60%**")

    st.title("AI Resume Screening System")
    st.write(
        "Upload one or more PDF resumes and enter a job description for an "
        "explainable screening summary. Uploaded files are used temporarily "
        "and are not saved permanently."
    )

    job_description = st.text_area(
        "Job description",
        placeholder="Paste the role requirements, responsibilities, and desired skills here...",
        height=220,
    )

    single_tab, multiple_tab = st.tabs(["Single Resume", "Multiple Resumes"])

    with single_tab:
        uploaded_resume = st.file_uploader("Upload a PDF resume", type=["pdf"])
        if st.button("Analyze Resume", type="primary", use_container_width=True):
            if uploaded_resume is None:
                st.warning("Please upload a PDF resume before analyzing.")
            elif not job_description.strip():
                st.warning("Please enter a job description before analyzing.")
            else:
                try:
                    with st.spinner("Analyzing resume..."):
                        result = _analyze_uploaded_resume(uploaded_resume, job_description)
                except PdfReadError:
                    st.error("The uploaded file is not a readable PDF. Please upload a valid PDF resume.")
                except Exception:
                    st.error("The resume could not be analyzed. Please try another PDF or try again.")
                else:
                    _display_single_result(result)

    with multiple_tab:
        uploaded_resumes = st.file_uploader(
            "Upload PDF resumes",
            type=["pdf"],
            accept_multiple_files=True,
        )
        if st.button("Rank Candidates", type="primary", use_container_width=True):
            if not uploaded_resumes:
                st.warning("Please upload at least one PDF resume before ranking.")
            elif not job_description.strip():
                st.warning("Please enter a job description before ranking.")
            else:
                progress_bar = st.progress(0, text="Preparing resumes...")

                def update_progress(processed: int, total: int) -> None:
                    percentage = int((processed / total) * 100) if total else 100
                    progress_bar.progress(
                        percentage,
                        text=f"Analyzed {processed} of {total} resume(s)...",
                    )

                try:
                    result = _screen_uploaded_resumes(
                        uploaded_resumes,
                        job_description,
                        update_progress,
                    )
                except Exception:
                    st.error("The resumes could not be prepared for analysis. Please try again.")
                else:
                    progress_bar.progress(100, text="Ranking complete")
                    _display_ranking(result)


if __name__ == "__main__":
    main()
