import streamlit as st
import requests

# Define the API URL of the back-end server
# Replace with the public URL of your backend, or use localhost if testing locally
API_URL = "http://localhost:5000/send_sms"  # Example: "https://your-backend-url.com/send_sms"

# Streamlit app title and description
st.title("SMS Automation System")
st.markdown("""
This app allows you to send bulk SMS using an automated backend.  
Simply provide the recipient numbers and the message, and let the system handle the rest.
""")

# Input fields for recipients and message
recipients = st.text_area(
    "Enter recipient phone numbers (comma-separated):",
    placeholder="e.g., +1234567890, +0987654321"
)
message = st.text_area(
    "Enter the SMS message:",
    placeholder="Hello! This is a test SMS from an automated system."
)

# Button to trigger SMS sending
if st.button("Send SMS"):
    if not recipients or not message:
        st.error("Both recipient phone numbers and message are required.")
    else:
        # Prepare data for the API
        data = {
            "recipients": [num.strip() for num in recipients.split(",")],
            "message": message
        }

        # Call the backend API
        try:
            st.info("Sending SMS...")
            response = requests.post(API_URL, json=data)

            # Handle API response
            if response.status_code == 200:
                st.success("SMS sent successfully!")
            else:
                st.error(f"Failed to send SMS. Error: {response.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error connecting to the backend server: {e}")

