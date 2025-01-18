import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# File path for storing guest data
# csv_file_path = 'guest_recommendations.csv'

csv_file_path = 'dataset for hotel management.csv'

# Initialize the CSV file
def initialize_csv():
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Customer_ID", "Name", "Email", "Preferences", "Review", "Rating"])
        df.to_csv(csv_file_path, index=False)

# Add guest data to CSV
def add_guest_data(customer_id, name, email, preferences, review, rating):
    # Create a new entry as a DataFrame
    new_entry = pd.DataFrame([{
        'Customer_ID': customer_id,
        'Name': name,
        'Email': email,
        'Preferences': preferences,
        'Review': review,
        'Rating': rating
    }])
    
    # If the file exists, load it and append the new entry
    try:
        df = pd.read_csv('guest_recommendations.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Customer_ID', 'Name', 'Email', 'Preferences', 'Review', 'Rating'])
    
    # Concatenate the new entry with the existing DataFrame
    df = pd.concat([df, new_entry], ignore_index=True)
    
    # Save the updated DataFrame back to the file
    df.to_csv('guest_recommendations.csv', index=False)
    return "Guest data added successfully!"


# Generate recommendations based on preferences and review
def get_recommendations(preferences_input, review_input):
    df = pd.read_csv(csv_file_path)

    if df.empty:
        return "No data available for recommendations."
    
    # Combine preferences and reviews into a single column
    combined_data = df['Preferences'] + " " + df['Review']
    combined_data = combined_data.tolist() + [preferences_input + " " + review_input]

    # TF-IDF vectorization and cosine similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(combined_data)
    cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # Find top 5 most similar records
    similar_indices = cosine_sim.argsort()[0, ::-1][:5]
    recommendations = []
    for idx in similar_indices:
        recommendations.append(df.iloc[idx])
    
    return recommendations

# Streamlit UI
st.title("Guest Experience Recommendation System")

# Initialize the CSV
initialize_csv()

# Predefined list of preferences
preferences_options = ["Spa", "Gym", "Pool", "Dining", "Kids' Club", "Room Service"]

# Input fields for guest details
st.subheader("Enter Guest Details:")
customer_id = st.text_input("Customer ID", "")
name = st.text_input("Name", "")
email = st.text_input("Email", "")
preferences = st.multiselect("Select Preferences", preferences_options)
review = st.text_area("Review", "")
rating = st.slider("Rating (1-5)", min_value=1, max_value=5)

# Submit data button
if st.button("Submit Data"):
    if not customer_id or not name or not email or not preferences:
        st.error("Please fill in all required fields.")
    else:
        preferences_str = ", ".join(preferences)
        result = add_guest_data(customer_id, name, email, preferences_str, review, rating)
        st.success(result)

# Recommendation section
st.subheader("Get Recommendations:")
selected_preferences = st.multiselect("Choose Preferences for Recommendations", preferences_options)
input_review = st.text_area("Enter Review for Recommendations", "")

if st.button("Get Recommendations"):
    if not selected_preferences:
        st.error("Please select at least one preference.")
    else:
        selected_preferences_str = ", ".join(selected_preferences)
        recommendations = get_recommendations(selected_preferences_str, input_review)

        if isinstance(recommendations, str):  # If no recommendations are found
            st.write(recommendations)
        else:
            st.write("Top Recommendations:")
            for rec in recommendations:
                st.write(f"Customer ID: {rec['Customer_ID']}, Name: {rec['Name']}, Preferences: {rec['Preferences']}, Rating: {rec['Rating']}")

# Show existing guest data
if st.button("Show Existing Guest Data"):
    df = pd.read_csv(csv_file_path)
    if df.empty:
        st.write("No guest data found.")
    else:
        st.write(df)

# Reset database
if st.button("Reset Database"):
    confirm_reset = st.checkbox("Are you sure you want to reset the database? This will delete all data.")
    if confirm_reset:
        df = pd.DataFrame(columns=["Customer_ID", "Name", "Email", "Preferences", "Review", "Rating"])
        df.to_csv(csv_file_path, index=False)
        st.warning("Database has been reset.")
