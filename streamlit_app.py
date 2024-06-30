import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

EMAIL = st.secrets["EMAIL"]
PASSWD = st.secrets["PASSWD"]
cookie_path_dir = "./cookies/"

# Login and get cookies
sign = Login(EMAIL, PASSWD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

def get_response(user_input):
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    for resp in chatbot.query(user_input, stream=True):
        if resp is not None:
            yield resp['token']
    
    
if "messages" not in st.session_state:
    st.session_state.messages = []
    

for msg in st.session_state.messages:
    if len(st.session_state.messages) > 0:
        st.chat_message(msg["role"]).write(msg["content"])
    


user_input = st.chat_input("Enter your message:", key="user_input")
st.session_state.messages.append({"role": "user", "content": user_input})

if user_input:
    st.chat_message("user").write(user_input)
    placeholder = st.chat_message("AI").empty()
    with st.spinner("Thinking..."):
        stream_res=""
        conversation_history = "\n".join([f"user: {msg['role']}\nAI: {msg['content']}" for msg in st.session_state.messages])
        combined_input = f"{conversation_history}\nuser: {user_input}\nAI:"
        for response in get_response(combined_input):
            stream_res += response
            placeholder.markdown(stream_res)    
        st.session_state.messages.append({"role": "AI", "content": stream_res})
            
            
