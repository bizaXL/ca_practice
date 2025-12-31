from . import __version__ as app_version

app_name = "ca_practice"
app_title = "CA Practice"
app_publisher = "Your Name"
app_description = "CA Practice Management"
app_email = "your@email.com"
app_license = "MIT"

# Include js and css files in desk
app_include_js = "/assets/ca_practice/js/ca_practice.js"
app_include_css = "/assets/ca_practice/css/ca_practice.css"

# Scheduled Tasks
scheduler_events = {
    "cron": {
        "0 9 * * *": [
            "ca_practice.utils.send_daily_reminders"
        ]
    }
}
