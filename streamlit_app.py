import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import gym_data_analysis.analysis as analysis
import gym_data_analysis.preprocessing as preprocessing
import csv

# Future me will make code clean
st.image("./thumbnail.png")
st.markdown("# Strong app data analysis")

st.markdown(
    """
        To get data: 
        1. Open strong app
        2. Click profile icon at bottom
        3. Click settings icon at top right
        4. Scroll down to "general" section
        5. Click export data to download csv data
        
        or just use the sample data here for a demo:
    """)

sample_data = pd.read_csv(
    "./data/input/strong8580138242478526790.csv",
    delimiter=";",
    parse_dates=['Date']
    ).to_csv(sep=';').encode("utf-8")
st.download_button(
    label="Download sample data",
    data=sample_data,
    file_name="strong_sample_data.csv",
    mime="text/csv",
)

uploaded_file = st.file_uploader("Upload csv file from strong app here:", type="csv")


if uploaded_file is None:
    exit()

# Raw data preprocessing
raw_df = preprocessing.preprocess_strong_csv(uploaded_file)
st.write(raw_df)


# Workout dataframe
grouped_workout_df = raw_df.groupby(["Date", "Workout Name", "Workout Duration"]).agg({"Volume": "sum", "Reps": "sum"}).reset_index()
# st.write(grouped_workout_df)


# Exercise dataframe
grouped_exercise_df = raw_df.groupby(["Date", "Exercise Name"]).agg({"Volume": "sum", "Reps": "sum", "Weight": "max"}).reset_index()
# st.write(grouped_exercise_df)


analysis.plot_heatmap(
    grouped_workout_df["Workout Duration"].values, 
    grouped_workout_df["Date"].values
)
st.pyplot(plt.gcf())
analysis.plot_weekly_workouts(grouped_workout_df)
st.pyplot(plt.gcf())
analysis.plot_daily_workouts(grouped_workout_df)
st.pyplot(plt.gcf())
analysis.plot_hourly_workouts(grouped_workout_df)
st.pyplot(plt.gcf())
analysis.plot_workouts_every_minute(grouped_workout_df)
st.pyplot(plt.gcf())
