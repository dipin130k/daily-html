import os
from datetime import datetime
import random

# Create HTML output folder if it doesn't exist
os.makedirs("daily_html", exist_ok=True)

# Today's date for file naming
today = datetime.utcnow().strftime("%Y-%m-%d")
filename = f"daily_html/{today}.html"

# Daily inspirational quotes
quotes = [
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "Code is like humor. When you have to explain it, it's bad.",
    "The only way to do great work is to love what you do.",
    "Innovation distinguishes between a leader and a follower.",
    "Stay hungry, stay foolish.",
    "The future belongs to those who believe in the beauty of their dreams.",
    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "Don't watch the clock; do what it does. Keep going."
]

# Color schemes for different days
color_schemes = [
    {"bg": "#FF6B6B", "accent": "#4ECDC4", "text": "#FFFFFF"},
    {"bg": "#A8E6CF", "accent": "#88D8C0", "text": "#2C3E50"},
    {"bg": "#FFD93D", "accent": "#6BCF7F", "text": "#2C3E50"},
    {"bg": "#6C5CE7", "accent": "#A29BFE", "text": "#FFFFFF"},
    {"bg": "#FD79A8", "accent": "#FDCB6E", "text": "#2C3E50"},
    {"bg": "#00B894", "accent": "#00CEC9", "text": "#FFFFFF"},
    {"bg": "#E17055", "accent": "#FDCB6E", "text": "#FFFFFF"}
]

# Select daily content
daily_quote = random.choice(quotes)
daily_colors = color_schemes[hash(today) % len(color_schemes)]  # Same color for same date

custom_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Inspiration - {today}</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, {daily_colors['bg']} 0%, {daily_colors['accent']} 100%);
            color: {daily_colors['text']};
            margin: 0;
            padding: 50px 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .container {{
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            max-width: 600px;
            text-align: center;
        }}
        h1 {{
            font-size: 2.5em;
            margin-bottom: 30px;
            font-weight: 300;
        }}
        .quote {{
            font-size: 1.4em;
            font-style: italic;
            margin: 30px 0;
            line-height: 1.6;
            opacity: 0.9;
        }}
        .date-display {{
            font-size: 1.2em;
            font-weight: bold;
            margin: 20px 0;
        }}
        .decoration {{
            font-size: 3em;
            margin: 20px 0;
            opacity: 0.7;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="decoration">✨</div>
        <h1>Daily Inspiration</h1>
        <div class="date-display">{today}</div>
        <div class="quote">"{daily_quote}"</div>
        <div class="decoration">🌟</div>
    </div>
</body>
</html>"""

# Generate the daily HTML file
with open(filename, "w") as f:
    f.write(custom_html)

# Enhanced index.html with better styling
files = sorted([f for f in os.listdir("daily_html") if f.endswith(".html")], reverse=True)

with open("index.html", "w") as index:
    index.write(f"""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<title>Daily Inspiration Archive</title>
<style>
body {{ 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    color: white; 
    margin: 0; 
    padding: 30px; 
    min-height: 100vh; 
}}
.container {{ max-width: 1000px; margin: auto; }}
h1 {{ text-align: center; font-size: 3em; margin-bottom: 20px; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }}
.subtitle {{ text-align: center; font-size: 1.2em; opacity: 0.9; margin-bottom: 40px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
.card {{ 
    background: rgba(255,255,255,0.15); 
    backdrop-filter: blur(10px); 
    padding: 25px; 
    border-radius: 15px; 
    box-shadow: 0 8px 25px rgba(0,0,0,0.2); 
    transition: transform 0.3s ease; 
}}
.card:hover {{ transform: translateY(-5px); }}
.date-badge {{ 
    background: rgba(255,255,255,0.2); 
    padding: 8px 15px; 
    border-radius: 20px; 
    font-size: 0.9em; 
    display: inline-block; 
    margin-bottom: 15px; 
}}
a {{ color: white; text-decoration: none; font-weight: 600; font-size: 1.1em; }}
a:hover {{ text-decoration: underline; }}
</style>
</head><body>
<div class="container">
    <h1>✨ Daily Inspiration Archive</h1>
    <div class="subtitle">Your collection of daily motivational pages</div>
    <div class="grid">""")
    
    for f in files:
        date_str = f.replace(".html", "")
        index.write(f'''
        <div class="card">
            <div class="date-badge">{date_str}</div>
            <a href="daily_html/{f}">View Inspiration →</a>
        </div>''')
    
    index.write("""
    </div>
</div>
</body></html>""")

print(f"Generated {filename} with daily quote and custom colors")
print(f"Quote of the day: {daily_quote[:50]}...")
