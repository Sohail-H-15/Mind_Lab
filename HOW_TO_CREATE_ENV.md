# How to Create .env File

## Quick Guide

The `.env` file is used to store your Google Gemini API key securely. Here's how to create it:

## Method 1: Using Text Editor (Easiest)

### Windows:
1. Open **Notepad** (or any text editor)
2. Type this line:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Replace `your_api_key_here` with your actual API key
4. Click **File** → **Save As**
5. Navigate to your MindLab project folder
6. In "Save as type", select **"All Files (*.*)"**
7. Type the filename as: `.env` (with the dot at the start)
8. Click **Save**

### Mac/Linux:
1. Open **TextEdit** (Mac) or any text editor
2. Type this line:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Replace `your_api_key_here` with your actual API key
4. Save the file in your MindLab project folder
5. Name it exactly: `.env` (with the dot at the start)

## Method 2: Using Command Line/Terminal

### Windows (PowerShell):
```powershell
cd C:\path\to\MindLab
echo "GEMINI_API_KEY=your_api_key_here" > .env
```
Then edit the file to replace `your_api_key_here` with your actual key.

### Windows (Command Prompt):
```cmd
cd C:\path\to\MindLab
echo GEMINI_API_KEY=your_api_key_here > .env
```
Then edit the file to replace `your_api_key_here` with your actual key.

### Mac/Linux:
```bash
cd /path/to/MindLab
echo "GEMINI_API_KEY=your_api_key_here" > .env
```
Then edit the file to replace `your_api_key_here` with your actual key.

## Method 3: Using VS Code or Other Code Editors

1. Open your MindLab project folder in VS Code
2. Click **File** → **New File**
3. Name it `.env`
4. Type:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
5. Replace `your_api_key_here` with your actual API key
6. Save the file

## Important Notes:

1. **File must be named exactly `.env`** (with the dot at the start, no extension)
2. **No spaces around the `=` sign**: `GEMINI_API_KEY=key` (correct) ✅
3. **Don't use quotes** around the API key (unless your key has special characters)
4. **File location**: Must be in the **root** of the MindLab project (same folder as `app.py`)

## Example .env File Content:

```
GEMINI_API_KEY=AIzaSyBKJnqAOSHNJl1SHvnJJTRTLSWdcaX69Pk
```

## Verify .env File is Created:

### Windows:
```powershell
dir .env
```

### Mac/Linux:
```bash
ls -la .env
```

If you see the file listed, it's created correctly!

## Get Your API Key:

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key
5. Paste it in your `.env` file

## Troubleshooting:

### File appears as "env" instead of ".env"
- Make sure you saved it as `.env` (with the dot)
- On Windows, you might need to enable "Show file extensions" in File Explorer

### File not found by the app
- Make sure the file is in the same folder as `app.py`
- Check the filename is exactly `.env` (not `.env.txt` or `env`)

### Still not working?
- Restart your Flask app after creating the file
- Check for typos in the file name or content
- Make sure there are no extra spaces or characters

