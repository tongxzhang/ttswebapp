# tts webapp

# Import necessary libraries
import streamlit as st
import requests
from requests.exceptions import RequestException, HTTPError
# [WIP for pydub and io]
# from pydub import AudioSegment # Handle audio operations
# import io # Handle in-memory audio files

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
        response.raise_for_status() # Raise an error if the HTTP request returns an unsuccessful status code
        return True, response.content # success=True, return audio content from successful request
    except HTTPError:
        return False, "Failed to generate due to a server error. Please check your API key and try again." # success=False, return error message from successful request
    except RequestException:
        return False, "Failed to generate due to a network error. Please check your connection and try again." # Handle other request-related errors
    except Exception as e:
        return False, "An unexpected error occurred. Please try again later." # Handle unexpected errors

# # [WIP] Function to split text above the 4096 API character limit into chunks
# def split_text_by_limit(text, limit=4096):
#     words = text.split()
#     # Initialise empty lists
#     text_chunks = []
#     current_text_chunk = []
#     current_length = 0

#     for word in words:
#         if current_length + len(word) + 1 > limit:
#             text_chunks.append(' '.join(current_text_chunk))
#             current_text_chunk = [word]
#             current_length = len(word)
#         else:
#             current_text_chunk.append(word)
#             current_length += len(word) + 1 # +1 for space
    
#     text_chunks.append(' '.join(current_text_chunk)) # add the last chunk
#     return text_chunks

# # [WIP] Function to concatenate audio segments
# def concatenate_audio_segments(audio_segments):
#     combined = AudioSegment.empty()
#     for segment in audio_segments:
#         combined += segment
#     return combined

# Main function to run the Streamlit app, setting up the UI and managing user interactions
def main():
    # Set up the Streamlit app title and input fields
    st.title('Text to Speech Converter')
    st.markdown("Please enter your OpenAI API key*, text for speech synthesis, [desired voice](https://platform.openai.com/docs/guides/text-to-speech/voice-options), then click to generate audio :)")

    # Create input fields for API key, text, character counter, and voice selection
    api_key = st.text_input("OpenAI API key:", type="password")

    user_input = st.text_area("Text to be converted into speech:")
    character_counter = f"<span style='display: block; text-align: right; color: grey; font-size: 0.8em;'>Character count: {len(user_input)}</span>"
    st.markdown(character_counter, unsafe_allow_html=True)
    
    voice = st.selectbox("Chosen voice:", VOICES)
    
    # Rates per 1000 characters for each quality model
    rates = {
        'Standard': 0.015,  # $0.015 per 1000 characters
        'HD': 0.03  # $0.03 per 1000 characters
    }

    # Function to calculate costs based on text length
    def calculate_costs(text_length, rates):
        costs = {}
        for model, rate in rates.items():
            cost = (text_length / 1000) * rate
            rounded_cost = round(cost, 3)  # Round to nearest $0.001
            costs[model] = rounded_cost
        return costs

    # Function to update model choices with dynamic costs
    def update_model_choices(text_length):
        costs = calculate_costs(text_length, rates)
        model_choices = {
            f'Standard, for most use cases (${costs["Standard"]})': 'tts-1',
            f'HD, for studio quality (${costs["HD"]})': 'tts-1-hd'
        }
        return model_choices

    # Define a dictionary to map friendly labels to API model identifiers
    model_choices = update_model_choices(len(user_input))
    # Update the Streamlit radio button for model choice to use the dictionary keys
    model_label = st.radio("Chosen quality and estimated cost:", options=list(model_choices.keys()))
    # Use the dictionary to get the corresponding model identifier in the API call
    model_choice = model_choices[model_label]

    # Define behaviour upon clicking the button to generate audio
    if st.button('Generate to play and download'):
        if user_input and api_key:
            # Check if the text exceeds the limit and split if necessary
            # Case 1 (simple) where user input does not exceed API character limit 
            if len(user_input) <= 4096:
                # Call generate_audio(). Unpack tuple into two variables: success (True/False) and content_or_message
                # 'content_or_message' captures either the audio data or error message depending on the outcome of the API request 
                success, content_or_message = generate_audio(api_key, user_input, voice, model_choice)
                if success:
                    st.audio(content_or_message, format='audio/mpeg') # Play audio content directly in the app
                else:
                    st.error(content_or_message) # Display error message if speech generation fails
            
            # Case 2 where user input exceeds API character limit 
            else:
                st.error("At this stage OpenAI's API only supports up to 4096 characters. We're currently working on a solution.")
                # # [WIP] Split the user input text into manageable chunks that do not exceed the API character limit
                # text_chunks = split_text_by_limit(user_input)
                # audio_segments = []

                # # Iterate over each chunk of text
                # for chunk in text_chunks:
                #     # Attempt to generate audio for the current chunk of text using the OpenAI API
                #     success, content_or_message = generate_audio(api_key, chunk, voice, model_choice)
                #     if success:
                #         audio_segments.append(AudioSegment.from_file(io.BytesIO(content_or_message), format='mp3')) # If the API call was successful, convert the audio content to a segment and add it to the list
                #     else:
                #         st.error(content_or_message) # If the API call failed, display an error message and stop processing further chunks
                #         break
                
                # # After processing all chunks, check if there are any audio segments collected
                # if audio_segments:
                #     final_audio = concatenate_audio_segments(audio_segments) # Concatenate all audio segments into one final audio file
                #     final_audio_file = io.BytesIO() # Create an in-memory file-like object to hold the concatenated audio
                #     final_audio.export(final_audio_file, format='mp3')
                #     final_audio_file.seek(0) # Reset the file pointer to the beginning of the file-like object
                #     st.audio(final_audio_file, format='audio/mpeg') # Stream the final audio directly in the app, allowing the user to play and download it
                
                # # If no audio segments were created (all API calls failed), display error message
                # else:
                #     st.error("Failed to generate all required audio. Please try again later.")
        else:
            st.error("Please ensure you have entered an API key and text.") # Display error message if API key or text input is missing
    else:
        pass # Placeholder for any additional instructions or UI elements when the button has not been clicked

# Note: This conditional checks if this script is being run directly by Python or being imported as a module into another script
# Commonly used to place script execution code (tests, command-line processing) which should only occur when the script is not being imported as a module elsewhere
if __name__ == "__main__":
    main()  # Call the main function to execute primary functionality of the script

st.markdown("*We ask for this because sadly I can't afford to pay for everyone's usage yet. Create your keys [here](https://platform.openai.com/api-keys) and revoke them when you're done to be extra safe.", unsafe_allow_html=True)
st.markdown("Created by [Tong Zhang](https://linktr.ee/tongzhang) © 2024")
# streamlit run ttsapp.py # Run locally