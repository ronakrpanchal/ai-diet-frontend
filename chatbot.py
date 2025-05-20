import streamlit as st
import requests
from bson import ObjectId

# Set the API endpoint URL
API_ENDPOINT = st.secrets['API_ENDPOINT']  # Use Streamlit secrets for sensitive data

def chat_bot(user_id):
    st.title("AI Diet Planner Chatbot")
    
    # Initialize session state variables
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").markdown(message["content"])
        else:
            st.chat_message("assistant").markdown(message["content"])
            
            # Display diet plan or meal log if available
            if "diet_plan" in message:
                with st.expander("Diet Plan Details"):
                    st.json(message["diet_plan"])
            elif "meal_log" in message:
                with st.expander("Meal Log Details"):
                    st.json(message["meal_log"])
    
    # Handle user input
    if prompt := st.chat_input("Ask me about diet plans or log your meals..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)
        
        # Make API request
        try:
            response = requests.post(
                API_ENDPOINT,
                json={"user_id": user_id, "message": prompt}
            )
            
            if response.status_code == 200:
                api_response = response.json()
                
                # Display assistant response
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    message_placeholder.markdown(api_response["message"])
                
                # Create response object for session state
                assistant_response = {
                    "role": "assistant",
                    "content": api_response["message"]
                }
                
                # Add diet plan or meal log if available
                if "diet_plan" in api_response:
                    assistant_response["diet_plan"] = api_response["diet_plan"]
                    with st.expander("Diet Plan Details"):
                        st.json(api_response["diet_plan"])
                        
                elif "meal_log" in api_response:
                    assistant_response["meal_log"] = api_response["meal_log"]
                    with st.expander("Meal Log Details"):
                        st.json(api_response["meal_log"])
                
                # Add assistant response to chat history
                st.session_state.messages.append(assistant_response)
                
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            st.error(f"Failed to connect to API: {str(e)}")