import pytest
import gym_data_analysis.preprocessing as preprocessing
import numpy as np


@pytest.mark.parametrize("duration, expected_output", [
    ("1h", 60),
    ("1m", 1),
    ("10h 5m", 605),
    ("3h 59m", 239)
])
def test_parse_duration(duration, expected_output):
    actual_output = preprocessing.parse_duration(duration)
    assert actual_output == expected_output
