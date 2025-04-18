import streamlit as st
import os
from openai import OpenAI

client = OpenAI()

if 'OPENAI_API_KEY' in os.environ:
    client.api_key = os.getenv("OPENAI_API_KEY")
else:
    client.api_key = st.secrets['OPENAI_API_KEY']

# Function to identify text using GPT-4
def identify_and_translate(text):
    response = client.responses.create(
        model = 'gpt-4.1',
        input = [
            {'role': 'system', 'content': """
                You will identify the language of the text and translate it into English. If the conversation 
                <Example>
                User Input: 我明天打算在家休息。
                Language: Chinese /n
                Translation: I plan to rest at home tomorrow. /n
                Transcription: <Original Text>
                </Example>
             """},
            {'role': 'user', 'content': "Text: {}".format(text)}
        ],
        temperature=0.0
    )
    return  response.output_text

# Function to translate and transcribe audio using Whisper API
def process_audio(audio):
    # Transcribe audio
    transcription = client.audio.transcriptions.create(
        model="gpt-4o-transcribe",
        file=audio
    )
    # Identify language and translate
    translation = identify_and_translate(transcription.text)
    return(translation)

# Main section
st.header("Audio Translate and Transcribe")

# Upload audio and run translation or transcription
file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])
if file is not None:
    mode = st.selectbox("Select Mode", ["Translate", "Transcribe"])
    output = process_audio(file)
    st.text_area("Output", value=output)
