# meal_logs.py
import streamlit as st
from pymongo import MongoClient

def meal_logs_page(user_id):
    st.title("🍽️ Meal Logs")
    
    client = MongoClient(st.secrets["MONGO_URI"])
    db = client["health_ai"]
    meals_collection = db["meals"]

    # Fetch user's meal logs
    try:
        meal_doc = meals_collection.find_one({"user_id": user_id})
        if not meal_doc or "meal_log" not in meal_doc or len(meal_doc["meal_log"]) == 0:
            st.info("No meals logged yet.")
            return

        meal_logs = meal_doc["meal_log"]

        for i, meal in enumerate(meal_logs, start=1):
            with st.expander(f"🍴 Meal {i}: {meal.get('mealType', 'Unknown').capitalize()}"):
                st.markdown(f"**Total Calories**: {meal['totalCalories']} kcal")
                st.markdown("**Macronutrients:**")
                st.write(f"• Carbohydrates: {meal['macronutrients']['carbohydrates']} g")
                st.write(f"• Proteins: {meal['macronutrients']['proteins']} g")
                st.write(f"• Fats: {meal['macronutrients']['fats']} g")

                st.markdown("**Items:**")
                for item in meal.get("items", []):
                    st.write(f"- **{item['name']}**")
                    st.write(f"  • Calories: {item['calories']} kcal")
                    st.write(f"  • Carbs: {item['carbs']} g")
                    st.write(f"  • Proteins: {item['proteins']} g")
                    st.write(f"  • Fats: {item['fats']} g")
    except Exception as e:
        st.error(f"Error fetching meal logs: {e}")
        
if __name__ == "__main__":
    user_id = 1  # Replace with actual user ID
    meal_logs_page(user_id)