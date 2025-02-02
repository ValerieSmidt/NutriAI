# NutrifAI

NutrifAI is an AI-powered Agent designed to provide nutritional advice and expertise. This application leverages the Ragflow SDK and integrates speech recognition capabilities to offer a seamless user experience.

## Features

- **Multiple Agents**: Choose from various specialized agents such as Nutritionalist, Diabetes Expert, Private Trainer, Dietitian, Pediatric Nutritionist, and Oncology Nutritionist. Each agent has their own knowledgebase, which leads to quicker response times and prevents hallucination.
- **Text and Voice Input**: Users can ask questions via text input or record a voice message. This provides accessibility for users. 
- **Speech Recognition and Text-to-Speech**: Integrates capabilities to convert voice input to text and provide responses via synthesized speech.
## Our Tech-stack
![alt text](https://github.com/ValerieSmidt/NutrifAI/blob/main/techstack.png)
## RagFlow
![alt text](https://github.com/ValerieSmidt/NutrifAI/blob/main/flow.png)
## Requirements

- Python 3.6+
- Streamlit
- Ragflow SDK
- Requests
- Gradio Client
- Pydub
- Streamlit WebRTC

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/NutrifAI.git
    cd NutrifAI
    ```

2. Install the required Python packages:

    ```sh
    pip install streamlit ragflow_sdk requests gradio_client pydub streamlit-webrtc
    ```

3. Ensure you have the `logo_nutrifAI.png` in the same directory as your script.

## Usage

1. Run the Streamlit application:

    ```sh
    streamlit run NutrifAI.py
    ```

2. Open your browser and navigate to `http://localhost:8501` to use the NutrifAI application.

