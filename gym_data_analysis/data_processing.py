import pandas as pd
import matplotlib.pyplot as plt
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

def process_data():
    print("Starting processing data")
    config = None
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    
    raw_df = pd.read_csv(config["input_data"], delimiter=";", parse_dates=['Date'])

    # df containing dates, workout names and workout duration
    workout_df = raw_df[["Date", "Workout Name", "Workout Duration"]].drop_duplicates()
    workout_df['Workout Duration'] = workout_df['Workout Duration'].apply(parse_duration)
    print(workout_df.head())
    
    july.heatmap(
        workout_df["Date"], 
        workout_df["Workout Duration"], 
        title='Workouts', 
        cmap="Blues", 
        colorbar=True,
        cmax=100,
        month_grid=True,
        fontfamily="monospace",
        fontsize=12,
        dpi=100
        )
    plt.savefig('./data/output/workout_heatmap.png', dpi=300, bbox_inches='tight')