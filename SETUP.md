# MindLab Setup Guide

## Quick Start with Google Gemini API

### Step 1: Get Your Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key" or "Get API Key"
4. Copy your API key (it will look like: `AIzaSy...`)

### Step 2: Create Environment File

Create a file named `.env` in the project root directory (`MindLab` folder) with the following content:

```
GEMINI_API_KEY=your_actual_api_key_here
```

Replace `your_actual_api_key_here` with the API key you copied.

**Example:**
```
GEMINI_API_KEY=AIzaSyABC123XYZ789...
```

### Step 3: Install Dependencies

Make sure your virtual environment is activated, then install the new dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- `google-generativeai` - For Gemini API integration
- `python-dotenv` - For loading environment variables

### Step 4: Run the Application

```bash
python app.py
```

You should see:
- `✓ Gemini API configured successfully!` if the API key is valid
- `⚠ Warning: GEMINI_API_KEY not found...` if the key is missing

### Step 5: Verify It's Working

1. **Test the Chatbot:**
   - Login to MindLab
   - Go to the Chatbot page
   - Ask any question (e.g., "What is machine learning?")
   - You should get an intelligent, contextual response

2. **Test Activity Generation:**
   - Go to Concept Playground
   - Enter any topic (e.g., "Python Programming", "World War II")
   - Click through the different activities
   - They should be dynamically generated based on your topic

3. **Test Pattern Insights:**
   - Go to Pattern Insight
   - Enter a topic
   - You should get detailed AI-generated insights

## Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution:** Make sure:
- The `.env` file exists in the project root (same folder as `app.py`)
- The `.env` file contains `GEMINI_API_KEY=your_key_here` (no spaces around `=`)
- You've restarted the Flask application after creating/updating `.env`

### Issue: "google-generativeai not installed"
**Solution:** Run:
```bash
pip install google-generativeai python-dotenv
```

### Issue: API errors or rate limits
**Solution:**
- Check if your API key is valid
- Make sure you haven't exceeded API quotas
- The app will automatically fall back to templates if the API fails

## Without API Key (Fallback Mode)

The application will still work without an API key using:
- Predefined templates for activities
- Keyword-based chatbot responses
- Rule-based pattern insights

However, you'll get much better, dynamic content with the Gemini API configured!

## Security Note

**Never commit your `.env` file to version control!**
- The `.env` file is already in `.gitignore`
- Only share your `.env.example` template
- Keep your API key private

