# tts webapp

# Import necessary libraries
import streamlit as st
import requests
from requests.exceptions import RequestException, HTTPError

# Constants for API usage
API_URL = 'https://api.openai.com/v1/audio/speech'
VOICES = ('alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer')

# Function to manage OpenAI API requests, exception handling, and audio or error message generation
# Returns a tuple (success, content_or_message). success: boolean indicating success of API call. content_or_message: audio content if successful, error message if not.
def generate_audio(api_key, text, voice, model):
    # Prepare headers and data for the OpenAI API request
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {
        'model': model, 
        'input': text,
        'voice': voice,
    }
    try:
        # Send POST request to OpenAI API endpoint
        response = requests.post(API_URL, headers=headers, json=data)
        # Raise an error if the HTTP request returns an unsuccessful status code
        response.raise_for_status()
        # success=True, return audio content from successful request
        return True, response.content
    except HTTPError: 
        # success=False, return error message from successful request
        return False, "Failed to generate due to a server error. Please check your API key and try again." # User-friendly error message
    except RequestException: 
        # Handle other request-related errors
        return False, "Failed to generate due to a network error. Please check your connection and try again."
    except Exception as e: 
        # Handle unexpected errors
        return False, "An unexpected error occurred. Please try again later."

# Main function to run the Streamlit app, setting up the UI and managing user interactions
def main():
    # Set up the Streamlit app title and input fields
    st.title('TTS with Tong')
    st.markdown("Please enter your OpenAI API key, text for speech synthesis, <a href='https://platform.openai.com/docs/guides/text-to-speech/voice-options' target='_blank'>desired voice</a>, then click to generate audio :)", unsafe_allow_html=True)

    # Create input fields for API key, text, character counter, and voice selection
    api_key = st.text_input("OpenAI API key:", type="password")
    user_input = st.text_area("Text to be converted into speech:")
    character_counter = f"<span style='display: block; text-align: right; color: grey; font-size: 0.8em;'>Character count: {len(user_input)}</span>"
    st.markdown(character_counter, unsafe_allow_html=True)
    voice = st.selectbox("Chosen voice:", VOICES)
    model_choice = st.radio("Standard vs HD quality (0.015 vs 0.03 USD / 1000 characters):", ('tts-1', 'tts-1-hd'))

    # Define behaviour upon clicking the button to generate audio
    if st.button('Generate to play and download'):
        if user_input and api_key:
            # Call generate_audio(). Unpack tuple into two variables: success (True/False) and content_or_message
            # content_or_message captures either the audio data or error message depending on the outcome of the API request 
            success, content_or_message = generate_audio(api_key, user_input, voice, model_choice)
            if success:
                # Play audio content directly in the app
                st.audio(content_or_message, format='audio/mpeg')
            else:
                # Display error message if speech generation fails
                st.error(content_or_message)
        else:
            # Display error message if API key or text input is missing
            st.error("Please ensure you have entered an API key and text.")
    else:
        # Placeholder for any additional instructions or UI elements when the button has not been clicked
        pass

# Note: This conditional checks if this script is being run directly by Python or being imported as a module into another script
# Commonly used to place script execution code (tests, command-line processing) which should only occur when the script is not being imported as a module elsewhere
if __name__ == "__main__":
    main()  # Call the main function to execute primary functionality of the script

# st.markdown("Created by TZ © 2024")
# streamlit run ttsapp.py # Run locally