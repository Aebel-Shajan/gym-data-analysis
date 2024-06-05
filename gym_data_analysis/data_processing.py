import pandas as pd
import yaml

def process_data():
    print("Starting processing data")
    config = None
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    
    raw_df = pd.read_csv(config["input_data"], delimiter=";", parse_dates=['Date'])

    # df containing dates, workout names and workout duration
    workout_df = raw_df[["Date", "Workout Name", "Workout Duration"]].drop_duplicates()
    print(workout_df.head())