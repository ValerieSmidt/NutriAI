import streamlit as st
import speech_recognition as sr

st.title("Voice-Based Nutrition Specialist Chatbot")

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

def get_audio():
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source, phrase_time_limit=5)
    try:
        text = r.recognize_google(audio)
        st.write(f"User said: {text}")
        return text
    except sr.UnknownValueError:
        st.write("Sorry, I did not get that. Could you please repeat?")
        return None
    except sr.RequestError as e:
        st.write(f"Could not request results; {e}")
        return None

if st.button('Speak'):
    st.write("Please speak into the microphone.")
    question = get_audio()
    if question:
        st.write(f"You said: {question}")
        # Here you would integrate with your chatbot model

# Placeholder for chatbot response
st.write("Bot response will be shown here.")