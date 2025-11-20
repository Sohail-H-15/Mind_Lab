// Icon Loading Diagnostic Script
// Add this to check if Font Awesome is loading

document.addEventListener('DOMContentLoaded', function() {
    // Check if Font Awesome is loaded
    const testIcon = document.createElement('i');
    testIcon.className = 'fas fa-check';
    testIcon.style.position = 'absolute';
    testIcon.style.left = '-9999px';
    document.body.appendChild(testIcon);
    
    // Get computed style
    const style = window.getComputedStyle(testIcon, ':before');
    const fontFamily = style.getPropertyValue('font-family');
    
    // Check if Font Awesome fonts are loaded
    if (fontFamily && fontFamily.includes('Font Awesome')) {
        console.log('✅ Font Awesome loaded successfully!');
    } else {
        console.warn('⚠️ Font Awesome not loaded. Checking CDN...');
        
        // Try to load alternative CDN
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.5.1/css/all.min.css';
        link.onerror = function() {
            console.error('❌ All CDN sources failed. Icons will not display.');
            console.log('💡 Solution: Check TROUBLESHOOTING.md for local Font Awesome setup');
        };
        document.head.appendChild(link);
    }
    
    // Remove test icon
    document.body.removeChild(testIcon);
});

