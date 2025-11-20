# Setup Checklist for New Users

## ✅ What's Included in the Repository

- ✅ All source code (`app.py`, templates, static files)
- ✅ `requirements.txt` with all dependencies
- ✅ `README.md` with detailed instructions
- ✅ `SETUP.md` and `QUICK_SETUP.md` guides
- ✅ `.gitignore` properly configured

## ✅ What's NOT Included (Users Need to Create)

- ❌ `.env` file (contains API key - users create their own)
- ❌ `venv/` folder (virtual environment - users create their own)
- ❌ `mindlab.db` (database - auto-created on first run)
- ❌ `uploads/` folder (auto-created on first run)

## 🚀 Quick Start for New Users

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd MindLab
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\Activate.ps1
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Optional: Add Gemini API Key**
   - Get key from: https://makersuite.google.com/app/apikey
   - Create `.env` file:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```
   - **Note:** App works without API key (uses fallbacks)

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the app**
   - Open: http://localhost:5000
   - Database will be created automatically
   - Register a new account and start using!

## ✅ Verification

The app will work immediately after cloning because:
- ✅ Database auto-creates on first run (`init_db()` function)
- ✅ Uploads folder auto-creates
- ✅ Works without API key (fallback mode)
- ✅ All dependencies listed in `requirements.txt`

## 📝 Important Notes

- **API Key is Optional**: The app works without it, but AI features will use templates instead of dynamic generation
- **Database**: SQLite database is created automatically - no setup needed
- **Port**: Default port is 5000, change in `app.py` if needed
- **Python Version**: Requires Python 3.7+

