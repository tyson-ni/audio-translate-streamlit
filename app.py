import streamlit as st
import openai
import os

if 'OPENAI_API_KEY' in os.environ:
    openai.api_key = os.getenv("OPENAI_API_KEY")
else:
    openai.api_key = st.secrets['OPENAI_API_KEY']

# Function to identify text using GPT-4
def identify_and_translate(text):
    response = openai.ChatCompletion.create(
        model = 'gpt-4',
        messages = [
            {'role': 'system', 'content': """
                You will identify the language of the text and translate it into English. 
                <Example>
                User Input: 我明天打算在家休息。
                Language: Chinese
                Translation: I plan to rest at home tomorrow.
                </Example>
             """},
            {'role': 'user', 'content': "Text: {}".format(text)}
        ],
        temperature=0.0
    )
    return  response['choices'][0]['message']['content']

# Function to translate and transcribe audio using Whisper API
def process_audio(audio, mode):
    # Transcribe audio
    transcription = openai.Audio.transcribe("whisper-1", audio) ['text']
    # Identify language and translate
    translation = identify_and_translate(transcription)
    output = '{}'.format(translation)
    #output += '\n Translation: {}'.format(openai.Audio.translate("whisper-1", audio) ['text'])
    return(output)

# Main section
st.header("Audio Translate and Transcribe")

# Upload audio and run translation or transcription
file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])
if file is not None:
    mode = st.selectbox("Select Mode", ["Translate", "Transcribe"])
    output = process_audio(file, mode)
    st.text_area("Output", value=output)