import streamlit as st
from ragflow_sdk import RAGFlow, Agent
import requests  # Import the requests module
# from jsonpath_ng import jsonpath, parse
import ast
import json 
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from gradio_client import Client, handle_file
import av
import pydub
import base64
from gradio_client import Client
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase

st.sidebar.image("logo_nutrifAI.png")
with st.sidebar:
    option = st.selectbox(
        "Agents",
        ("Nutritionalist", "Diabetes expert", "Private Trainer", "Dietitian", "Pediatric nutritionilist", "Oncology nutritionist")
    )
    st.sidebar.markdown("<div style='height: 300px;'></div>", unsafe_allow_html=True)
    option2 = st.button(
        "Profile"
    )


st.title("Nutrif:green[AI]")

# Initialize session state for messages, input status, Ragflow session, datasets, and agent
if "messages" not in st.session_state:
    st.session_state.messages = []  # Holds the chat messages
if "input_disabled" not in st.session_state:
    st.session_state.input_disabled = False  # Tracks if the input field is disabled
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None  # Holds the question that has been sent
# if "ragflow_session" not in st.session_state:
#     st.session_state.ragflow_session = None  # Holds the Ragflow session (agent session)
# if "datasets" not in st.session_state:
#     st.session_state.datasets = []  # Holds the available datasets
# if "selected_dataset_id" not in st.session_state:
#     st.session_state.selected_dataset_id = None  # Holds the selected dataset ID

#API for speech recognition: 
client = Client("http://89.169.98.17:7860/")

# Speech Recognition Language Selection
language = st.selectbox("Select Speech Recognition Language", ["English", "Norwegian", "Russian", "Spanish"])

def send_query_to_server(question, session):
    """
    Sends a question to the Ragflow API server within a session and retrieves the response.
    """
    #session = st.session_state.agent_session
    if not session:
        st.write("Agent session not initialized.")
        return "Agent session not initialized."
    response = session.ask(question=question, stream=False)
    raw_response = ''
    for ans in response:

        # ans_json = json.loads(str(ans))
        ans_dict = eval(str(ans))
        print(type(ans_dict))#['content'])
        print(ans_dict)
        raw_response = ans_dict['content']
    #st.write(raw_response)
    return raw_response


def handle_user_input(session):
    """
    Handles the user input from the chat interface, sends the question to the server,
    and displays the response received.
    """
    if st.session_state.pending_question:  # If there is a pending question
        question = st.session_state.pending_question
        st.session_state.pending_question = None  # Clear the pending state

        # Store the user message
        st.session_state.messages.append({"role": "user", "content": question})

        # Display the message in the chat
        with st.chat_message("user"):
            st.write(question)

        # Show a spinner while waiting for the assistant's response
        with st.spinner("Waiting for a response..."):
            response = send_query_to_server(question, session)

        # Store the response in the session state
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display the response with appropriate line breaks
        with st.chat_message("Agent Response"):
            st.markdown(response.replace('\n', '  \n'))

        # Re-enable the input field once the response is received
        st.session_state.input_disabled = False

        # Rerun to update the UI
        #st.rerun()

        return response

api_key = 'ragflow-NlMmQzMGJhZTBhNTExZWY5MTc1MDI0Mm'  # Provided API key
base_url = 'http://89.169.98.17/'  # Provided base URL    

rag_object = RAGFlow(api_key=api_key, base_url=base_url)

AGENT_ID = "9a154ff2e09b11ef85280242ac120006"  # Replace with the actual agent ID
agent_session = Agent.create_session(AGENT_ID, rag_object)
st.session_state.agent_session = agent_session
# st.success("Agent session initialized successfully.")
# st.write("Agent session initialized successfully.")


response = agent_session.ask(question='Hi', stream=False)
raw_response = ''
for ans in response:

    # ans_json = json.loads(str(ans))
    ans_dict = eval(str(ans))
    print(type(ans_dict))#['content'])
    print(ans_dict)
    raw_response = ans_dict['content']
st.write(f"First response: {raw_response}")




# Input for questions, check if the input field should be disabled
if not st.session_state.input_disabled:
    prompt = st.chat_input(
        "Ask the nutrition-bot anything",  # Default message for input
        disabled=st.session_state.input_disabled  # Disable input while waiting for server response
    )

    #initializing audio var
    result_audio=""

    audio_value = st.audio_input("Record a voice message")

    if audio_value:
        with open("/Users/djordjemijajlovic/temp.wav", "wb") as f:
            f.write(audio_value.read())

        result_audio = client.predict(
            audio_path=handle_file('/Users/djordjemijajlovic/temp.wav'),
            language=language,
            api_name="/speech_recognition"
        )
        print(result_audio)
        prompt = result_audio

    if prompt:
        # Before sending the request, disable the input field and store the question
        st.session_state.pending_question = prompt
        st.session_state.input_disabled = True
        response = handle_user_input(agent_session)

        if result_audio != "":
            result_b64 = client.predict(
            text=response,
            api_name="/text_to_speech"
        )

        binary = base64.b64decode(result_b64[1])

        with open('/Users/djordjemijajlovic/temp.mp3', "wb") as f:
            f.write(binary)

        st.audio('/Users/djordjemijajlovic/temp.mp3', autoplay=True)

        result_audio=""


        # Rerun to update the UI after setting query parameters
        #st.rerun()
else:
    # While waiting for the response, change the input field text to a waiting message
    st.chat_input("Please wait for a response...", disabled=True)