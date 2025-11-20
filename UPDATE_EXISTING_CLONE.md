# How to Update Your Existing Clone

## Don't Clone Again! Just Pull the Latest Changes

If you already cloned the repository and want to get the latest fixes (like the icon fix), you don't need to clone again. Just update your existing clone.

## Quick Update (Recommended)

### Step 1: Navigate to Your Project Folder
```bash
cd path/to/MindLab
```

### Step 2: Pull Latest Changes
```bash
git pull origin main
```

That's it! Your local files will be updated with the latest changes.

## What This Does

- ✅ Downloads only the new/changed files
- ✅ Keeps your local changes (if any)
- ✅ Much faster than re-cloning
- ✅ Preserves your `.env` file and database

## If You Get Conflicts

If you see merge conflicts (rare), you can:

**Option 1: Keep your local changes**
```bash
git stash
git pull origin main
git stash pop
```

**Option 2: Discard local changes and get latest**
```bash
git reset --hard origin/main
```
⚠️ Warning: This will overwrite any local changes!

## Verify Update Worked

After pulling, check if you have the latest files:
```bash
# Check if troubleshooting guide exists
ls TROUBLESHOOTING.md

# Check git log for latest commit
git log --oneline -5
```

You should see commits about "Fix: Update Font Awesome CDN link" and other recent updates.

## After Updating

1. **Restart your Flask app** (if it's running)
2. **Clear browser cache** (Ctrl+Shift+Delete or Cmd+Shift+Delete)
3. **Refresh the page** - icons should now appear!

## Still Having Issues?

If icons still don't appear after updating:
1. Check `TROUBLESHOOTING.md` for detailed solutions
2. Make sure you have internet connection (icons load from CDN)
3. Check browser console (F12) for errors

