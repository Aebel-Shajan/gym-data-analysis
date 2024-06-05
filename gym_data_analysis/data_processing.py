import pandas as pd
import yaml

def process_data():
    print("Starting processing data")
    config = None
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    
    workout_data = pd.read_csv(config["input_data"], delimiter=";")
    print(workout_data.head())
    