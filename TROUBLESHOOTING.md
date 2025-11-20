# Troubleshooting Guide

## Icons Not Appearing

If Font Awesome icons are not showing up, here are the most common causes and solutions:

### 1. **Internet Connection Required**
Icons are loaded from a CDN (Content Delivery Network), so an active internet connection is required.

**Solution**: Ensure you have internet connectivity.

### 2. **CDN Blocked by Network/Firewall**
Some networks (schools, offices, certain countries) block CDN access.

**Solutions**:
- Check with your network administrator
- Try using a VPN
- Use mobile hotspot to test
- Check browser console (F12) for blocked resource errors

### 3. **Browser Issues**
Some browsers or extensions block external resources.

**Solutions**:
- Try a different browser (Chrome, Firefox, Edge)
- Disable ad blockers temporarily
- Clear browser cache
- Check browser console (F12 → Console) for errors

### 4. **Check Browser Console**
Press `F12` → Go to `Console` tab → Look for errors like:
- `Failed to load resource`
- `CORS policy`
- `net::ERR_BLOCKED_BY_CLIENT`

### 5. **Alternative Solutions**

If CDN is completely blocked, you can:

**Option A: Download Font Awesome Locally**
1. Download Font Awesome from: https://fontawesome.com/download
2. Extract to `static/fontawesome/`
3. Update `templates/base.html` line 8 to:
   ```html
   <link rel="stylesheet" href="{{ url_for('static', filename='fontawesome/css/all.min.css') }}">
   ```

**Option B: Use Different CDN**
Update `templates/base.html` line 8 to use jsDelivr:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.5.1/css/all.min.css">
```

### 6. **Verify CDN is Working**
Test the CDN link directly in your browser:
```
https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css
```

If this doesn't load, it's a network/CDN access issue.

### 7. **App Still Works Without Icons**
The application will function normally even if icons don't load - you'll just see text labels instead of icons.

## Quick Test

1. Open browser Developer Tools (F12)
2. Go to Network tab
3. Refresh the page
4. Look for `all.min.css` - if it shows red/failed, CDN is blocked
5. Check Console tab for any error messages

## Still Having Issues?

If icons still don't appear after trying these solutions:
1. Check if other websites with Font Awesome icons work
2. Try accessing the app from a different network
3. Contact your network administrator if on a restricted network

