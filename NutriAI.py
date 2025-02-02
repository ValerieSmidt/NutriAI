import streamlit as st
from ragflow_sdk import RAGFlow, Agent
import requests  # Import the requests module
from jsonpath_ng import jsonpath, parse

st.title("NutrifAI")  # Set the title of the Streamlit app

# Initialize session state for messages, input status, Ragflow session, datasets, and agent
if "messages" not in st.session_state:
    st.session_state.messages = []  # Holds the chat messages
if "input_disabled" not in st.session_state:
    st.session_state.input_disabled = False  # Tracks if the input field is disabled
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None  # Holds the question that has been sent
if "ragflow_session" not in st.session_state:
    st.session_state.ragflow_session = None  # Holds the Ragflow session (agent session)
if "datasets" not in st.session_state:
    st.session_state.datasets = []  # Holds the available datasets
if "selected_dataset_id" not in st.session_state:
    st.session_state.selected_dataset_id = None  # Holds the selected dataset ID

api_key = 'ragflow-NlMmQzMGJhZTBhNTExZWY5MTc1MDI0Mm'  # Provided API key
base_url = 'http://89.169.98.17/'  # Provided base URL    

def initialize_ragflow():
    """
    Initializes the Ragflow SDK and lists available datasets.
    """
    try:
        rag_object = RAGFlow(api_key=api_key, base_url=base_url)
        datasets = rag_object.list_datasets()
        if not datasets:
            st.error("No datasets available.")
            return

        # Store datasets in session state
        st.session_state.datasets = datasets
        st.success("Datasets loaded successfully.")
        
        # Debugging: Print out all datasets
        st.write("Available datasets:")
        for dataset in datasets:
            st.write(f"- {dataset.name} (ID: {dataset.id})")

    except Exception as e:
        st.error(f"Failed to initialize Ragflow: {str(e)}")

def get_or_create_agent():
    """
    Initializes or retrieves the agent session using the Ragflow API.
    """
    rag_object = RAGFlow(api_key=api_key, base_url=base_url)
    
    try:
        AGENT_ID = "9a154ff2e09b11ef85280242ac120006"  # Replace with the actual agent ID
        session = Agent.create_session(AGENT_ID, rag_object)
        st.session_state.ragflow_session = session
        st.success("Agent session initialized successfully.")
        st.write(f"Session type: {type(session)}")
        st.write(f"Session methods: {dir(session)}")

    except Exception as e:
        st.error(f"Failed to initialize agent session: {str(e)}")

def handle_user_input():
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
            response = send_query_to_server(question)

        # Store the response in the session state
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display the response with appropriate line breaks
        with st.chat_message("assistant"):
            st.markdown(response.replace('\n', '  \n'))

        # Re-enable the input field once the response is received
        st.session_state.input_disabled = False

        # Rerun to update the UI
        st.rerun()

def send_query_to_server(question):
    """
    Sends a question to the Ragflow API server within a session and retrieves the response.
    """
    session = st.session_state.ragflow_session
    if not session:
        return "Ragflow session not initialized."

    try:
        response = session.ask_agent(question=question, stream=False)
        # Convert the generator to a list and get the content
        response_list = list(response)

        # Debugging: Print the raw response
        st.write(f"Raw response: {response_list}")

        if response_list:
            # Extract the content from the response
            first_response = response_list[0]
            st.write(f"First response: {first_response}")
            if isinstance(first_response, dict) and 'content' in first_response:
                return first_response['content']
            else:
                return f"Response does not contain 'content' key: {first_response}"
        else:
            return "No response received from the server."
    except Exception as e:
        return f"Error communicating with server: {str(e)}"

# Initialize Ragflow and list available datasets if not already initialized
if not st.session_state.datasets:
    initialize_ragflow()

# Display available datasets and allow user to select one
if st.session_state.datasets:
    dataset_names = [dataset.name for dataset in st.session_state.datasets]
    selected_dataset_name = st.selectbox("Select a dataset", dataset_names)

    if selected_dataset_name:
        selected_dataset = next((dataset for dataset in st.session_state.datasets if dataset.name == selected_dataset_name), None)
        if selected_dataset:
            st.session_state.selected_dataset_id = selected_dataset.id
            st.write(f"Dataset selected: {selected_dataset.name} (ID: {selected_dataset.id})")

# Initialize agent session if not already initialized
if st.session_state.selected_dataset_id and st.session_state.ragflow_session is None:
    get_or_create_agent()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"].replace('\n', '  \n'))

# Input for questions, check if the input field should be disabled
if not st.session_state.input_disabled:
    prompt = st.chat_input(
        "Ask the nutrition-bot anything",  # Default message for input
        disabled=st.session_state.input_disabled  # Disable input while waiting for server response
    )

    if prompt:
        # Before sending the request, disable the input field and store the question
        st.session_state.pending_question = prompt
        st.session_state.input_disabled = True

        # Rerun to update the UI after setting query parameters
        st.rerun()
else:
    # While waiting for the response, change the input field text to a waiting message
    st.chat_input("Please wait for a response...", disabled=True)

# If there is a pending question, handle it
if st.session_state.pending_question:
    handle_user_input()
