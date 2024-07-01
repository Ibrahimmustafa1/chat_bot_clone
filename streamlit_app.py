import streamlit as st
from groq import Groq
import json

api_key = st.secrets['token']
client = Groq(api_key=api_key)

def get_response(query, model, temp):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ],
        model=model,
        temperature=temp,
        stream=True
    )
    for token in chat_completion:
        msg = token.choices[0].json()
        msg = json.loads(msg)
        msg = msg['delta']['content']
        if msg is not None:
            yield msg

with st.sidebar:
    model_options = {
        "Gemma 7b": 'gemma-7b-it',
        "Mixtral 8x7b": 'mixtral-8x7b-32768',
        "LLaMA3 70b": 'llama3-70b-8192',
        "LLaMA3 8b": 'llama3-8b-8192'
    }
    
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = list(model_options.keys())[0]

    selected_model = st.selectbox("Select a model", list(model_options.keys()), index=list(model_options.keys()).index(st.session_state.selected_model))
    selected_model_id = model_options[selected_model]
    temp = st.slider("Model Temperature", 0.0, 2.0, 0.5, 0.1)

    if selected_model != st.session_state.selected_model:
        st.session_state.selected_model = selected_model
        st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Enter your message:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    placeholder = st.chat_message("AI").empty()
    with st.spinner("Thinking..."):
        stream_res = ""
        conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
        combined_input = f"{conversation_history}\nuser: {user_input}\nAI:"
        for response in get_response(combined_input, selected_model_id, temp):
            stream_res += response
            placeholder.markdown(stream_res)
        st.session_state.messages.append({"role": "AI", "content": stream_res})
