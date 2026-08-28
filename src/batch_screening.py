"""Batch resume screening built on the single-resume analyzer."""

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

from src.analyzer import analyze_resume


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESUMES_DIRECTORY = PROJECT_ROOT / "data" / "resumes"


@dataclass(frozen=True)
class ScreeningFailure:
    """A resume that could not be analyzed during batch screening."""

    filename: str
    error_message: str


@dataclass
class BatchScreeningResult:
    """Successful ranked candidates and failures from one screening run."""

    candidates: list[dict]
    failures: list[ScreeningFailure]


def screen_resume_paths(
    resume_paths: Iterable[str | Path],
    job_description: str,
    *,
    progress_callback: Callable[[int, int], None] | None = None,
) -> BatchScreeningResult:
    """Analyze PDF paths once each and rank successful candidates by score."""
    paths = list(resume_paths)
    candidates = []
    failures = []

    for index, raw_path in enumerate(paths, start=1):
        resume_path = Path(raw_path)

        if resume_path.suffix.lower() != ".pdf":
            failures.append(
                ScreeningFailure(resume_path.name, "File is not a PDF.")
            )
        elif not resume_path.is_file():
            failures.append(
                ScreeningFailure(resume_path.name, "File could not be found.")
            )
        else:
            try:
                analysis = analyze_resume(resume_path, job_description)
            except Exception as error:
                error_message = str(error) or error.__class__.__name__
                failures.append(ScreeningFailure(resume_path.name, error_message))
            else:
                candidates.append({"filename": resume_path.name, **analysis})

        if progress_callback is not None:
            progress_callback(index, len(paths))

    candidates.sort(key=lambda candidate: candidate["overall_score"], reverse=True)
    return BatchScreeningResult(candidates=candidates, failures=failures)


def screen_resumes(
    job_description: str,
    resumes_directory: str | Path | None = None,
) -> BatchScreeningResult:
    """Screen PDFs in a directory, defaulting to the project's data/resumes."""
    directory = (
        Path(resumes_directory)
        if resumes_directory is not None
        else DEFAULT_RESUMES_DIRECTORY
    )
    resume_paths = sorted(
        (path for path in directory.glob("*.pdf") if path.is_file()),
        key=lambda path: path.name.lower(),
    )
    return screen_resume_paths(resume_paths, job_description)
