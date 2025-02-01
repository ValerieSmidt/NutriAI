import streamlit as st
from ragflow_sdk import RAGFlow
import requests  # Import the requests module

st.title("NutrifAI")  # Set the title of the Streamlit app

# Initialize session state for messages, input status, Ragflow session, assistant, and datasets
if "messages" not in st.session_state:
    st.session_state.messages = []  # Holds the chat messages
if "input_disabled" not in st.session_state:
    st.session_state.input_disabled = False  # Tracks if the input field is disabled
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None  # Holds the question that has been sent
if "ragflow_session" not in st.session_state:
    st.session_state.ragflow_session = None  # Holds the Ragflow session
if "assistant" not in st.session_state:
    st.session_state.assistant = None  # Holds the chat assistant
if "datasets" not in st.session_state:
    st.session_state.datasets = []  # Holds the available datasets
if "selected_dataset_id" not in st.session_state:
    st.session_state.selected_dataset_id = None  # Holds the selected dataset ID

def initialize_ragflow():
    """
    Initializes the Ragflow SDK and lists available datasets.
    """
    api_key = 'ragflow-NlMmQzMGJhZTBhNTExZWY5MTc1MDI0Mm'  # Provided API key
    base_url = 'http://89.169.98.17/knowledge'  # Provided base URL

    try:
        rag_object = RAGFlow(api_key=api_key, base_url=base_url)
        
        # List all available datasets
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

def get_or_create_assistant(dataset_id):
    """
    Retrieves an existing chat assistant or creates a new one using the specified dataset.
    """
    api_key = 'ragflow-NlMmQzMGJhZTBhNTExZWY5MTc1MDI0Mm'  # Provided API key
    base_url = 'http://89.169.98.17/'  # Provided base URL

    try:
        rag_object = RAGFlow(api_key=api_key, base_url=base_url)

        # Verify the selected dataset ID exists
        dataset = next((ds for ds in st.session_state.datasets if ds.id == dataset_id), None)
        if not dataset:
            st.error(f"Selected dataset (ID: {dataset_id}) does not exist.")
            return

        # Debugging: Print selected dataset information
        st.write(f"Selected dataset: {dataset.name} (ID: {dataset.id})")

        # Check if an assistant with the same name already exists
        assistants = rag_object.list_chats(name="Miss R")
        if assistants:
            assistant = assistants[0]
        else:
            # Create a new chat assistant
            assistant = rag_object.create_chat(
                name="Miss R",
                dataset_ids=[dataset_id]
            )
        st.session_state.assistant = assistant
        st.success("Ragflow assistant initialized successfully.")
    except Exception as e:
        st.error(f"Failed to initialize Ragflow assistant: {str(e)}")

def initialize_ragflow_session():
    """
    Initializes a session with the Ragflow chat assistant.
    """
    assistant = st.session_state.assistant
    if not assistant:
        st.error("Assistant not initialized.")
        return

    try:
        session = assistant.create_session()
        st.session_state.ragflow_session = session
        st.success("Ragflow session created successfully.")
    except Exception as e:
        st.error(f"Failed to create Ragflow session: {str(e)}")

def send_query_to_server(question):
    """
    Sends a question to the Ragflow API server within a session and retrieves the response.

    Args:
        question (str): The question to send to the         server.

    Returns:
        str: The response received from the server, or an error message if communication fails.
    """
    session = st.session_state.ragflow_session
    if not session:
        return "Ragflow session not initialized."

    try:
        response = session.ask(question=question, stream=False)
        # Convert the generator to a list and get the content
        response_list = list(response)
        if response_list:
            # Extract the content from the response
            first_response = response_list[0]
            if isinstance(first_response, dict) and "content" in first_response:
                content = first_response["content"]
            else:
                content = "Unexpected response format."
            return content
        else:
            return "No response received from the server."
    except Exception as e:
        return f"Error communicating with server: {str(e)}"

def handle_user_input():
    """
    Handles the user input from the chat interface, sends the question to the server,
    and displays the response received.

    This function manages the display of user messages, waits for the assistant's response,
    and updates the session state accordingly.
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
        with st.spinner("Waiting for a response from the assistant..."):
            # Send the question to the server
            response = send_query_to_server(question)

        # Store the assistant's response in the session state
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Display the response with appropriate line breaks
        with st.chat_message("assistant"):
            st.markdown(response.replace('\n', '  \n'))

        # Re-enable the input field once the response is received
        st.session_state.input_disabled = False

        # Rerun to update the UI
        st.rerun()

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

# Create or get assistant if dataset is selected and assistant is not already created
if st.session_state.selected_dataset_id and not st.session_state.assistant:
    get_or_create_assistant(st.session_state.selected_dataset_id)

# Initialize Ragflow session if not already initialized
if st.session_state.assistant and st.session_state.ragflow_session is None:
    initialize_ragflow_session()

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