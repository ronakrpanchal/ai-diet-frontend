import streamlit as st
from pymongo import MongoClient
import re
import bcrypt
from datetime import datetime
from db import create_mongodb_structure
from home import home_page
from diets import display_diet_plan
from meals import meal_logs_page

MONGO_URI = st.secrets["MONGO_URI"]

# Initialize MongoDB client
try:
    client = MongoClient(MONGO_URI)
    db = client["health_ai"]
    
    users_collection = db["users"]
    meals_collection = db["meals"]
    diets_collection = db["diets"]
except Exception as e:
    st.error(f"Failed to connect to MongoDB: {e}")
    st.stop()

# Utility functions
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_strong_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    return True, "Password is strong"

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(provided_password, stored_password_hash):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password_hash.encode('utf-8'))

# Authentication functions
def register_user(username, password, confirm_password):
    if not username or not password or not confirm_password:
        return False, "All fields are required"
    
    if not is_valid_email(username):
        return False, "Invalid email format"
    
    if password != confirm_password:
        return False, "Passwords do not match"
    
    password_strong, msg = is_strong_password(password)
    if not password_strong:
        return False, msg
    
    if users_collection.find_one({"username": username}):
        return False, "User already exists"
    
    try:
        hashed_password = hash_password(password)
        new_user = {
            "username": username,
            "password": hashed_password,
            "created_at": datetime.now(),
            "profile_completed": False
        }
        result = users_collection.insert_one(new_user)
        if result.inserted_id:
            return True, "Registration successful!"
        else:
            return False, "Failed to register user"
    except Exception as e:
        return False, f"Registration error: {str(e)}"

def login_user(username, password):
    if not username or not password:
        return False, "Email and password are required"
    
    try:
        user = users_collection.find_one({"username": username})
        if not user:
            return False, "Invalid email or password"
        
        if check_password(password, user["password"]):
            st.session_state.authenticated = True
            st.session_state.user = {
                "id": str(user["_id"]),
                "email": user["username"],
                "profile_completed": user.get("profile_completed", False)
            }
            return True, "Login successful"
        else:
            return False, "Invalid email or password"
    except Exception as e:
        return False, f"Login error: {str(e)}"

def logout_user():
    try:
        st.session_state.authenticated = False
        st.session_state.user = None
        return True, "Logged out successfully"
    except Exception as e:
        return False, f"Logout error: {str(e)}"

# Personal Info Submission
def submit_personal_info():
    with st.form("personal_info_form"):
        st.title("📝 Complete Your Profile")
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=0, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        height = st.number_input("Height (cm)", min_value=0.0, step=0.1)
        weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
        bfp = st.number_input("Body Fat Percentage (BFP)", min_value=0.0, max_value=100.0, step=0.1)

        submitted = st.form_submit_button("Submit")

        if submitted:
            try:
                users_collection.update_one(
                    {"username": st.session_state.user["email"]},
                    {
                        "$set": {
                            "profile_completed": True,
                            "personal_info": {
                                "name": name,
                                "age": age,
                                "gender": gender,
                                "height": height,
                                "weight": weight,
                                "bfp": bfp
                            }
                        }
                    }
                )
                st.session_state.user["profile_completed"] = True
                st.success("Profile completed successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to save profile: {e}")

# Streamlit App
def main():
    create_mongodb_structure()

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"
    if "auth_tab" not in st.session_state:
        st.session_state.auth_tab = "Sign In"

    # Sidebar
    with st.sidebar:
        st.title("Get Your Personal AI Dietitian")
        st.markdown("---")
        
        if st.session_state.authenticated:
            st.write(f"👤 {st.session_state.user['email']}")
            st.markdown("---")

            if st.button("🏠 Home", use_container_width=True):
                st.session_state.current_page = "Home"
                st.rerun()
            if st.button("Diet plans", use_container_width=True):
                st.session_state.current_page = "Diets plans"
                st.rerun()
            if st.button("Meal logs", use_container_width=True):
                st.session_state.current_page = "Meal logs"
                st.rerun()
            
            st.markdown("---")
            if st.button("Sign Out", use_container_width=True):
                success, msg = logout_user()
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        else:
            st.info("Please sign in to access all features")

    # Main Content
    if st.session_state.authenticated:
        if not st.session_state.user.get("profile_completed"):
            submit_personal_info()
        else:
            if st.session_state.current_page == "Home":
                home_page(st.session_state.user["id"])
            elif st.session_state.current_page == "Diets plans":
                display_diet_plan(st.session_state.user["id"])
            elif st.session_state.current_page == "Meal logs":
                meal_logs_page(st.session_state.user["id"])
    else:
        st.title("Welcome to AI Diet Planner")
        tab1, tab2 = st.tabs(["Sign In", "Create Account"])

        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Password", type="password", key="login_password")
                submit = st.form_submit_button("Sign In")
                if submit:
                    success, response = login_user(email, password)
                    if success:
                        st.success("Login successful!")
                        st.session_state.current_page = "Home"
                        st.rerun()
                    else:
                        st.error(response)
            if st.button("Forgot Password?"):
                st.session_state.show_reset = True
                st.rerun()

        with tab2:
            with st.form("register_form"):
                email = st.text_input("Email", key="register_email")
                password = st.text_input("Password", type="password", key="register_password")
                st.caption("Password must be at least 8 characters with uppercase, lowercase, and numbers")
                confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
                submit = st.form_submit_button("Create Account")
                if submit:
                    success, msg = register_user(email, password, confirm_password)
                    if success:
                        st.success(msg)
                        st.session_state.auth_tab = "Sign In"
                        st.rerun()
                    else:
                        st.error(msg)

if __name__ == "__main__":
    main()