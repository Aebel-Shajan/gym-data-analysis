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

def plot_workout_heatmap(workout_df):
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
    plt.savefig('./data/output/workout_heatmap.png', dpi=300, bbox_inches='tight')

def plot_workout_barplot(workout_df):
    workout_df['Day of Week'] = workout_df['Date'].dt.day_name()
    day_counts = workout_df['Day of Week'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])


    plt.figure(figsize=(8, 6))
    plt.bar(day_counts.index, day_counts.values)
    plt.xlabel('Day of Week')
    plt.ylabel('Frequency')
    plt.title('Workout Frequency by Day of Week')
    plt.savefig('./data/output/workout_barplot.png', dpi=300)
    plt.show()
    
def plot_weekly_workout(workout_df):
    workout_df['WeekNumber'] = workout_df['Date'].dt.strftime('%Y-%W')
    print(workout_df.head())
    week_counts =  workout_df['WeekNumber'].value_counts().sort_index()
    
    plt.figure(figsize=(8, 6))
    plt.bar(week_counts.index, week_counts.values)
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
    
    plt.savefig('./data/output/weekly_workout_barplot.png', dpi=300)
    plt.show()

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
    
    # display heatmap
    plot_workout_heatmap(workout_df)
    
    # display workout frequency
    plot_workout_barplot(workout_df)
    
    plot_weekly_workout(workout_df)