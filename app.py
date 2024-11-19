import streamlit as st
from appium import webdriver
import time
import random

# Streamlit app title and description
st.title("SMS Automation System")
st.write("""
This app automates the process of sending SMS using a VoIP app (e.g., TextNow) on an Android emulator.
""")

# Input fields for recipients and message
recipients = st.text_area("Enter recipient phone numbers (comma-separated):", "+1234567890, +0987654321")
message = st.text_area("Enter the SMS message:", "Hello! This is a test SMS from an automated system.")

# Configuration for Appium and Android emulator
APPIUM_SERVER_URL = "http://localhost:4723/wd/hub"
DESIRED_CAPS = {
    "platformName": "Android",
    "deviceName": "Android Emulator",
    "appPackage": "com.enflick.android.TextNow",  # Replace with the app's package name
    "appActivity": "com.textnow.activity.LauncherActivity",  # Replace with the app's activity
    "noReset": True
}

# Function to send an SMS using Appium
def send_sms(driver, recipient, message):
    try:
        # Open the new message screen
        driver.find_element_by_accessibility_id("New Message").click()
        time.sleep(2)

        # Input the recipient's number
        recipient_field = driver.find_element_by_id("com.enflick.android.TextNow:id/recipient")
        recipient_field.send_keys(recipient)
        time.sleep(1)

        # Input the message body
        message_field = driver.find_element_by_id("com.enflick.android.TextNow:id/message_body")
        message_field.send_keys(message)
        time.sleep(1)

        # Click send
        send_button = driver.find_element_by_id("com.enflick.android.TextNow:id/send_button")
        send_button.click()
        time.sleep(2)

        st.success(f"SMS sent to {recipient}.")
    except Exception as e:
        st.error(f"Failed to send SMS to {recipient}: {e}")

# Main logic to connect to Appium and send SMS to all recipients
if st.button("Send SMS"):
    if not recipients or not message:
        st.error("Please provide both recipients and a message.")
    else:
        st.info("Connecting to the Android emulator...")
        
        # Parse recipients
        recipient_list = [r.strip() for r in recipients.split(",")]

        # Connect to the Appium server
        try:
            driver = webdriver.Remote(APPIUM_SERVER_URL, DESIRED_CAPS)
            st.success("Connected to the Android emulator.")

            for recipient in recipient_list:
                send_sms(driver, recipient, message)
                time.sleep(random.randint(5, 10))  # Random delay to avoid detection

        except Exception as e:
            st.error(f"Failed to connect to Appium: {e}")
        finally:
            if 'driver' in locals():
                driver.quit()
