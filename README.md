# Streamlit Chat Application

This project is a Streamlit-based chat application that uses the Groq API to generate responses. The application allows users to select different models and control the temperature of the responses. The chat history is reset whenever the model is changed.

## Features

- **Model Selection**: Choose between multiple models (Gemma 7b, Mixtral 8x7b, LLaMA3 70b, LLaMA3 8b).
- **Temperature Control**: Adjust the response temperature using a slider.
- **Chat History**: Displays the conversation history.
- **Dynamic Reset**: Resets the chat history whenever a different model is selected.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/streamlit-chat-app.git
    cd streamlit-chat-app
    ```

2. **Install the required packages**:
    ```bash
    pip install streamlit groq
    ```

3. **Set up your Groq API key**:
    Replace the placeholder API key in the script with your actual Groq API key.
    ```python
    api_key = 'your_actual_api_key'
    ```

## Usage

1. **Run the Streamlit app**:
    ```bash
    streamlit run app.py
    ```

2. **Select a model and adjust the temperature**:
    Use the sidebar to select a model and adjust the temperature.

3. **Enter your message**:
    Type your message in the input box and press Enter.

4. **View the chat history**:
    The chat history will be displayed above the input box. If you change the model, the chat history will reset.

