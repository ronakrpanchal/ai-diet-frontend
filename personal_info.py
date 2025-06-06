from bson import ObjectId
import streamlit as st
import requests

API_URL = st.secrets['API_ENDPOINT']  # Use Streamlit secrets for sensitive data

def personal_info(user_id):
    st.title("🏠 User Health Profile")

    try:
        response = requests.get(f"{API_URL}/user", params={"id": user_id})
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch user data from API: {e}")
        return

    # Display user details
    st.subheader("👤 Personal Details")

    st.markdown(f"- **Name:** {data.get('name', 'N/A')}")
    st.markdown(f"- **Gender:** {data.get('gender', 'N/A').capitalize()}")
    st.markdown(f"- **Age:** {data.get('age', 'N/A')} years")

    st.subheader("📏 Health Metrics")
    st.markdown(f"- **Height:** {data.get('height', 'N/A')} cm")
    st.markdown(f"- **Weight:** {data.get('weight', 'N/A')} kg")
    st.markdown(f"- **Body Fat Percentage (BFP):** {data.get('bfp', 'N/A')} %")