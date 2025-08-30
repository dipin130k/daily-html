import os
import json
import random
from datetime import datetime

# ----------------------------------------------------------------------
# 1️⃣  CONFIG – where your quotes live and where the state is stored
# ----------------------------------------------------------------------
QUOTES_FILE = "quotes.txt"          # One quote per line, plain‑text
STATE_FILE  = "used.json"           # Automatically created/updated

# ----------------------------------------------------------------------
# 2️⃣  Load the quote pool
# ----------------------------------------------------------------------
if not os.path.isfile(QUOTES_FILE):
    raise FileNotFoundError(f"❌  You need a file named '{QUOTES_FILE}' with one quote per line.")
with open(QUOTES_FILE, "r", encoding="utf-8") as f:
    quotes = [line.strip() for line in f if line.strip()]   # drop blank lines

total_quotes = len(quotes)
if total_quotes == 0:
    raise ValueError("❌  Your quotes file is empty. Add at least one quote!")

# ----------------------------------------------------------------------
# 3️⃣  Load / initialise the state (which indexes have already been used)
# ----------------------------------------------------------------------
def load_state():
    if os.path.isfile(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Guard against corrupted files
            if isinstance(data, dict) and "used" in data and isinstance(data["used"], list):
                return data
    # Fresh start
    return {"used": []}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

# ----------------------------------------------------------------------
# 4️⃣  Pick a quote that hasn't been shown in the current cycle
# ----------------------------------------------------------------------
def get_new_quote():
    state = load_state()
    used  = set(state["used"])

    # All quotes have been exhausted → start a new round automatically
    if len(used) >= total_quotes:
        used = set()
        state["used"] = []

    # Build a list of still‑available indexes
    available = [i for i in range(total_quotes) if i not in used]

    # Choose one at random
    chosen_index = random.choice(available)

    # Record the choice
    state["used"].append(chosen_index)
    save_state(state)

    return quotes[chosen_index]

# ----------------------------------------------------------------------
# 5️⃣  Prepare today’s file name & colour scheme (your original logic)
# ----------------------------------------------------------------------
os.makedirs("daily_html", exist_ok=True)

today_str   = datetime.utcnow().strftime("%Y-%m-%d")
today_file  = f"daily_html/{today_str}.html"

# ---- colour schemes (you already had these) ----
color_schemes = [
    {"bg": "#FF6B6B", "accent": "#4ECDC4", "text": "#FFFFFF"},
    {"bg": "#A8E6CF", "accent": "#88D8C0", "text": "#2C3E50"},
    {"bg": "#FFD93D", "accent": "#6BCF7F", "text": "#2C3E50"},
    {"bg": "#6C5CE7", "accent": "#A29BFE", "text": "#FFFFFF"},
    {"bg": "#FD79A8", "accent": "#FDCB6E", "text": "#2C3E50"},
    {"bg": "#00B894", "accent": "#00CEC9", "text": "#FFFFFF"},
    {"bg": "#E17055", "accent": "#FDCB6E", "text": "#FFFFFF"}
]
daily_colors = color_schemes[hash(today_str) % len(color_schemes)]

# ----------------------------------------------------------------------
# 6️⃣  Build the daily HTML (your beautiful UI)
# ----------------------------------------------------------------------
daily_quote = get_new_quote()

custom_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Inspiration - {today_str}</title>
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
        h1 {{font-size: 2.5em; margin-bottom: 30px; font-weight: 300;}}
        .quote {{font-size: 1.4em; font-style: italic; margin: 30px 0; line-height: 1.6; opacity: 0.9;}}
        .date-display {{font-size: 1.2em; font-weight: bold; margin: 20px 0;}}
        .decoration {{font-size: 3em; margin: 20px 0; opacity: 0.7;}}
    </style>
</head>
<body>
    <div class="container">
        <div class="decoration">✨</div>
        <h1>Daily Inspiration</h1>
        <div class="date-display">{today_str}</div>
        <div class="quote">"{daily_quote}"</div>
        <div class="decoration">🌟</div>
    </div>
</body>
</html>"""

with open(today_file, "w", encoding="utf-8") as f:
    f.write(custom_html)

# ----------------------------------------------------------------------
# 7️⃣  Re‑build the archive page (index.html) – with "My collection"
# ----------------------------------------------------------------------
files = sorted([f for f in os.listdir("daily_html") if f.endswith(".html")], reverse=True)

with open("index.html", "w", encoding="utf-8") as index:
    index.write("""<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<title>Daily Inspiration Archive</title>
<style>
body { 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    color: white; 
    margin: 0; 
    padding: 30px; 
    min-height: 100vh; 
}
.container { max-width: 1000px; margin: auto; }
h1 { text-align: center; font-size: 3em; margin-bottom: 20px; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }
.subtitle { text-align: center; font-size: 1.2em; opacity: 0.9; margin-bottom: 40px; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
.card { 
    background: rgba(255,255,255,0.15); 
    backdrop-filter: blur(10px); 
    padding: 25px; 
    border-radius: 15px; 
    box-shadow: 0 8px 25px rgba(0,0,0,0.2); 
    transition: transform 0.3s ease; 
}
.card:hover { transform: translateY(-5px); }
.date-badge { 
    background: rgba(255,255,255,0.2); 
    padding: 8px 15px; 
    border-radius: 20px; 
    font-size: 0.9em; 
    display: inline-block; 
    margin-bottom: 15px; 
}
a { color: white; text-decoration: none; font-weight: 600; font-size: 1.1em; }
a:hover { text-decoration: underline; }
</style>
</head><body>
<div class="container">
    <h1>✨ Daily Inspiration Archive</h1>
    <div class="subtitle">My collection of daily motivational pages</div>
    <div class="grid">""") # <-- THIS LINE WAS CHANGED
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

print(f"✅  {today_str} generated with a brand‑new quote.")
print(f"    Quote: “{daily_quote[:80]}…”")
