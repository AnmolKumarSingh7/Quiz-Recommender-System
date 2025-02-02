import streamlit as st
import pandas as pd
import json
import os

# File paths for all three datasets
file_paths = [
    r"C:\Users\anmol\OneDrive\Desktop\Quiz_recommendation\API1.json",
    r"C:\Users\anmol\OneDrive\Desktop\Quiz_recommendation\API2.json",
    r"C:\Users\anmol\OneDrive\Desktop\Quiz_recommendation\API3.json"
]

# Load and combine all datasets
data_frames = []
for file in file_paths:
    if os.path.exists(file):  # Check if file exists
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

            # Handle both dictionary and list structures
            if isinstance(data, dict):
                # Convert dictionary to list of records
                data = [data]

            if isinstance(data, list):
                df = pd.DataFrame(data)
                data_frames.append(df)
            else:
                st.error(f"Invalid JSON format in {file}")

# Merge all datasets into one DataFrame
if data_frames:
    interactions_df = pd.concat(data_frames, ignore_index=True)
else:
    st.error("Error: No valid datasets found. Please check the JSON structure.")

# Debugging: Show the first few rows and unique quiz_ids
st.write("### Sample Data:")
st.write(interactions_df.head())

# Check if the quiz_id and score columns exist
st.write("### Columns in the dataset:")
st.write(interactions_df.columns)


# Function to recommend quizzes
def recommend_for_quiz(quiz_id, top_n=5):
    # Ensure the necessary columns are in the dataset
    required_columns = {'quiz_id', 'user_id', 'score'}
    if not required_columns.issubset(interactions_df.columns):
        return ["Error: Missing necessary columns in dataset."]

    # Show available quiz IDs
    st.write("### Available Quiz IDs in the dataset:")
    st.write(interactions_df['quiz_id'].unique())

    quiz_data = interactions_df[interactions_df['quiz_id'] == quiz_id]

    if quiz_data.empty:
        return ["No recommendations found for this quiz."]

    recommended_users = quiz_data.sort_values(by="score", ascending=False)['user_id'].head(top_n).tolist()

    return recommended_users


# Streamlit UI
st.title("📚 Quiz Recommender System")

# Input for quiz ID
quiz_id = st.text_input("Enter Quiz ID:", "")

if st.button("Get Recommendations"):
    if quiz_id:
        recommendations = recommend_for_quiz(quiz_id)
        st.write("### Recommended Users:")
        for user in recommendations:
            st.write(f"✅ User: {user}")
    else:
        st.error("Please enter a valid Quiz ID.")
