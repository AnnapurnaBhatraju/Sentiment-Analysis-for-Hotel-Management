import streamlit as st
from textblob import TextBlob
import pandas as pd

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


          
