import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import gym_data_analysis.data_processing as analysis


st.write("Strong app data analysis")

uploaded_file = st.file_uploader("Upload strong data csv", type="csv")

if uploaded_file is None:
    exit()

# Raw data preprocessing
raw_df = pd.read_csv(uploaded_file, delimiter=";", parse_dates=['Date'])
raw_df['Workout Duration'] = raw_df['Workout Duration'].apply(analysis.parse_duration)
# convert weight to kg
# convert distance to metres
raw_df = raw_df.drop(columns=["Weight Unit", "RPE", "Distance", "Distance Unit", "Seconds", "Notes", "Workout Notes"])
# remove rows with null weights?
raw_df["Volume"] = raw_df["Reps"] * raw_df["Weight"]
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
