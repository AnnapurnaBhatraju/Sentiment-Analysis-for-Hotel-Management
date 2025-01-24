import streamlit as st
from textblob import TextBlob
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json  # For loading secrets

# Load secrets from the JSON file
def load_secrets(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Load negative areas from a file
def load_negative_areas(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Load secrets
secrets = load_secrets("secrets.json")
SENDER_EMAIL = secrets["email"]
APP_PASSWORD = secrets["app_password"]
STAFF_EMAIL = secrets["receiver_email"]

# Slack Webhook URL
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# Mock recommendation data
RECOMMENDATIONS = {
    "Dining 🍽️": [
        "Veg: Today's special Paneer Biryani is a must-try!",
        "Non-Veg: Explore our exclusive range of Indian non-vegetarian delicacies.",
        "Cafe: Don’t miss our signature cappuccino and pastries.",
        "Bar: Relish premium foreign wines and craft cocktails.",
    ],
    "Spa 🧖‍♀️": [
        "Massage: Experience our signature hot stone massage for ultimate relaxation.",
        "Facial: Try our rejuvenating gold facial for glowing skin.",
        "Aromatherapy: Immerse yourself in soothing essential oil treatments.",
    ],
    "Gym 🏋️": [
        "Equipment: Utilize our advanced treadmills and elliptical machines.",
        "Classes: Join yoga, Zumba, or aerobics for a fun workout.",
        "Personal Training: Work with our certified fitness trainers.",
    ],
    "Pool 🏊‍♀️": [
        "Swimming: Take a dip in our temperature-controlled pool.",
        "Poolside: Enjoy tropical cocktails and snacks by the pool.",
        "Activities: Participate in aqua aerobics or pool volleyball games.",
    ],
    "Beauty Parlor 💇‍♀💄️": [
        "Hair: Get a stylish haircut or a nourishing hair spa.",
        "Skin: Pamper yourself with a detox facial or hydrating face mask.",
        "Makeup: Opt for a glamorous makeover for special occasions.",
    ],
    "Kid's Park 🎠": [
        "Play Area: Let kids enjoy swings, slides, and trampolines.",
        "Activities: Sign up for arts, crafts, or storytelling sessions.",
        "Fun Events: Participate in treasure hunts and competitions.",
    ],
    "Luxury Rooms 🛌": [
        "Suite: Upgrade to a room with a private Jacuzzi and scenic views.",
        "Family Rooms: Enjoy spacious accommodations for the whole family.",
        "Perks: Complimentary breakfast and evening snacks.",
    ],
    "Theater 🎭": [
        "Movies: Watch the latest blockbusters with surround sound.",
        "Live Shows: Enjoy live music, drama, and comedy shows.",
        "Private Booking: Book the theater for private movie nights.",
    ],
    "Waiting Halls 🛋️": [
        "Seating: Relax in plush seating with free Wi-Fi.",
        "Refreshments: Complimentary tea, coffee, and snacks available.",
        "Entertainment: Enjoy magazines, newspapers, or TV while waiting.",
    ],
    "Club 🎉": [
        "Music: Dance to live DJ performances and trending tracks.",
        "Drinks: Explore an extensive menu of cocktails and mocktails.",
        "Ambiance: Enjoy a chic setting with rooftop views.",
    ],
    "Sports Area ⚽": [
        "Indoor: Play table tennis, chess, or carrom indoors.",
        "Outdoor: Enjoy tennis, badminton, or basketball courts.",
        "Tournaments: Participate in seasonal sports tournaments.",
    ],
    "Stand-up Comedy 🎤": [
        "Shows: Attend comedy gigs featuring top comedians.",
        "Open-Mic: Try your hand at stand-up during open-mic nights.",
        "Themes: Enjoy humor tailored to specific themes and occasions.",
    ],
    "Parking Area 🅿️": [
        "Security: Park with 24/7 surveillance and attendants.",
        "Facilities: Use dedicated electric vehicle charging stations.",
        "Space: Plenty of parking for all vehicle types.",
    ],
    "Responsive Staff 🤝": [
        "Service: Call for 24/7 in-room dining or housekeeping.",
        "Assistance: Get help with travel bookings and local tours.",
        "Support: Immediate response to queries or complaints.",
    ],
    "Other Activities 🎨": [
        "Tours: Join local area guided tours to explore nearby attractions.",
        "Adventure: Book an adventure trip with experienced guides.",
        "Culture: Enjoy curated cultural and heritage walks.",
    ],
}


# Sentiment Analysis Function
def analyze_sentiment(feedback):
    negative_areas = load_negative_areas('negative_areas.txt')
    analysis = TextBlob(feedback)
    sentiment = "Positive 😊" if analysis.sentiment.polarity > 0 else "Negative 😟"
    
    areas_of_concern = []
    if sentiment == "Negative 😟":
        for area in negative_areas:
            if area.lower() in feedback.lower():
                areas_of_concern.append(area)
    
    return sentiment, areas_of_concern

# Email Sending Function
def send_email(subject, body_html):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = STAFF_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body_html, "html"))
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

