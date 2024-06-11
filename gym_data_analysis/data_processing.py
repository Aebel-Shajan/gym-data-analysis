import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yaml
import july
import re



def parse_duration(duration):
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


def plot_workouts_heatmap(workout_df):
    july.heatmap(
        workout_df["Date"], 
        workout_df["Workout Duration"], 
        title='Workouts', 
        cmap="YlGn", 
        colorbar=True,
        cmax=100,
        month_grid=True,
        fontfamily="monospace",
        fontsize=12,
        dpi=100
        )

    
def plot_weekly_workouts(workout_df):
    workout_df['WeekNumber'] = workout_df['Date'].dt.strftime('%Y-%W')
    week_counts =  workout_df['WeekNumber'].value_counts().sort_index()

    plt.figure(figsize=(8, 6))
    plt.plot(list(week_counts.index), list(week_counts.values))
    plt.xlabel('Week number')
    plt.xticks([])
    plt.ylabel('Frequency')
    plt.title('Workouts per week')
    
    # Add a label/line for when a new year starts
    years = workout_df['Date'].dt.year.unique()
    for year in years:
        first_week = f'{year}-01'
        if first_week in week_counts.index:
            plt.axvline(x=first_week, color='red', linestyle='--', linewidth=1)
            # Add text with the year
            plt.text(x=first_week, y=week_counts.max(), s=str(year), color='red', ha='center', va='bottom')
            
    plt.show()


def plot_daily_workouts(workout_df):
    workout_df['DayName'] = workout_df['Date'].dt.day_name()
    day_counts = workout_df['DayName'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    plt.figure(figsize=(8, 6))
    plt.bar(day_counts.index, day_counts.values)
    plt.xlabel('Day')
    plt.ylabel('Frequency')
    plt.title('Workouts per day')
    plt.show()
    
    
def plot_hourly_workouts(workout_df):
    workout_df["HourNumber"] = workout_df["Date"].dt.strftime('%H')
    hour_counts = workout_df["HourNumber"].value_counts().sort_index()
    
    plt.figure(figsize=(8, 6))
    plt.bar(hour_counts.index, hour_counts.values)
    plt.xlabel('Hour')
    plt.ylabel('Frequency')
    plt.title('Workouts per hour')
    plt.show()
    
def plot_workout_types(workout_df):
    workout_type_counts = workout_df["Workout Name"].value_counts()
    
    plt.figure(figsize=(8, 6))
    plt.bar(workout_type_counts.index, workout_type_counts.values)
    plt.xticks(rotation='vertical',  fontsize=10)
    plt.xlabel('Workout Name')
    plt.ylabel('Frequency')
    plt.title('Workout types')
    plt.show()
    