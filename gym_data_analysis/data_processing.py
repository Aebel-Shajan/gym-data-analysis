import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import yaml
import calplot
import re
import datetime


# Utils
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


def first_non_zero(arr):
    I = np.nonzero(arr)
    return I[0][0]


def last_non_zero(arr):
    return len(arr) - first_non_zero(list(reversed(arr)))


def plot_heatmap(intensity, dates):
    events = pd.Series(intensity, index=dates)
    calplot.calplot(events, cmap="Greens", vmax=120)


# This is sorta broken
def plot_weekly_workouts(workout_df):
    workout_df['WeekNumber'] = workout_df['Date'].dt.strftime('%Y-%W')
    week_counts =  workout_df['WeekNumber'].value_counts().sort_index()
    x_ticks = [datetime.datetime.strptime(x + '-1', "%Y-%W-%w").strftime('%D')  for x in week_counts.index]

    plt.figure(figsize=(8, 6))
    plt.bar(x_ticks, week_counts.values)
    plt.xlabel('Week number')
    plt.xticks(x_ticks[::2], rotation="vertical")
    plt.ylabel('Frequency')
    plt.title('Workouts per week')
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
    

def plot_workouts_every_minute(workout_df):
    smallest_increment = 1 # in minutes
    total_mins = 1440
    time_bins = np.zeros(total_mins // smallest_increment, dtype=int)
    time_labels = np.arange(0, len(time_bins))#np.zeros(total_mins // smallest_increment, dtype=int)
    time_labels = ['{:02d}:{:02d}'.format(*divmod(x, 60)) for x in time_labels]
    
    # convert to mins then round to smallest increment
    workout_df["DailyMinute"] = (workout_df["Date"].dt.hour * 60) + workout_df["Date"].dt.minute
    workout_df["DailyMinute"] = (workout_df["DailyMinute"] // smallest_increment) * smallest_increment

    for index, row in workout_df.iterrows():
        start_index = int(row["DailyMinute"]) // smallest_increment
        time_bins[start_index] += 1
        for offset_index in range(row["Workout Duration"] // smallest_increment):
            time_bins[(start_index + offset_index) % len(time_bins)] += 1
    
    plt.figure(figsize=(8, 6))
    plt.plot(time_labels, time_bins)
    plt.xticks(time_labels[::120], rotation="vertical")
    plt.xlabel('Hour')
    plt.ylabel('Frequency')
    plt.title('Spread of workouts through the day')
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
    