import streamlit as st
import requests
from bson import ObjectId

# Base URL of your FastAPI server
API_URL = st.secrets['API_ENDPOINT']  # Use Streamlit secrets for sensitive data

def display_diet_plan(user_id):
    """
    Fetch diet plan from FastAPI endpoint and display it in Streamlit.
    """
    with st.spinner("Fetching your diet plan..."):
        try:
            response = requests.get(f"{API_URL}/diet", params={"id": user_id})
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data: {e}")
            return

    if data.get("AI_Plan", {}).get("response_type") != "diet_plan":
        st.warning("No diet plan found.")
        return

    diet_plan = data["AI_Plan"]["diet_plan"]

    # --- Display General Info ---
    st.title("🥗 Your AI-Generated Diet Plan")

    st.header("🧠 Goal and Preferences")
    st.markdown(f"- **Goal:** {diet_plan['goal']}")
    st.markdown(f"- **Diet Preference:** {diet_plan['dietPreference']}")

    # --- Daily Nutrition ---
    st.header("📊 Daily Nutrition Goals")
    daily = diet_plan["dailyNutrition"]
    st.markdown(f"- **Calories:** {daily['calories']} kcal")
    st.markdown(f"- **Carbs:** {daily['carbs']} g")
    st.markdown(f"- **Proteins:** {daily['protein']} g")
    st.markdown(f"- **Fats:** {daily['fats']} g")
    st.markdown(f"- **Water Intake:** {daily['waterIntake']} L")

    # --- Calorie Distribution ---
    st.header("📈 Calorie Distribution")
    for dist in diet_plan["calorieDistribution"]:
        st.markdown(f"- {dist['category']}: {dist['percentage']}")

    # --- Workout Routine ---
    st.header("🏋️ Weekly Workout Routine")
    for workout in diet_plan["workoutRoutine"]:
        st.markdown(f"- **{workout['day']}**: {workout['routine']}")

    # --- Weekly Meal Plans ---
    st.header("🍱 Weekly Meal Plans")
    for day_plan in diet_plan["mealPlans"]:
        st.subheader(f"📅 {day_plan['day']}")
        st.markdown(f"**Total Calories:** {day_plan['totalCalories']} kcal")

        st.markdown("**Macronutrients:**")
        st.markdown(
            f"- Carbs: {day_plan['macronutrients']['carbohydrates']} g\n"
            f"- Proteins: {day_plan['macronutrients']['proteins']} g\n"
            f"- Fats: {day_plan['macronutrients']['fats']} g"
        )

        for meal in day_plan["meals"]:
            st.markdown(f"**🍽️ {meal['mealType'].capitalize()}**")
            for item in meal["items"]:
                st.markdown(f"- **{item['name']}** ({item['calories']} kcal)")
                st.markdown(f"  - Ingredients: {', '.join(item['ingredients'])}")
        st.markdown("---")


# ---- Streamlit App Layout ----
# st.set_page_config(page_title="Your Diet Plan", layout="wide")

# st.sidebar.title("🔑 Get Your Diet Plan")
# user_id = st.sidebar.text_input("Enter your MongoDB user ID (ObjectId string):")

# if user_id:
#     display_diet_plan(user_id)