import streamlit as st
from hugchat import hugchat
from hugchat.login import Login


EMAIL = st.secrets["EMAIL"]
PASSWD = st.secrets["PASSWD"]
cookie_path_dir = "./cookies/"

sign = Login(EMAIL, PASSWD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

def get_response(user_input):
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    for resp in chatbot.query(user_input, stream=True):
        if resp is not None:
            yield resp['token']

def main():
    st.title("Hugging Face Chatbot Clone")

    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    user_input = st.text_input("Enter your message", key="user_input")

    if st.button("Send") and user_input:
        response_container = st.empty()  
        full_response = ""
        
        conversation_history = "\n".join([f"You: {msg[0]}\nBot: {msg[1]}" for msg in st.session_state.conversation])
        combined_input = f"{conversation_history}\nYou: {user_input}\nBot:"

        with st.spinner("Wait for bot response..."):
            for response in get_response(combined_input):
                full_response += response
                response_container.text_area("Bot", value=full_response, height=200)
        
        st.session_state.conversation.append((user_input, full_response))

    conversation_text = "\n".join([f"You: {msg[0]}\nBot: {msg[1]}" for msg in st.session_state.conversation])
    st.text_area("History", value=conversation_text, height=400, key="conversation_text_area")

if __name__ == "__main__":
    main()