# Slack Sending Function
def send_to_slack(message):
    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        st.error(f"Failed to send Slack message: {response.status_code}, {response.text}")

# Streamlit UI
st.title("Guest Experience Personalization System ✨")

st.header("Guest Details and Feedback 📝")
name = st.text_input("Name")
email = st.text_input("Email 📧")
feedback = st.text_area("Feedback 💬")

if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "sentiment" not in st.session_state:
    st.session_state.sentiment = None
if "areas_of_concern" not in st.session_state:
    st.session_state.areas_of_concern = []
if "preferences" not in st.session_state:
    st.session_state.preferences = []

submit_feedback = st.button("Submit Feedback")

if submit_feedback and name and email and feedback:
    sentiment, areas_of_concern = analyze_sentiment(feedback)
    st.session_state.submitted = True
    st.session_state.sentiment = sentiment
    st.session_state.areas_of_concern = areas_of_concern

if st.session_state.submitted:
    st.subheader("Sentiment Analysis Result :")
    st.write(f"Sentiment: {st.session_state.sentiment}")
    if st.session_state.sentiment == "Negative 😟":
        st.write("Identified Areas of Concern 🚩:")
        for area in st.session_state.areas_of_concern:
            st.write(f"- {area}")
        st.write("Sorry for the inconvenience caused!")
    else:
        st.write("Thank you for your positive feedback! 😊")

st.subheader("Select Your Preferences ⭐")
preferences = st.multiselect(
    "Choose your preferences (one or more):",
    list(RECOMMENDATIONS.keys()),
    default=st.session_state.preferences
)
st.session_state.preferences = preferences

if preferences:
    get_recommendations = st.button("Get Recommendations")
    if get_recommendations:
        st.subheader(f"Personalized Recommendations for our beloved guest {name} 🌟")
        recommendations_text = ""
        recommendations_html = ""
        for pref in preferences:
            st.write(f"{pref}:")
            recommendations_text += f"{pref}:\n"
            recommendations_html += f"<h4>{pref}:</h4>"
            for rec in RECOMMENDATIONS.get(pref, []):
                st.write(f"• {rec}")
                recommendations_text += f"- {rec}\n"
                recommendations_html += f"<li>{rec}</li>"
        
        subject = "🚨 Action Required: Guest Feedback Alert 🚨" if st.session_state.sentiment == "Negative 😟" else "🎊🎉 Guest satisfied by our Hospitality! 🎊🎉"
        if st.session_state.sentiment == "Negative 😟":
            areas_text = "\n".join([f"- {area}" for area in st.session_state.areas_of_concern])
            areas_html = "".join([f"<li>{area}</li>" for area in st.session_state.areas_of_concern])
            body_html = f"""
            <h3>Action Required!🚨</h3>
            <p><b>Guest Name:</b> {name}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Feedback:</b> {feedback}</p>
            <p><b>Sentiment:</b> {st.session_state.sentiment}</p>
            <p><b>Areas Responsible for Negative Feedback:</b></p>
            <ul>{areas_html}</ul>
            <h4>Generated Recommendations:</h4>
            <ul>{recommendations_html}</ul>
            """
            slack_message = f"🚨 *Action Required* 🚨\n\n*Guest Name*: {name}\n*Email*: {email}\n*Feedback*: {feedback}\n*Sentiment*: {st.session_state.sentiment}\n*Areas Responsible for Negative Feedback*:\n{areas_text}\n\n*Generated Recommendations*:\n{recommendations_text}"
        else:
            body_html = f"""
            <h3>🥳 Positive Guest Feedback Received</h3>
            <p><b>Guest Name:</b> {name}</p>
            <p><b>Email:</b> {email}</p>
            <p><b>Feedback:</b> {feedback}</p>
            <p><b>Sentiment:</b> {st.session_state.sentiment}</p>
            <h4>Generated Recommendations:</h4>
            <ul>{recommendations_html}</ul>
            """
            slack_message = f"🥳 *Positive Guest Feedback Received* 🥳\n\n*Guest Name*: {name}\n*Email*: {email}\n*Feedback*: {feedback}\n*Sentiment*: {st.session_state.sentiment}\n\n*Generated Recommendations*:\n{recommendations_text}"
        
        send_email(subject, body_html)
        send_to_slack(slack_message)
        st.success("Email and Slack notifications sent to staff successfully! 📤")
else:
    st.warning("Please select at least one preference. ⚠️")
