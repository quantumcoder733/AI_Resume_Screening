"""Evaluate threshold decisions made from existing screening scores."""

from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVALUATION_DATASET = (
    PROJECT_ROOT / "data" / "evaluation" / "sample_labeled_results.csv"
)
DEFAULT_SCREENING_THRESHOLD = 60.0
POSITIVE_LABEL = "suitable"
NEGATIVE_LABEL = "not_suitable"
REQUIRED_COLUMNS = {
    "candidate",
    "screening_score",
    "actual_label",
}


def load_evaluation_dataset(path: str | Path = DEFAULT_EVALUATION_DATASET) -> pd.DataFrame:
    """Load the small synthetic/manual evaluation dataset from CSV."""
    dataframe = pd.read_csv(path)
    _validate_evaluation_data(dataframe)
    return dataframe


def add_threshold_predictions(
    dataframe: pd.DataFrame,
    threshold: float = DEFAULT_SCREENING_THRESHOLD,
) -> pd.DataFrame:
    """Add a predicted label from the existing overall screening score.

    This does not train a model. It applies a documented threshold to scores
    that were already calculated by the screening formula.
    """
    _validate_evaluation_data(dataframe)
    predictions = dataframe.copy()
    predictions["predicted_label"] = predictions["screening_score"].ge(threshold).map(
        {True: POSITIVE_LABEL, False: NEGATIVE_LABEL}
    )
    return predictions


def calculate_threshold_metrics(predictions: pd.DataFrame) -> dict[str, float]:
    """Compare threshold predictions with manually assigned labels."""
    _validate_evaluation_data(predictions)
    if "predicted_label" not in predictions.columns:
        raise ValueError("predicted_label is required to calculate evaluation metrics.")

    human_labels = predictions["actual_label"]
    predicted_labels = predictions["predicted_label"]

    return {
        "accuracy": float(accuracy_score(human_labels, predicted_labels)),
        "precision": float(
            precision_score(
                human_labels,
                predicted_labels,
                pos_label=POSITIVE_LABEL,
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                human_labels,
                predicted_labels,
                pos_label=POSITIVE_LABEL,
                zero_division=0,
            )
        ),
        "f1_score": float(
            f1_score(
                human_labels,
                predicted_labels,
                pos_label=POSITIVE_LABEL,
                zero_division=0,
            )
        ),
    }


def evaluate_screening_threshold(
    dataframe: pd.DataFrame,
    threshold: float = DEFAULT_SCREENING_THRESHOLD,
) -> tuple[pd.DataFrame, dict]:
    """Return threshold decisions and their metrics against manual labels."""
    predictions = add_threshold_predictions(dataframe, threshold)
    return predictions, calculate_threshold_metrics(predictions)


def _validate_evaluation_data(dataframe: pd.DataFrame) -> None:
    """Check that evaluation data has valid columns, scores, and labels."""
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("Evaluation data must be a pandas DataFrame.")

    missing_columns = REQUIRED_COLUMNS - set(dataframe.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Evaluation data is missing required columns: {missing}.")

    if dataframe.empty:
        raise ValueError("Evaluation data must contain at least one row.")

    valid_labels = {POSITIVE_LABEL, NEGATIVE_LABEL}
    unknown_labels = set(dataframe["actual_label"]) - valid_labels
    if unknown_labels:
        labels = ", ".join(sorted(unknown_labels))
        raise ValueError(f"Evaluation data contains unsupported actual labels: {labels}.")

    try:
        scores = pd.to_numeric(dataframe["screening_score"], errors="raise")
    except (TypeError, ValueError) as error:
        raise ValueError("screening_score must contain numeric values.") from error

    if scores.isna().any():
        raise ValueError("screening_score cannot contain missing values.")
