import streamlit as st
import speech_recognition as sr

# Define custom CSS for dark mode
dark_mode_css = """
<style>
body {
    background-color: #1e1e1e;
    color: white;
}
.stApp {
    background-color: #1e1e1e;
    color: white;
}
.stSidebar {
    background-color: #333333;
    color: white;
}
header, .css-1v3fvcr, .css-18e3th9 {
    background-color: #333333 !important;
    color: white !important;
}
button, .stButton button {
    background-color: #555555;
    color: white;
    border-color: #555555;
}
</style>
"""

# Define custom CSS for light mode
light_mode_css = """
<style>
body {
    background-color: white;
    color: black;
}
.stApp {
    background-color: white;
    color: black;
}
.stSidebar {
    background-color: #f0f0f5;
    color: black;
}
header, .css-1v3fvcr, .css-18e3th9 {
    background-color: #f0f0f5 !important;
    color: black !important;
}
button, .stButton button {
    background-color: #e0e0e0;
    color: black;
    border-color: #cccccc;
}
</style>
"""

# CSS for the toggle switch
toggle_switch_css = """
<style>
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

/* Sun and moon icons */
.slider:after {
  content: '☀️';
  position: absolute;
  left: 8px;
  bottom: 4px;
}

input:checked + .slider:after {
  content: '🌙';
  left: 32px;
}
</style>
"""

# Add the toggle switch CSS
st.markdown(toggle_switch_css, unsafe_allow_html=True)

# Initialize session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Toggle switch for dark/light mode
toggle = st.sidebar.checkbox("Toggle Dark/Light Mode", value=st.session_state.dark_mode)
st.session_state.dark_mode = toggle

# Apply the chosen theme
if st.session_state.dark_mode:
    st.markdown(dark_mode_css, unsafe_allow_html=True)
else:
    st.markdown(light_mode_css, unsafe_allow_html=True)

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