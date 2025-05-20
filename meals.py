import streamlit as st
import requests
from bson import ObjectId

API_URL = st.secrets['API_ENDPOINT']  # Use Streamlit secrets for sensitive data

def meal_logs_page(user_id):
    st.title("🍽️ Meal Logs")

    # Fetch meal logs via FastAPI
    try:
        with st.spinner("Loading your meals..."):
            response = requests.get(API_URL, params={"id": user_id})
            response.raise_for_status()
            data = response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            st.info(response.json().get("detail", "No meals found"))
        elif response.status_code == 400:
            st.error("Invalid user ID format. Please enter a valid MongoDB ObjectId.")
        else:
            st.error(f"HTTP Error: {e}")
        return
    except Exception as e:
        st.error(f"Error fetching meal logs: {e}")
        return

    meal_logs = data.get("meal_logs", [])
    if not meal_logs:
        st.info("No meals logged yet.")
        return

    # Display meal logs
    for i, meal in enumerate(meal_logs, start=1):
        with st.expander(f"🍴 Meal {i}: {meal.get('mealType', 'Unknown').capitalize()}"):
            st.markdown(f"**Total Calories**: {meal.get('totalCalories', 0)} kcal")

            macronutrients = meal.get("macronutrients", {})
            st.markdown("**Macronutrients:**")
            st.write(f"• Carbohydrates: {macronutrients.get('carbohydrates', 0)} g")
            st.write(f"• Proteins: {macronutrients.get('proteins', 0)} g")
            st.write(f"• Fats: {macronutrients.get('fats', 0)} g")

            st.markdown("**Items:**")
            for item in meal.get("items", []):
                st.write(f"- **{item['name']}**")
                st.write(f"  • Calories: {item.get('calories', 0)} kcal")
                st.write(f"  • Carbs: {item.get('carbs', 0)} g")
                st.write(f"  • Proteins: {item.get('proteins', 0)} g")
                st.write(f"  • Fats: {item.get('fats', 0)} g")

# ---- App Entry Point ----
if __name__ == "__main__":
    st.set_page_config(page_title="Meal Logs", layout="centered")
    user_id_input = st.sidebar.text_input("Enter your MongoDB User ID (ObjectId):")
    if user_id_input:
        meal_logs_page(user_id_input)