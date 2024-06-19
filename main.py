from gym_data_analysis.preprocessing import preprocess_strong_csv
import yaml

def main():
    config = None
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    #Preprocessing
    with open(config["input_data"]) as csv_file:
        raw_df = preprocess_strong_csv(csv_file)
    print(raw_df)

if __name__ == "__main__":
    main()
