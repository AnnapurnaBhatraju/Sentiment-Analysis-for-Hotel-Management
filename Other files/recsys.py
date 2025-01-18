import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob

# Sample recommendations for preferences
recommendations = {
    "Dining": [
        "Veg - Today's special Paneer Biryani is a must-try!",
        "Non-Veg - Try out our exclusive range of Indian non-vegetarian food.",
        "Cafe - Never forget to have a cappuccino.",
        "Bar - Must taste premium foreign brands."
    ],
    "Spa": [
        "Relax with our Swedish massage therapy.",
        "Enjoy a refreshing aromatherapy session.",
        "Indulge in a rejuvenating facial treatment."
    ],
    "Activities": [
        "Join our morning yoga sessions.",
        "Try kayaking at the nearby lake.",
        "Sign up for a guided hiking tour."
    ]
}

# DataFrame to store guest details
try:
    guest_data = pd.read_csv('guest_feedback_data.csv')
except FileNotFoundError:
    guest_data = pd.DataFrame(columns=['Email', 'Feedback', 'Sentiment', 'Preferences'])

# UI Layout
st.title("Guest Experience Recommendation System")

# Step 1: Enter Guest Email
email = st.text_input("Enter your email:")
if email:
    st.write("Welcome! Please share your feedback below.")

# Step 2: Feedback Input
feedback = st.text_area("Enter your feedback about your experience:")
if st.button("Submit Feedback"):
    if feedback:
        # Analyze sentiment
        sentiment = TextBlob(feedback).sentiment.polarity
        sentiment_label = "Positive" if sentiment > 0 else "Negative"
        
        # Display sentiment analysis result
        if sentiment_label == "Negative":
            st.error("We're sorry for the inconvenience caused. Thank you for your feedback!")
        else:
            st.success("Thank you for your positive feedback!")
        
        # Save feedback to the DataFrame
        new_data = {"Email": email, "Feedback": feedback, "Sentiment": sentiment_label, "Preferences": ""}
        guest_data = pd.concat([guest_data, pd.DataFrame([new_data])], ignore_index=True)
        guest_data.to_csv('guest_feedback_data.csv', index=False)
    else:
        st.warning("Please enter your feedback before submitting!")

# Step 3: Preferences Selection
preferences = st.multiselect("Select your preferences:", options=list(recommendations.keys()))
if preferences and st.button("Get Recommendations"):
    # Update preferences in the DataFrame
    guest_data.loc[guest_data['Email'] == email, 'Preferences'] = ", ".join(preferences)
    guest_data.to_csv('guest_feedback_data.csv', index=False)

    # Display recommendations
    st.subheader("Here are our recommendations for you:")
    for pref in preferences:
        st.write(f"**{pref}:**")
        for rec in recommendations[pref]:
            st.write(f"- {rec}")
    
    # Final message
    st.write("**Have a great stay!**")

# Step 4: View Existing Data
if st.button("Show Existing Guest Data"):
    if guest_data.empty:
        st.write("No guest data found.")
    else:
        st.write(guest_data)
