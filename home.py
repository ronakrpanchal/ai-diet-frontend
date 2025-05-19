import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB connection
MONGO_URI = st.secrets["MONGO_URI"]
DB_NAME = "health_ai"
COLLECTION_NAME = "users"

def home_page(user_id):
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    try:
        user_data = collection.find_one({"_id": ObjectId(user_id)})
    except Exception as e:
        st.error(f"Invalid user ID format: {e}")
        return

    st.title("🏠 Home - User Health Profile")

    if user_data:
        st.subheader("👤 Personal Details")

        personal_info = user_data.get("personal_info", {})

        st.markdown(f"- **Name:** {personal_info.get('name', 'N/A')}")
        st.markdown(f"- **Email:** {user_data.get('username', 'N/A')}")
        st.markdown(f"- **Gender:** {personal_info.get('gender', 'N/A').capitalize()}")
        st.markdown(f"- **Age:** {personal_info.get('age', 'N/A')} years")

        st.subheader("📏 Health Metrics")
        st.markdown(f"- **Height:** {personal_info.get('height', 'N/A')} cm")
        st.markdown(f"- **Weight:** {personal_info.get('weight', 'N/A')} kg")
        st.markdown(f"- **Body Fat Percentage (BFP):** {personal_info.get('bfp', 'N/A')} %")
    else:
        st.error("User not found in database.")

# For testing purposes — replace with actual ObjectId from your database
if __name__ == "__main__":
    user_id = "682b1d2989c9596f1f526b59"  # Replace with real ObjectId
    home_page(user_id)