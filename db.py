from pymongo import MongoClient
import streamlit as st

@st.cache_resource
def create_mongodb_structure():
    """Create MongoDB database and collections"""
    try:
        # Connect to MongoDB
        MONGO_URI = st.secrets['MONGO_URI'] 
        client = MongoClient(MONGO_URI)
        
        # Create or access the database
        db = client["health_ai"]
        
        # Create collections (equivalent to tables in SQL)
        users_collection = db["users"]
        diets_collection = db["diets"]
        meals_collection = db["meals"]
        
        # Create indexes for faster queries
        users_collection.create_index("username", unique=True)
        diets_collection.create_index("user_id")
        meals_collection.create_index("user_id")
        
        print("MongoDB database and collections created successfully")
        return db
    
    except Exception as e:
        print(f"Error creating MongoDB database: {e}")
        return None

if __name__ == "__main__":
    create_mongodb_structure()