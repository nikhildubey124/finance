# Global Loading Indicator Guide

## Overview

The FinanceTracker application now includes a comprehensive global loading indicator that automatically appears during:

- **Page navigation** (clicking links, submitting forms)
- **Form submissions** (login, registration, data entry)
- **AJAX/Fetch requests** (API calls)
- **Page loads** (initial page rendering)

The loader is:
- ✅ **Automatic** - No manual code needed in most cases
- ✅ **Consistent** - Same look and feel across all pages
- ✅ **Responsive** - Works on desktop, tablet, and mobile
- ✅ **Smart** - Prevents flashing for quick operations
- ✅ **Safe** - Auto-hides after 30 seconds (failsafe)
- ✅ **Accessible** - Respects `prefers-reduced-motion`

---

## Files Involved

### Core Files
- **[static/loader.css](static/loader.css)** - Loading indicator styles
- **[static/loader.js](static/loader.js)** - Loading indicator logic
- **[templates/base.html](templates/base.html)** - Base template with loader included
- **[static/app.js](static/app.js)** - Integrated with GlobalLoader

### What You Need to Do
**Nothing!** The loader works automatically when you:
1. Use the base template (recommended)
2. Include `loader.css` and `loader.js` in your templates
3. Let the JavaScript handle the rest

---

## Usage

### Option 1: Use the Base Template (Recommended)

Create or update your page template to extend `base.html`:

```html
{% extends "base.html" %}

{% block title %}My Page | FinanceTracker{% endblock %}

{% block content %}
<div class="container">
    <h1>My Page Content</h1>
    <p>This page automatically has the loading indicator!</p>

    <!-- Forms automatically show loader on submit -->
    <form method="POST">
        <input type="text" name="data" required>
        <button type="submit">Submit</button>
    </form>
</div>
{% endblock %}
```

That's it! The loader will automatically:
- Show when you click submit
- Show when you click navigation links
- Hide when the page finishes loading

### Option 2: Add to Existing Templates

If you can't use the base template, add these lines to your existing templates:

```html
<!DOCTYPE html>
<html>
<head>
    <!-- ... your existing head content ... -->

    <!-- Add loader CSS -->
    <link rel="stylesheet" href="/static/loader.css">
</head>
<body>

    <!-- Add loader HTML (right after <body>) -->
    <div id="global-loader">
        <div class="loader-container">
            <div class="loader-spinner"></div>
            <div class="loader-text">Loading...</div>
            <div class="loader-subtext">Please wait</div>
        </div>
    </div>

    <!-- ... your existing content ... -->

    <!-- Add loader JavaScript (before closing </body>) -->
    <script src="/static/loader.js"></script>
    <script src="/static/app.js"></script>
</body>
</html>
```

---

## Automatic Behavior

The loader automatically shows for:

### 1. Form Submissions
```html
<!-- Loader shows automatically -->
<form method="POST" action="/add-transaction">
    <input type="number" name="amount">
    <button type="submit">Add Transaction</button>
</form>
```

### 2. Link Navigation
```html
<!-- Loader shows when clicked -->
<a href="/dashboard">Go to Dashboard</a>
```

### 3. Fetch/AJAX Requests
```javascript
// Loader shows automatically for fetch requests
fetch('/api/data')
    .then(response => response.json())
    .then(data => {
        // Loader hides automatically
        console.log(data);
    });
```

---

## Customization

### Custom Loading Messages

#### For Forms
```html
<form method="POST"
      data-loading-message="Saving transaction..."
      data-loading-subtext="This may take a moment">
    <button type="submit">Save</button>
</form>
```

#### For Links
```html
<a href="/export-transactions"
   data-loading-message="Generating report..."
   data-loading-subtext="Preparing your CSV file">
    Export CSV
</a>
```

### Disable Loader for Specific Elements

#### Using Class
```html
<a href="/page" class="no-loader">No Loading Indicator</a>

<form class="no-loader" method="POST">
    <!-- This form won't trigger the loader -->
</form>
```

#### Using Data Attribute
```html
<a href="/page" data-no-loader>Quick Link</a>
```

### Manual Control

For advanced use cases, you can manually control the loader:

```javascript
// Show loader with custom message
GlobalLoader.show('Processing payment...', 'Please do not close this window');

// Perform your operation
await someAsyncOperation();

// Hide loader
GlobalLoader.hide();
```

#### Check Loader Status
```javascript
if (GlobalLoader.isVisible()) {
    console.log('Loader is currently showing');
}
```

#### Configuration Options
```javascript
// Access configuration
console.log(GlobalLoader.config);

// Modify settings (before page fully loads)
GlobalLoader.config.minDisplayTime = 500; // Show for at least 500ms
GlobalLoader.config.autoHideTimeout = 60000; // Auto-hide after 60 seconds
```

---

## Examples

