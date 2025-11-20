# MindLab – Intelligent Learning Platform

An intelligent learning platform that combines interactive learning activities, AI-powered insights, and a smart chatbot to enhance the learning experience.

## ⚠️ Important: Icons Not Showing?

If icons are not appearing, it's likely a CDN connectivity issue. The app uses Font Awesome icons from a CDN. Solutions:

1. **Check Internet Connection**: Icons load from CDN, so internet is required
2. **Try Different Browser**: Some browsers block CDN resources
3. **Check Browser Console**: Press F12 → Console tab to see any errors
4. **Firewall/Network**: Some networks block CDN access - check with your network admin
5. **Alternative**: The app will still function without icons, just without visual icons

## Features

### 1. User Authentication System
- **User Registration**: Secure registration with email validation
- **Login/Logout**: Session-based authentication
- **Password Hashing**: Uses Werkzeug's secure password hashing
- **Email Verification**: Token-based email verification system
- **SQLite Database**: Lightweight database for user management

### 2. Interactive Concept Playground
Engage with any topic through multiple interactive activities:
- **Drag & Drop**: Match items to categories
- **Reorder Steps**: Arrange process steps in correct order
- **Fill in Blanks**: Complete sentences with correct answers
- **Flashcards**: Flip cards to learn key concepts
- **Mini Quiz**: Test your knowledge with multiple-choice questions

### 3. AI Pattern Insight Engine
Get comprehensive insights for any topic:
- **Summarization**: Quick overview of the topic
- **Pattern Recognition**: Identifies key patterns and themes
- **Difficulty Level Prediction**: Estimates learning difficulty (Basic/Intermediate/Expert)
- **Concept Explanation**: Detailed explanations
- **Related Topics**: Suggests connected topics

### 4. Built-in Chatbot
- Ask questions about any learning topic
- Powered by Google Gemini API for intelligent responses
- Chat history saved for reference
- Fallback to keyword-based responses if API not configured

## Installation

### For New Users:
1. **Clone or download the project**

2. **Create and activate virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\Activate.ps1
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Google Gemini API** (Optional but recommended):
   
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.env` file in the project root (see `HOW_TO_CREATE_ENV.md` for detailed instructions):
     ```
     GEMINI_API_KEY=your_api_key_here
     ```
   - **⚠️ IMPORTANT**: File must be named exactly `.env` (not `env.env`, `env.txt`, or `.env.txt`)
   - **If you saved it as `env.env`**: See `FIX_ENV_FILENAME.md` to rename it correctly
   - **Quick method**: Create a new file named `.env` in the project root folder and add the line above with your API key
   - The application will work without the API key using fallback responses, but for best experience with dynamic content generation, add your API key.

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

**Note:** If you don't have a Gemini API key, the application will still work using fallback templates, but you'll get more dynamic and intelligent responses with the API key configured.

### For Existing Users (Updating Your Clone):

If you already cloned the repository and want to get the latest fixes:

```bash
cd MindLab
git pull origin main
```

Then restart your Flask app. See `UPDATE_EXISTING_CLONE.md` for detailed instructions.

## Usage

### Getting Started
1. **Register** a new account or **Login** if you already have one
2. Visit the **Dashboard** to see your recent concepts
3. Explore the three main features:
   - **Concept Playground**: Enter a topic and engage with interactive activities
   - **Pattern Insight**: Get AI-powered analysis of any topic
   - **Chatbot**: Ask questions and get instant answers

### Concept Playground
1. Enter any topic (e.g., "Photosynthesis", "Python", "World War II")
2. Choose from 5 different activity types:
   - Drag & Drop puzzles
   - Reorder steps
   - Fill in the blanks
   - Interactive flashcards
   - Mini quizzes
3. Complete activities and track your progress

### Pattern Insight Engine
1. Enter a topic you want to analyze
2. Get instant insights including:
   - Summary
   - Recognized patterns
   - Difficulty prediction
   - Detailed explanation
   - Related topics

### Chatbot
1. Type your question in the chat interface
2. Get instant responses
3. View your chat history

## Project Structure

```
MindLab/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── concept_playground.html
│   ├── playground_activity.html
│   ├── pattern_insight.html
│   └── chatbot.html
├── static/                # Static files
│   ├── style.css
│   └── main.js
├── mindlab.db            # SQLite database (created on first run)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Database Schema

- **users**: User accounts with authentication
- **concepts**: Saved learning topics
- **activities**: Activity completion records
- **chat_history**: Chatbot conversation history

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **AI/ML**: Google Gemini API (for chatbot and activity generation)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Security**: Werkzeug password hashing
- **Icons**: Font Awesome
- **Environment**: python-dotenv for configuration

## Features in Detail

### Interactive Activities
All activities are dynamically generated using **Google Gemini API** based on the topic. The system generates personalized:
- Drag & Drop puzzles
- Step reordering activities  
- Fill-in-the-blank exercises
- Educational flashcards
- Custom quizzes

If the API key is not configured, the system falls back to predefined templates.

### Pattern Recognition
The insight engine uses **Google Gemini API** to analyze topics and provide intelligent insights including:
- Summarization
- Pattern recognition
- Difficulty prediction
- Detailed explanations
- Related topic suggestions

### Chatbot Intelligence
The chatbot is powered by **Google Gemini API** for intelligent, contextual responses. It can:
- Answer questions about any topic
- Provide educational explanations
- Guide users to relevant features
- Maintain conversation context

If the API key is not configured, it uses keyword-based matching as a fallback.

## API Configuration

### Google Gemini API Setup

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key
5. Create a `.env` file in the project root:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
6. Restart the application

The API is used for:
- **Chatbot**: Intelligent, contextual responses
- **Activity Generation**: Dynamic puzzles, quizzes, flashcards, and exercises
- **Pattern Insights**: AI-powered topic analysis

## Future Enhancements

- Email sending functionality for verification
- More activity types and customization options
- Progress tracking and analytics
- Social features (sharing concepts, leaderboards)
- Mobile app support
- Multi-language support

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please check the code comments or create an issue in the repository.

---

**Built with ❤️ for intelligent learning**

