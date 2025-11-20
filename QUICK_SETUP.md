# Quick Gemini API Setup

## Current Status
❌ **Gemini API is NOT configured yet** - You need to add your API key manually.

The app will work without it (using fallback templates), but you won't get AI-powered features.

## Setup Steps (2 minutes)

### 1. Get Your API Key
- Go to: https://makersuite.google.com/app/apikey
- Sign in with Google
- Click "Create API Key"
- Copy the key (starts with `AIzaSy...`)

### 2. Create .env File
Create a file named `.env` in the `MindLab` folder with this content:

```
GEMINI_API_KEY=your_actual_api_key_here
```

**Example:**
```
GEMINI_API_KEY=AIzaSyABC123XYZ789def456ghi012jkl345mno678pqr901stu234vwx567
```

### 3. Restart the App
Stop the Flask app (Ctrl+C) and restart it:
```bash
python app.py
```

### 4. Verify It's Working
When you start the app, you should see:
- ✅ `✓ Gemini API configured successfully!` = Working!
- ⚠️ `⚠ Warning: GEMINI_API_KEY not found...` = Not configured

## Test It
1. Login to the app
2. Go to **Chatbot** and ask: "What is machine learning?"
3. If you get an intelligent, detailed response = API is working!
4. If you get a generic template response = API not configured

## Without API Key
The app still works but uses:
- Template-based activities (not dynamic)
- Keyword-based chatbot (not AI-powered)
- Rule-based insights (not AI-generated)

