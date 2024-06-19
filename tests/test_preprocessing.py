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
    

def test_convert_df_to_metric():
    input_df = pd.DataFrame(data={
        "Distance": [1, 0.5, 36.5, 700, 10, 20],
        "Distance Unit": ["miles", "miles", "miles", "miles", "km", "km"],
        "Weight": [1, 0.4, 39.1, 225, 60, 80],
        "Weight Unit": ["lbs", "lbs", "lbs", "lbs", "kg", "kg"]
    })
    actual_df = preprocessing.convert_df_to_metric(input_df)
    expected_df = pd.DataFrame(data={
        "Distance": [1*1.609, 0.5*1.609, 36.5*1.609, 700*1.609, 10, 20],
        "Distance Unit": ["km", "km", "km", "km", "km", "km"],
        "Weight": [1/ 2.205, 0.4/ 2.205, 39.1/ 2.205, 225/ 2.205, 60, 80],
        "Weight Unit": ["kg", "kg", "kg", "kg", "kg", "kg"]
    })
    pd.testing.assert_frame_equal(actual_df, expected_df)
    

def test_drop_redundant_columns():
    input_df = pd.DataFrame(data={
        "A": [1, 2, 3],
        "B": [4, 5, 6],
        "C": [7, 8, 9],
        "D": [10, 11, 12]
    })
    actual_df = preprocessing.drop_redundant_columns(input_df, ["C", "B"])
    expected_df = pd.DataFrame(data={
        "A": [1, 2, 3],
        "D": [10, 11, 12]
    })
    pd.testing.assert_frame_equal(actual_df, expected_df)


@pytest.mark.parametrize("filename, content, expected_delimiter", [
    ('comma.csv', "col1,col2,col3\n1,2,3\n4,5,6\n", ','),
    ('semicolon.csv', "col1;col2;col3\n1;2;3\n4;5;6\n", ';'),
    ('tab.csv', "col1\tcol2\tcol3\n1\t2\t3\n4\t5\t6\n", '\t'),
])
def test_detect_delimiter(tmpdir, filename, content, expected_delimiter):
    # Note: tmpdir is an inbuilt fixture which allows creation of temprory files
    file_path = tmpdir.join(filename)
    with open(file_path, 'w') as f:
        f.write(content)
    with open(file_path, "r") as f:
        assert preprocessing.detect_delimiter(f) == expected_delimiter


def test_check_columns_exist():
    input_df = pd.DataFrame(data={
        "A": [1, 2, 3],
        "B": [4, 5, 6],
        "C": [7, 8, 9],
        "D": [10, 11, 12]
    })
    positive_check = preprocessing.check_columns_exist(input_df, ["A", "B"])
    negative_check = preprocessing.check_columns_exist(input_df, ["E", "F", "A", "B"])
    assert positive_check == True
    assert negative_check == False