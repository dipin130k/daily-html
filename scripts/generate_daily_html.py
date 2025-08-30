import os
from datetime import datetime

# Fixed text: "Your" → "My"
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>✨ Daily Inspiration Archive</title>
    <style>
        body {{ font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; }}
        .subtitle {{ color: #7f8c8d; font-size: 1.2em; margin-bottom: 30px; }}
        .days {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 10px; }}
        .day {{ background: #f8f9fa; border-radius: 8px; padding: 10px; text-align: center; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>✨ Daily Inspiration Archive</h1>
    <p class="subtitle">My collection of daily motivational pages</p>  <!-- FIXED LINE -->
    
    <div class="days">
        {days}
    </div>
</body>
</html>
"""

def generate_daily_html():
    # Create daily_html directory if not exists
    os.makedirs("daily_html", exist_ok=True)
    
    # Generate today's page
    today = datetime.now().strftime("%Y-%m-%d")
    daily_file = f"daily_html/{today}.html"
    
    with open(daily_file, "w") as f:
        f.write(f"<h1>Daily Motivation for {today}</h1>")
        f.write("<p>Your inspirational content here...</p>")
    
    # Update index.html with all days
    days = []
    for filename in sorted(os.listdir("daily_html"), reverse=True):
        if filename.endswith(".html"):
            date_str = filename[:-5]
            days.append(f'<div class="day"><a href="daily_html/{filename}">{date_str}</a></div>')
    
    with open("index.html", "w") as f:
        f.write(HTML_TEMPLATE.format(days="\n".join(days)))

if __name__ == "__main__":
    generate_daily_html()
