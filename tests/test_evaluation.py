import pandas as pd
import pytest

from src.evaluation import (
    DEFAULT_SCREENING_THRESHOLD,
    add_threshold_predictions,
    calculate_threshold_metrics,
    evaluate_screening_threshold,
    load_evaluation_dataset,
)


def test_threshold_evaluation_calculates_metrics_from_sample_data():
    dataframe = load_evaluation_dataset()

    predictions, metrics = evaluate_screening_threshold(
        dataframe,
        DEFAULT_SCREENING_THRESHOLD,
    )

    assert predictions["predicted_label"].tolist() == [
        "suitable",
        "suitable",
        "suitable",
        "not_suitable",
        "not_suitable",
        "not_suitable",
    ]
    assert metrics["accuracy"] == pytest.approx(4 / 6)
    assert metrics["precision"] == pytest.approx(2 / 3)
    assert metrics["recall"] == pytest.approx(2 / 3)
    assert metrics["f1_score"] == pytest.approx(2 / 3)


def test_threshold_includes_score_equal_to_cutoff():
    dataframe = pd.DataFrame(
        {
            "candidate": ["at_cutoff", "below_cutoff"],
            "screening_score": [60.0, 59.99],
            "actual_label": ["suitable", "not_suitable"],
        }
    )

    predictions = add_threshold_predictions(dataframe, threshold=60.0)

    assert predictions["predicted_label"].tolist() == [
        "suitable",
        "not_suitable",
    ]


def test_empty_evaluation_data_is_rejected():
    empty_dataframe = pd.DataFrame(
        columns=["candidate", "screening_score", "actual_label"]
    )

    with pytest.raises(ValueError, match="at least one row"):
        add_threshold_predictions(empty_dataframe)


def test_invalid_label_is_rejected():
    dataframe = pd.DataFrame(
        {
            "candidate": ["candidate"],
            "screening_score": [70.0],
            "actual_label": ["unknown"],
        }
    )

    with pytest.raises(ValueError, match="unsupported actual labels"):
        add_threshold_predictions(dataframe)


def test_metrics_require_predicted_labels():
    dataframe = load_evaluation_dataset()

    with pytest.raises(ValueError, match="predicted_label is required"):
        calculate_threshold_metrics(dataframe)
