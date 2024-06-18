from gym_data_analysis.preprocessing import preprocess_strong_csv
import yaml

def main():
    config = None
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    #Preprocessing
    raw_df = preprocess_strong_csv(config["input_data"])
    print(raw_df)

if __name__ == "__main__":
    main()