### Example 1: Transaction Form with Custom Message
```html
<form method="POST" action="/add-transaction"
      data-loading-message="Adding transaction..."
      data-loading-subtext="Updating your balance">

    <label>Amount</label>
    <input type="number" name="amount" required>

    <label>Category</label>
    <select name="category">
        <option>Food</option>
        <option>Transport</option>
    </select>

    <button type="submit">Add Transaction</button>
</form>
```

### Example 2: Bulk Upload with Progress
```html
<form method="POST" enctype="multipart/form-data"
      data-loading-message="Uploading file..."
      data-loading-subtext="Processing transactions">

    <input type="file" name="file" accept=".xlsx,.csv" required>
    <button type="submit">Upload</button>
</form>
```

### Example 3: Export Button
```html
<a href="/export-transactions" class="btn btn-primary"
   data-loading-message="Generating CSV..."
   data-loading-subtext="This may take a few moments">
    📥 Export Transactions
</a>
```

### Example 4: Manual AJAX Request
```javascript
async function deleteTransaction(transactionId) {
    // Show loader
    GlobalLoader.show('Deleting transaction...', 'Please wait');

    try {
        const response = await fetch(`/api/transactions/${transactionId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            Toast.success('Transaction deleted');
            location.reload(); // Loader will show during reload
        } else {
            throw new Error('Delete failed');
        }
    } catch (error) {
        Toast.error('Failed to delete transaction');
        GlobalLoader.hide(); // Hide on error
    }
}
```

### Example 5: Disable Loader for Modal/Popups
```html
<!-- Modal trigger - don't show loader -->
<button class="no-loader" onclick="openModal()">
    Open Settings
</button>

<!-- External link - don't show loader -->
<a href="https://example.com" target="_blank" class="no-loader">
    External Help
</a>
```

---

## Styling Customization

### Change Loader Colors
Edit `static/loader.css`:

```css
/* Primary loader color */
.loader-spinner {
    border-top-color: #27ae60; /* Change to your color */
}

/* Background overlay */
#global-loader {
    background-color: rgba(26, 43, 60, 0.85); /* Adjust opacity */
}

/* Loader container */
.loader-container {
    background: #ffffff; /* Change background */
}
```

### Use Different Spinner Style
Replace the spinner with a progress bar:

```css
/* Hide default spinner */
.loader-spinner {
    display: none;
}

/* Show progress bar instead */
.loader-progress-bar {
    display: block !important;
}
```

---

## Troubleshooting

### Loader Not Showing

**Check 1:** Verify files are loaded
```html
<link rel="stylesheet" href="/static/loader.css">
<script src="/static/loader.js"></script>
```

**Check 2:** Verify loader HTML exists
```javascript
console.log(document.getElementById('global-loader'));
// Should not be null
```

**Check 3:** Check for exclusions
```html
<!-- This won't show loader -->
<form class="no-loader">
```

### Loader Not Hiding

**Cause:** JavaScript error preventing completion

**Solution:**
```javascript
// Force hide
GlobalLoader.hide();

// Or reload page
location.reload();
```

**Automatic failsafe:** Loader auto-hides after 30 seconds

### Loader Flashing Too Quickly

**Cause:** Operation completes in < 300ms

**Solution:** This is intentional to prevent flashing. If you want to show it longer:
```javascript
GlobalLoader.config.minDisplayTime = 1000; // 1 second minimum
```

### Multiple Loaders Showing

**Cause:** Both old Loading and new GlobalLoader being used

**Solution:** Update code to use only GlobalLoader:
```javascript
// Old (remove)
Loading.show();

// New (use this)
GlobalLoader.show();
```

---

## Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

### Features
- ES6+ JavaScript (arrow functions, const/let)
- CSS animations and transitions
- Fetch API interception
- Modern event listeners

---

## Performance Impact

- **CSS File Size:** 4KB (minified: ~2KB)
- **JS File Size:** 8KB (minified: ~4KB)
- **Runtime Overhead:** < 1ms per operation
- **Memory:** Minimal (single DOM element)

### Best Practices
1. ✅ Use automatic loader (no manual code)
2. ✅ Let it hide automatically
3. ✅ Use custom messages for long operations
4. ✅ Disable for quick actions (< 100ms)
5. ❌ Don't show loader for instant feedback (clicks, toggles)

---

## Migration from Old Loader

If you used the old `Loading` object, it now uses GlobalLoader:

```javascript
// This still works (backward compatible)
Loading.show();
Loading.hide();

// But GlobalLoader is more powerful
GlobalLoader.show('Custom message', 'Subtext');
```

---

## Future Enhancements

Planned features:
- [ ] Progress bar with percentage
- [ ] Queue management for multiple operations
- [ ] Toast integration (show toast after loader hides)
- [ ] Custom animations
- [ ] Themes (dark mode, custom colors)

---

## Support

If you encounter issues:

1. **Check browser console** for JavaScript errors
2. **Verify file paths** are correct
3. **Test manual control** with `GlobalLoader.show()` in console
4. **Check template** includes loader.css and loader.js

Your FinanceTracker now has professional, automatic loading indicators! 🎉
