import streamlit as st
import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# File path for storing guest data as CSV
csv_file_path = 'guest_experience.csv'

# Check if the CSV file exists, and if not, create it
def initialize_csv():
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        # Create an empty dataframe and save it as CSV
        df = pd.DataFrame(columns=["Customer_ID", "Name", "Email", "Phone_Number", "Checkin_Date", "Checkout_Date", 
                                   "Duration_of_Stay", "Preferences", "Review", "Rating"])
        df.to_csv(csv_file_path, index=False)

# Function to add new guest data to the CSV file
def add_guest_data(customer_id, name, email, phone_number, checkin_date, checkout_date, duration_of_stay, preferences, review, rating):
    # Read the existing data from the CSV file
    df = pd.read_csv(csv_file_path)

    # Check if the Customer_ID already exists
    if customer_id in df['Customer_ID'].values:
        return "Customer ID already exists. Please use a unique ID."

    # Add new entry to the dataframe
    new_entry = {
        "Customer_ID": customer_id,
        "Name": name,
        "Email": email,
        "Phone_Number": phone_number,
        "Checkin_Date": checkin_date,
        "Checkout_Date": checkout_date,
        "Duration_of_Stay": duration_of_stay,
        "Preferences": preferences,
        "Review": review,
        "Rating": rating
    }

    df = df.append(new_entry, ignore_index=True)

    # Save the updated dataframe back to the CSV
    df.to_csv(csv_file_path, index=False)

    return "Data submitted successfully!"

# Cosine Similarity & TF-IDF Vectorizer for Recommendations
def get_recommendations(preferences_input, review_input):
    # Retrieve all reviews and preferences from the CSV file
    df = pd.read_csv(csv_file_path)

    # Combine preferences and review for all records
    data_combined = df['Preferences'] + " " + df['Review']

    # Add the new preferences and review to the list for comparison
    data_combined = data_combined.tolist() + [preferences_input + " " + review_input]

    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(data_combined)

    # Calculate cosine similarity between the new input and existing data
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    # Sort the similarities and get the indices of the most similar guests
    similar_indices = cosine_sim.argsort()[0, ::-1]
    
    # Return the most similar guest data
    recommendations = []
    for idx in similar_indices[:5]:  # Get top 5 similar records
        recommendations.append(df.iloc[idx])

    return recommendations

# Streamlit UI
st.title("Guest Experience Data Entry")

# Initialize the CSV file if not already present
initialize_csv()

# Input fields
customer_id = st.text_input("Customer ID", "")
name = st.text_input("Name", "")
email = st.text_input("Email", "")
phone_number = st.text_input("Phone Number", "")
checkin_date = st.date_input("Check-in Date", datetime.today())
checkout_date = st.date_input("Check-out Date", datetime.today())
duration_of_stay = st.number_input("Duration of Stay (in days)", min_value=1, max_value=30, value=1)
preferences = st.text_area("Preferences", "")
review = st.text_area("Review", "")
rating = st.slider("Rating (1-5)", min_value=1, max_value=5)

# Button to insert data
if st.button("Submit Data"):
    try:
        # Add guest data to CSV and handle unique ID constraint
        result = add_guest_data(customer_id, name, email, phone_number, checkin_date, checkout_date, 
                                duration_of_stay, preferences, review, rating)
        st.write(result)

        if result == "Data submitted successfully!":
            # Get Recommendations based on preferences and review
            recommendations = get_recommendations(preferences, review)
            if recommendations:
                st.write("Here are some personalized recommendations for similar guests:")
                for rec in recommendations:
                    st.write(f"Customer ID: {rec['Customer_ID']}, Name: {rec['Name']}, Rating: {rec['Rating']}")
            else:
                st.write("No recommendations found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display existing data in the database
if st.button("Show Existing Guests Data"):
    df = pd.read_csv(csv_file_path)
    if not df.empty:
        st.write(df)
    else:
        st.write("No guest data found.")

# Reset button to clear the CSV data (optional)
if st.button("Reset Database"):
    confirm_reset = st.checkbox("Are you sure you want to reset the database? This will delete all data.")
    if confirm_reset:
        df = pd.DataFrame(columns=["Customer_ID", "Name", "Email", "Phone_Number", "Checkin_Date", "Checkout_Date", 
                                   "Duration_of_Stay", "Preferences", "Review", "Rating"])
        df.to_csv(csv_file_path, index=False)
        st.warning("Database has been reset.")
