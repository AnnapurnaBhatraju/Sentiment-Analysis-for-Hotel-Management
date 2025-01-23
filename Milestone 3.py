import streamlit as st
from textblob import TextBlob
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Recommendations 
recommendations = {
    "Dining": [
        "Veg: Today's special Paneer Biryani is a must-try!",
        "Non-Veg: Explore our exclusive range of Indian non-vegetarian delicacies.",
        "Cafe: Don’t miss our signature cappuccino and pastries.",
        "Bar: Relish premium foreign wines and craft cocktails.",
    ],
    "Spa": [
        "Massage: Experience our signature hot stone massage for ultimate relaxation.",
        "Facial: Try our rejuvenating gold facial for glowing skin.",
        "Aromatherapy: Immerse yourself in soothing essential oil treatments.",
    ],
    "Gym": [
        "Equipment: Utilize our advanced treadmills and elliptical machines.",
        "Classes: Join yoga, Zumba, or aerobics for a fun workout.",
        "Personal Training: Work with our certified fitness trainers.",
    ],
    "Pool": [
        "Swimming: Take a dip in our temperature-controlled pool.",
        "Poolside: Enjoy tropical cocktails and snacks by the pool.",
        "Activities: Participate in aqua aerobics or pool volleyball games.",
    ],
    "Beauty Parlor": [
        "Hair: Get a stylish haircut or a nourishing hair spa.",
        "Skin: Pamper yourself with a detox facial or hydrating face mask.",
        "Makeup: Opt for a glamorous makeover for special occasions.",
    ],
    "Kid's Park": [
        "Play Area: Let kids enjoy swings, slides, and trampolines.",
        "Activities: Sign up for arts, crafts, or storytelling sessions.",
        "Fun Events: Participate in treasure hunts and competitions.",
    ],
    "Luxury Rooms": [
        "Suite: Upgrade to a room with a private Jacuzzi and scenic views.",
        "Family Rooms: Enjoy spacious accommodations for the whole family.",
        "Perks: Complimentary breakfast and evening snacks.",
    ],
    "Theater": [
        "Movies: Watch the latest blockbusters with surround sound.",
        "Live Shows: Enjoy live music, drama, and comedy shows.",
        "Private Booking: Book the theater for private movie nights.",
    ],
    "Waiting Halls": [
        "Seating: Relax in plush seating with free Wi-Fi.",
        "Refreshments: Complimentary tea, coffee, and snacks available.",
        "Entertainment: Enjoy magazines, newspapers, or TV while waiting.",
    ],
    "Club": [
        "Music: Dance to live DJ performances and trending tracks.",
        "Drinks: Explore an extensive menu of cocktails and mocktails.",
        "Ambiance: Enjoy a chic setting with rooftop views.",
    ],
    "Sports Area": [
        "Indoor: Play table tennis, chess, or carrom indoors.",
        "Outdoor: Enjoy tennis, badminton, or basketball courts.",
        "Tournaments: Participate in seasonal sports tournaments.",
    ],
    "Stand-up Comedy": [
        "Shows: Attend comedy gigs featuring top comedians.",
        "Open-Mic: Try your hand at stand-up during open-mic nights.",
        "Themes: Enjoy humor tailored to specific themes and occasions.",
    ],
    "Parking Area": [
        "Security: Park with 24/7 surveillance and attendants.",
        "Facilities: Use dedicated electric vehicle charging stations.",
        "Space: Plenty of parking for all vehicle types.",
    ],
    "Responsive Staff": [
        "Service: Call for 24/7 in-room dining or housekeeping.",
        "Assistance: Get help with travel bookings and local tours.",
        "Support: Immediate response to queries or complaints.",
    ],
    "Other Activities": [
        "Tours: Join local area guided tours to explore nearby attractions.",
        "Adventure: Book an adventure trip with experienced guides.",
        "Culture: Enjoy curated cultural and heritage walks.",
    ],
}

# Predefined recommendations (as text descriptions for cosine similarity)
categories = {
    "Dining": "Enjoy a variety of vegetarian and non-vegetarian meals, including Indian and international dishes.",
    "Spa": "Relax with our range of therapeutic spa services such as massages, facials, and aromatherapy.",
    "Gym": "Work out in our state-of-the-art gym with a variety of fitness classes and personal training sessions.",
    "Pool": "Take a swim in our temperature-controlled pool or relax poolside with snacks and drinks.",
    "Beauty Parlor": "Pamper yourself with professional hair and beauty services, including facials, haircuts, and makeup.",
    "Kid's Park": "Let your children enjoy various outdoor and indoor activities such as swings, slides, and arts and crafts.",
    "Luxury Rooms": "Stay in our luxury suites with premium amenities like Jacuzzis, spacious rooms, and scenic views.",
    "Theater": "Watch the latest movies or enjoy live shows in our state-of-the-art theater with surround sound.",
    "Waiting Halls": "Relax in our comfortable waiting halls with free Wi-Fi, snacks, and entertainment options.",
    "Club": "Dance to the latest tunes or enjoy drinks and snacks in our trendy club with a chic ambiance.",
    "Sports Area": "Engage in sports such as tennis, badminton, and basketball, or enjoy indoor games like chess.",
    "Stand-up Comedy": "Attend comedy shows or participate in open-mic nights for a fun and relaxing evening.",
    "Parking Area": "Park your vehicle safely in our spacious parking area with dedicated spots for electric vehicles.",
    "Responsive Staff": "Our staff is available 24/7 for any assistance, including room service, travel bookings, and general queries.",
    "Other Activities": "Explore local attractions through guided tours, adventurous activities, and cultural experiences."
}

# TF-IDF Vectorizer setup
vectorizer = TfidfVectorizer(stop_words='english')

# DataFrame to store guest details
try:
    guest_data = pd.read_csv('guest_feedback_data.csv')
except FileNotFoundError:
    guest_data = pd.DataFrame(columns=['Email', 'Feedback', 'Sentiment', 'Preferences'])

# UI Layout
st.title("Guest Experience AI Recommendation System")

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

# Step 3: AI-based Recommendations Using Cosine Similarity
if feedback and st.button("Get AI Recommendations"):
    # Transform feedback and categories into vectors
    all_texts = list(categories.values()) + [feedback]
    vectors = vectorizer.fit_transform(all_texts)
    
    # Calculate cosine similarity between guest feedback and categories
    cosine_sim = cosine_similarity(vectors[-1], vectors[:-1])
    
    # Get the most similar categories based on cosine similarity
    top_indices = cosine_sim.argsort()[0][-3:][::-1]  # Get top 3 recommendations
    recommended_categories = [list(categories.keys())[i] for i in top_indices]

    # Display recommendations
    st.subheader("Here are our personalized recommendations for you:")
    for category in recommended_categories:
        st.write(f"**{category}:**")
        for rec in recommendations.get(category, []):
            st.write(f"- {rec}")

    st.write("**Have a great stay!**")

# Step 4: View Existing Data
if st.button("Show Existing Guest Data"):
    if guest_data.empty:
        st.write("No guest data found.")
    else:
        st.write(guest_data)

# Step 5: Delete Data
if st.button("Delete Guest Data"):
    if email:
        guest_data = guest_data[guest_data['Email'] != email]
        guest_data.to_csv('guest_feedback_data.csv', index=False)
        st.success("All data related to this email has been deleted.")
    else:
        st.warning("Please enter an email to delete data.")
