# Quick Start: Adding Global Loader to Your Pages

## 3-Step Integration

### Step 1: Add CSS to `<head>`
```html
<head>
    <!-- Your existing head content -->
    {% include 'includes/loader_assets.html' %}
</head>
```

### Step 2: Add HTML after `<body>`
```html
<body>
    {% include 'includes/loader_html.html' %}

    <!-- Your existing body content -->
</body>
```

### Step 3: Add Scripts before `</body>`
```html
    <!-- Your existing content -->

    {% include 'includes/loader_scripts.html' %}
    <script src="/static/app.js"></script> <!-- Your other scripts -->
</body>
</html>
```

## Complete Example

### Before (Without Loader)
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>My Page</title>
    <link rel="stylesheet" href="/static/responsive.css">
</head>
<body>
    <h1>My Page</h1>

    <form method="POST">
        <button type="submit">Submit</button>
    </form>

    <script src="/static/app.js"></script>
</body>
</html>
```

### After (With Loader)
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>My Page</title>
    <link rel="stylesheet" href="/static/responsive.css">
    {% include 'includes/loader_assets.html' %} <!-- ADD THIS -->
</head>
<body>
    {% include 'includes/loader_html.html' %} <!-- ADD THIS -->

    <h1>My Page</h1>

    <form method="POST">
        <button type="submit">Submit</button>
    </form>

    {% include 'includes/loader_scripts.html' %} <!-- ADD THIS -->
    <script src="/static/app.js"></script>
</body>
</html>
```

That's it! Your page now has automatic loading indicators.

## Alternative: Use Base Template

Instead of adding includes to each file, extend the base template:

```html
{% extends "base.html" %}

{% block title %}My Page | FinanceTracker{% endblock %}

{% block content %}
    <h1>My Page</h1>

    <form method="POST">
        <button type="submit">Submit</button>
    </form>
{% endblock %}
```

The base template already includes the loader!

## Customization

### Custom Form Message
```html
<form method="POST"
      data-loading-message="Saving your data..."
      data-loading-subtext="This will just take a moment">
    <button type="submit">Save</button>
</form>
```

### Disable Loader
```html
<form class="no-loader" method="POST">
    <!-- This form won't show loader -->
</form>
```

See [LOADING_INDICATOR_GUIDE.md](LOADING_INDICATOR_GUIDE.md) for complete documentation.
