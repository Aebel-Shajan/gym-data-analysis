import numpy as np
import pandas as pd
import yaml
import re
import csv
from typing import BinaryIO


def parse_duration(duration: str) -> int:
    """
    Parse a duration string formatted as '<hours>h <minutes>m' into total minutes.

    Parameters
    ----------
    duration : str
        A string representing the duration, such as '2h 30m', '45m', '3h', or similar formats.

    Returns
    -------
    total_minutes : int
        The total duration in minutes.
    """

    # Initialize the total duration in minutes
    total_minutes = 0
    
    # Regex to match hours and minutes
    match = re.match(r'(?:(\d+)h)?\s*(?:(\d+)m)?', duration)
    if match:
        hours = match.group(1)
        minutes = match.group(2)
        if hours:
            total_minutes += int(hours) * 60
        if minutes:
            total_minutes += int(minutes)
    return total_minutes


def convert_weights_to_metric(row):
        
    """
    Converts the weight column from pounds to kilograms in a given row
    
    Parameters
    ----------
    row : pandas dataframe row
        row to modify
        
    Returns
    -------
    row : pandas dataframe row
    """
    if row["Weight Unit"] == "lbs":
        row["Weight"] = row["Weight"] / 2.205
        row["Weight Unit"] = "kg"
    return row
    

def convert_distance_to_metric(row):
    """Converts the distance column from miles to kilometres in a given row

    Args:
        row : pandas dataframe row

    Returns:
        row : pandas dataframe row 
    """
    if row["Distance Unit"] == "miles":
        row["Distance"] = row["Distance"]* 1.609
        row["Distance Unit"] = "km"
    return row


def convert_df_to_metric(df: pd.DataFrame) -> pd.DataFrame:
    """Converts "Weight" and "Distance" columns in a pandas to metric using "Weight Unit" and "Distance Unit" columns.
    
    Parameters
    ----------
    df: pd.DataFrame
        Input dataframe
        
    Returns
    -------
    metric_df: pd.DataFrame
        Output dataframe with "Weight" and "Distance" converted to kg and km.
    """
    metric_df = df
    if "Weight" in df and "Weight Unit" in df:
        metric_df = metric_df.apply(convert_weights_to_metric, axis=1)   
    if "Distance" in df and "Distance Unit" in df:
        metric_df = metric_df.apply(convert_distance_to_metric, axis=1)       
    return metric_df


def drop_redundant_columns(df: pd.DataFrame, redundant_cols: list[str]) -> pd.DataFrame:
    """Drops redundant columns from dataframe obtained from the exported strong data csv.

    Args:
        df (pd.DataFrame): dataframe obtained from the exported strong data csv
        redundant_cols (list[str]): columns to drop

    Returns:
        pd.DataFrame: dataframe with redundant columns dropped
    """
    output_df = df
    for column in redundant_cols:
        if column in df:
            output_df = output_df.drop(columns=[column])

    return output_df


def detect_delimiter(csv_file: BinaryIO) -> str:
    """
    Detect the delimiter used in a CSV file.

    Args:
        csv_file (BinaryIO): The path to the CSV file.

    Returns:
        str: The detected delimiter (e.g. ',', ';', '\t', etc.).
    """
    original_pos = csv_file.tell()
    dialect = csv.Sniffer().sniff(csv_file.read(1024))
    csv_file.seek(original_pos)
    return dialect.delimiter


def check_columns_exist(df: pd.DataFrame, columns: list[str]) -> bool:
    """Checks if a given dataframe contains the provided columns

    Args:
        df (pd.DataFrame): Dataframe to check columns
        columns (list[str]): Columns to check

    Returns:
        bool: True if dataframe contains all columns provided. False otherwise
    """
    return set(columns).issubset(df.columns)


def preprocess_strong_csv(csv_file):
    """Reads strong data csv from config.yaml file and perform some preprocessing to get a pandas dataframe.
    The strong app exported data has different formats, this function also aims to standardise them.

    Raises:
        Exception: Csv not provided in correct format

    Returns:
        pd.DataFrame: Resulting dataframe
    """
    # Read in csv from config into a pandas dataframe
    raw_df= pd.read_csv(csv_file, delimiter=detect_delimiter(csv_file), parse_dates=['Date'])
    
    # The strong app has 2 different formats with different column names
    if "Duration" in raw_df:
        raw_df = raw_df.rename(columns={"Duration" : "Workout Duration"})
    
    # Check that csv has required columns
    required_columns = [
        "Date",
        "Workout Name",
        "Exercise Name",
        "Set Order",
        "Weight",
        "Reps",
        "Distance",
        "Seconds",
        "Workout Duration"
        ]
    if not check_columns_exist(raw_df, required_columns):
        raise Exception("CSV provided not in correct format.")
        
    # Format the columns
    raw_df['Workout Duration'] = raw_df['Workout Duration'].apply(parse_duration)
    raw_df = convert_df_to_metric(raw_df)
    
    # Remove columns not needed for analysis
    redundant_columns = [ "RPE", "Distance",  "Seconds", "Notes", "Workout Notes", "Weight Unit", "Distance Unit"]
    raw_df = drop_redundant_columns(raw_df, redundant_columns)
    
    # Add a new column for volume
    raw_df["Volume"] = raw_df["Weight"] * raw_df["Reps"]
    return raw_df
