import streamlit as st

st.title("🤖 Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").markdown(message["content"])
    else:
        st.chat_message("assistant").markdown(message["content"])
        
if prompt := st.chat_input("Ask me anything about your health!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = "This is a placeholder response. Replace with actual model response."
        message_placeholder.markdown(response)
        
    st.session_state.messages.append({"role": "assistant", "content": response})
    message_placeholder.markdown(response)
    
