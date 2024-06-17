import numpy as np
import re


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


def convert_lbs_to_kg(pounds: float) -> float:
    """
    Converts the weight from pounds to kilograms
    
    Parameters
    ----------
    pounds : float
        Float equal to the number of pounds.
        
    Returns
    -------
    kilograms : float
        Equivalent weight in kilograms
    """
    return pounds / 2.205
    

def convert_miles_to_km(miles: float) -> float:
    """
    Converts miles to kilometers given distance in miles.
    
    Parameters
    ----------
    miles : float
        Float equal to number of miles
        
    Returns
    -------
    kilometers : float
        Equivalent distance in kilometers
    """
    return miles * 1.609


