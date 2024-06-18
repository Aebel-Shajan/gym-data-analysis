import pytest
import gym_data_analysis.preprocessing as preprocessing
import numpy as np
import pandas as pd


@pytest.mark.parametrize("duration, expected_output", [
    ("1h", 60),
    ("1m", 1),
    ("10h 5m", 605),
    ("3h 59m", 239)
])
def test_parse_duration(duration, expected_output):
    actual_output = preprocessing.parse_duration(duration)
    assert actual_output == expected_output


# Am i doing to much here?
@pytest.mark.parametrize(
    "input_row, expected_weight",
    [
        (pd.Series({"Weight": 220.5, "Weight Unit": "lbs"}), 220.5 / 2.205),
        (pd.Series({"Weight": 100, "Weight Unit": "kg"}), 100),
        (pd.Series({"Weight": 150, "Weight Unit": "lbs"}), 150 / 2.205),
        (pd.Series({"Weight": 75, "Weight Unit": "kg"}), 75)
    ]
)
def test_convert_weights_to_metric(input_row, expected_weight):
    actual_output = preprocessing.convert_weights_to_metric(input_row)
    assert actual_output["Weight"] == expected_weight
    assert actual_output["Weight Unit"] == "kg"


@pytest.mark.parametrize(
    "input_row, expected_distance",
    [
        (pd.Series({"Distance": 220.5, "Distance Unit": "miles"}), 220.5 * 1.609),
        (pd.Series({"Distance": 100, "Distance Unit": "km"}), 100),
        (pd.Series({"Distance": 150, "Distance Unit": "miles"}), 150 * 1.609),
        (pd.Series({"Distance": 75, "Distance Unit": "km"}), 75)
    ]
)
def test_convert_distance_to_metric(input_row, expected_distance):
    actual_output = preprocessing.convert_distance_to_metric(input_row)
    assert actual_output["Distance"] == expected_distance
    assert actual_output["Distance Unit"] == "km"