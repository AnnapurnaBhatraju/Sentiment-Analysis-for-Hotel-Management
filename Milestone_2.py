# Import Libraries and Load Environment Variables

import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("GROQCLOUD_API_KEY")

# Define the API URL and headers for GroqCloud API
api_url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}


# Load Negative Areas Function

# Load negative areas from a file
def load_negative_areas(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Process Feedback Function

# Function to process feedback and analyze sentiment
def process_feedback(feedback):
    # Define the task prompt that trains the model using the feedback
    task_prompt = (
        "You are a highly advanced AI model tasked with analyzing customer feedback "
        "to identify areas that caused dissatisfaction. Focus on key aspects of the experience, such as "
        "dining, cleanliness, staff behavior, room amenities, parking facilities, and other service-related "
        "issues. For each piece of feedback, identify whether the sentiment is positive or negative. "
        "If negative, highlight specific aspects mentioned in the feedback that contributed to the dissatisfaction. "
        "Provide a structured response indicating the sentiment and the areas of concern."
    )
        
    # Load the negative areas from the file
    negative_areas = load_negative_areas('negative_areas.txt')  
    # Create the input payload for the API request
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": f"Analyze the sentiment of the following feedback: '{feedback}'. Return a sentiment (Positive or Negative)."
            }
        ]
    }

    # Make a POST request to GroqCloud's API
    response = requests.post(api_url, headers=headers, json=data)

    # Check if the response is successful and process the result
    if response.status_code == 200:
        result = response.json()  # If successful, process the response data
        print("\nAPI Response:", result)  # Debugging step to inspect the actual response structure
        
        # Extract the sentiment from the response
        try:
            sentiment = result['choices'][0]['message']['content'].strip()  # Adjusted indexing
            print(f"Sentiment: {sentiment}")
            
            found_areas = []
            if "negative" in sentiment.lower():
                print("Negative sentiment detected. Analyzing areas that caused negative feedback...")
                
                # Compare feedback with the negative areas
                found_areas = [area for area in negative_areas if area.lower() in feedback.lower()]
                
                if found_areas:
                    print("\nNegative feedback related to:")
                    for area in found_areas:
                        print(f"- {area}")
                else:
                    print("No specific areas of negative feedback identified.")
                
                # Generate an alert for negative sentiment or service issues
                generate_alert(feedback, found_areas)
            
            # Create the dictionary to store results
            feedback_analysis = {
                'sentiment': 'Negative' if "negative" in sentiment.lower() else 'Positive',
                'areas identified': found_areas
            }
            
            # Print the dictionary
            print("\nFeedback Analysis Dictionary:")
            print(feedback_analysis)
            
        except (IndexError, KeyError) as e:
            print("Unexpected API response structure:", e)
    else:
        print(f"Error: {response.status_code}, {response.text}")

# Generate Alert Function

# Function to generate an alert
def generate_alert(feedback, found_areas):
    # Generate a detailed alert including the negative areas
    print(f"\nALERT GENERATED: Immediate attention required for the following feedback:")
    print(f"Feedback: {feedback}")
    if found_areas:
        print("\nIdentified issues in the following areas:")
        for area in found_areas:
            print(f"- {area}")
    else:
        print("No specific areas identified, but negative sentiment detected.")
   
# Main Function

# Main function to get user input and process feedback
def main():
    # Input: Dynamic user feedback
    feedback = input("Please enter your feedback: ")
    
    # Call the function to process feedback
    process_feedback(feedback)

# Run the main function
main()

















