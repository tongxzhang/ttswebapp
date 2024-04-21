# tts webapp

# Import necessary libraries
import streamlit as st
import requests
from requests.exceptions import RequestException, HTTPError

# Constants for API usage
API_URL = 'https://api.openai.com/v1/audio/speech'
VOICES = ('Alloy', 'Echo', 'Fable', 'Onyx', 'Nova', 'Shimmer')

# Set up the Streamlit app title and input fields
st.title('TTS with Tong')
st.markdown("Please enter your OpenAI API key, text for speech synthesis, desired voice, then click to generate audio :)")

# Create input fields for API key, text, and voice selection
api_key = st.text_input("OpenAI API key", type="password")
user_input = st.text_area("Text")
voice = st.selectbox("Choose your voice", VOICES)

# Define behaviour upon clicking the button to generate audio
if st.button('Generate to listen and download'):
    # Check if both API key and text input are provided
    if user_input and api_key:
        # Prepare headers and data for the OpenAI API request
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {
            'model': 'tts-1', 
            'input': user_input,
            'voice': voice,
        }

        try:
            # Send POST request to OpenAI API endpoint
            response = requests.post(API_URL, headers=headers, json=data)
            response.raise_for_status()  # Raise an error if the HTTP request returns an unsuccessful status code
            
            # Assuming that a successful response contains an audio file
            if response.status_code == 200:
                # Play the audio directly in the app
                st.audio(response.content, format='audio/mpeg')
            else:
                # Display error message if speech generation fails
                st.error(f"Failed to generate speech: {response.reason}")
        except HTTPError as http_err:
            # Handle HTTP errors
            st.error(f"HTTP error occurred: {http_err}")
        except RequestException as err:
            # Handle other request-related errors
            st.error(f"An error occurred: {err}")
        except Exception as e:
            # Handle unexpected errors
            st.error(f"An unexpected error occurred: {e}")
    else:
        # Display error message if API key or text input is missing
        st.error("Please ensure you have entered an API key and text.")

# st.markdown("Created by TZ © 2024")