# AI Diet Planner 🥗🤖

A comprehensive AI-powered diet planning application built with Streamlit that provides personalized nutrition plans, meal logging, and intelligent chatbot assistance for your health and fitness journey.

## Features

### 🔐 User Authentication
- Secure user registration and login system
- Password strength validation with bcrypt encryption
- Email format validation
- Session management

### 👤 Personal Health Profile
- Complete health profile setup (name, age, gender, height, weight, body fat percentage)
- View and manage personal health metrics
- Profile completion tracking

### 🤖 AI Chatbot Assistant
- Interactive AI-powered diet planning chatbot
- Natural language processing for diet and meal queries
- Real-time responses with structured data display
- Integration with FastAPI backend for AI processing

### 📊 Diet Plan Management
- AI-generated personalized diet plans
- Daily nutrition goals and macronutrient breakdown
- Weekly meal plans with detailed calorie information
- Workout routine recommendations
- Calorie distribution analysis

### 🍽️ Meal Logging
- Track daily meals and nutrition intake
- Detailed macronutrient breakdown per meal
- Historical meal log viewing
- Calorie and nutrition tracking

## Tech Stack

### Frontend
- **Streamlit** - Web application framework
- **Python** - Core programming language

### Backend Integration
- **FastAPI** - Backend API integration
- **Requests** - HTTP client for API communication

### Database
- **MongoDB** - NoSQL database for user data storage
- **PyMongo** - MongoDB driver for Python

### Security
- **bcrypt** - Password hashing and authentication

## Project Structure

```
ai-diet-planner/
├── app.py              # Main application entry point
├── chatbot.py          # AI chatbot functionality
├── db.py               # MongoDB database setup and configuration
├── diets.py            # Diet plan display and management
├── meals.py            # Meal logging and tracking
├── personal_info.py    # User profile management
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Installation

### Prerequisites
- Python 3.7+
- MongoDB Atlas account or local MongoDB installation
- FastAPI backend service (separate deployment)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd ai-diet-planner
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Streamlit Secrets**
   Create a `.streamlit/secrets.toml` file in your project root:
   ```toml
   MONGO_URI = "your_mongodb_connection_string"
   API_ENDPOINT = "your_fastapi_backend_url"
   ```

4. **Set up MongoDB**
   - Create a MongoDB Atlas cluster or set up local MongoDB
   - Create a database named `health_ai`
   - Collections will be created automatically on first run

5. **Deploy FastAPI Backend**
   - Ensure your FastAPI backend is deployed and accessible
   - The backend should handle endpoints:
     - `POST /ai` - AI chatbot responses
     - `GET /diet` - Diet plan retrieval
     - `GET /meals` - Meal logs retrieval
     - `GET /user` - User profile data

## Usage

### Running the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

### User Journey

1. **Registration/Login**
   - Create a new account with email and secure password
   - Or sign in with existing credentials

2. **Profile Setup**
   - Complete your health profile with personal metrics
   - This data is used for personalized recommendations

3. **AI Chatbot Interaction**
   - Ask questions about diet planning
   - Log meals through natural language
   - Get personalized nutrition advice

4. **View Diet Plans**
   - Access AI-generated diet plans
   - View daily nutrition goals
   - Check weekly meal recommendations

5. **Track Meals**
   - Log daily meals and track nutrition
   - View historical meal data
   - Monitor macronutrient intake

## Database Schema

### Users Collection
```javascript
{
  "_id": ObjectId,
  "username": String,      // Email address
  "password": String,      // Bcrypt hashed password
  "created_at": Date,
  "profile_completed": Boolean,
  "personal_info": {
    "name": String,
    "age": Number,
    "gender": String,
    "height": Number,       // cm
    "weight": Number,       // kg
    "bfp": Number          // Body fat percentage
  }
}
```

### Diets Collection
```javascript
{
  "_id": ObjectId,
  "user_id": String,
  "AI_Plan": {
    "response_type": "diet_plan",
    "diet_plan": {
      "goal": String,
      "dietPreference": String,
      "dailyNutrition": Object,
      "mealPlans": Array,
      "workoutRoutine": Array
    }
  }
}
```

### Meals Collection
```javascript
{
  "_id": ObjectId,
  "user_id": String,
  "meal_logs": Array,
  "mealType": String,
  "totalCalories": Number,
  "macronutrients": Object,
  "items": Array
}
```

## API Integration

The application integrates with a FastAPI backend for AI processing. Ensure your backend implements these endpoints:

- `POST /ai` - Process AI chatbot requests
- `GET /diet?id={user_id}` - Retrieve user's diet plan
- `GET /meals?id={user_id}` - Get user's meal logs
- `GET /user?id={user_id}` - Fetch user profile data

## Security Features

- Password strength validation (minimum 8 characters, uppercase, lowercase, numbers)
- Bcrypt password hashing
- Email format validation
- Session state management
- MongoDB injection protection through PyMongo

## Configuration

### Environment Variables (Streamlit Secrets)
- `MONGO_URI` - MongoDB connection string
- `API_ENDPOINT` - FastAPI backend URL

### Database Indexes
The application automatically creates indexes for:
- `users.username` (unique)
- `diets.user_id`
- `meals.user_id`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Verify your MongoDB URI in secrets.toml
   - Check network connectivity and firewall settings

2. **API Connection Failed**
   - Ensure FastAPI backend is running and accessible
   - Verify API_ENDPOINT URL in configuration

3. **Authentication Issues**
   - Clear browser cache and session state
   - Check password strength requirements

**Built with ❤️ using Streamlit, MongoDB, and AI technologies**