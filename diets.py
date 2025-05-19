import streamlit as st
from pymongo import MongoClient

def display_diet_plan(user_id):
    """
    Fetches and displays the diet plan for a given user ID.

    Args:
        user_id (int): The ID of the user whose diet plan is to be displayed.
    """
    # MongoDB setup
    client = MongoClient(st.secrets['MONGO_URI'])  # Change if hosted elsewhere
    db = client["health_ai"]
    collection = db["diets"]

    # Fetch the diet plan for the user
    record = collection.find_one({"user_id": user_id, "AI_plan.response_type": "diet_plan"})

    if not record:
        st.error("No diet plan found.")
        return

    diet_plan = record["AI_plan"]["diet_plan"]

    # --- Display General Diet Info ---
    st.title("Your AI-Generated Diet Plan")

    st.header("🧠 Goal and Preferences")
    st.markdown(f"- **Goal:** {diet_plan['goal']}")
    st.markdown(f"- **Diet Preference:** {diet_plan['dietPreference']}")

    st.header("📊 Daily Nutrition Goals")
    daily = diet_plan["dailyNutrition"]
    st.markdown(f"- **Calories:** {daily['calories']} kcal")
    st.markdown(f"- **Carbs:** {daily['carbs']} g")
    st.markdown(f"- **Proteins:** {daily['protein']} g")
    st.markdown(f"- **Fats:** {daily['fats']} g")
    st.markdown(f"- **Water Intake:** {daily['waterIntake']} L")

    st.header("📈 Calorie Distribution")
    for dist in diet_plan["calorieDistribution"]:
        st.markdown(f"- {dist['category']}: {dist['percentage']}")

    # --- Display Workout Routine ---
    st.header("🏋️ Weekly Workout Routine")
    for workout in diet_plan["workoutRoutine"]:
        st.markdown(f"- **{workout['day']}:** {workout['routine']}")

    # --- Display Daily Meal Plans ---
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

# Example usage
if __name__ == "__main__":
    user_id = 1  # Replace with dynamic input if needed
    display_diet_plan(user_id)