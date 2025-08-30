import os
import random
from datetime import datetime

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>✨ Daily Inspiration Archive</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }}
        .container {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        h1 {{
            color: white;
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        .subtitle {{
            color: rgba(255, 255, 255, 0.8);
            font-size: 1.2rem;
            text-align: center;
            margin-bottom: 30px;
        }}
        .days {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
            gap: 15px;
            margin-bottom: 40px;
        }}
        .day {{
            background: rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            padding: 15px 10px;
            text-align: center;
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .day:hover {{
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.25);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }}
        a {{
            color: white;
            text-decoration: none;
            font-weight: 500;
            display: block;
        }}
        .day a:hover {{
            text-decoration: underline;
        }}
        .daily-content {{
            background: rgba(0, 0, 0, 0.2);
            border-radius: 15px;
            padding: 25px;
            margin-top: 30px;
            text-align: center;
        }}
        .quote-container {{
            margin: 30px 0;
            padding: 20px;
            border-left: 4px solid #9b59b6;
        }}
        .quote {{
            font-size: 1.8rem;
            font-style: italic;
            line-height: 1.4;
        }}
        .author {{
            font-size: 1.2rem;
            margin-top: 15px;
            opacity: 0.9;
        }}
        .date {{
            font-size: 1.5rem;
            margin-bottom: 20px;
            color: #f1c40f;
        }}
        .action-button {{
            display: inline-block;
            margin: 30px auto;
            padding: 12px 30px;
            background: #9b59b6;
            color: white;
            border: none;
            border-radius: 50px;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
            text-decoration: none;
        }}
        .action-button:hover {{
            background: #8e44ad;
            transform: scale(1.05);
        }}
        .stars {{
            font-size: 2rem;
            margin: 10px 0;
            color: #f1c40f;
        }}
        .day:nth-child(6n+1) {{ background: rgba(231, 76, 60, 0.7); }}
        .day:nth-child(6n+2) {{ background: rgba(46, 204, 113, 0.7); }}
        .day:nth-child(6n+3) {{ background: rgba(52, 152, 219, 0.7); }}
        .day:nth-child(6n+4) {{ background: rgba(155, 89, 182, 0.7); }}
        .day:nth-child(6n+5) {{ background: rgba(241, 196, 15, 0.7); }}
        .day:nth-child(6n+6) {{ background: rgba(230, 126, 34, 0.7); }}
    </style>
</head>
<body>
    <div class="container">
        <h1>✨ Daily Inspiration Archive</h1>
        <p class="subtitle">My collection of daily motivational pages</p>
        
        <div class="days">
            {days}
        </div>
        
        <div class="daily-content">
            <div class="stars">✨</div>
            <div class="date">Daily Inspiration</div>
            <div class="date">{date}</div>
            
            <div class="quote-container">
                <div class="quote">"{quote}"</div>
                <div class="author">- {author}</div>
            </div>
            
            <div class="stars">🌟</div>
            
            <a href="#" class="action-button">Start My Day Right</a>
        </div>
    </div>
</body>
</html>
"""

# List of inspirational quotes
QUOTES = [
    {"quote": "Don't watch the clock; do what it does. Keep going.", "author": "Sam Levenson"},
    {"quote": "The only way to do great work is to love what you do", "author": "Steve Jobs"},
    {"quote": "Believe you can and you're halfway there", "author": "Theodore Roosevelt"},
    {"quote": "It always seems impossible until it's done", "author": "Nelson Mandela"},
    {"quote": "Success is not final, failure is not fatal: It is the courage to continue that counts", "author": "Winston Churchill"},
    {"quote": "The future belongs to those who believe in the beauty of their dreams", "author": "Eleanor Roosevelt"},
    {"quote": "Do what you can, with what you have, where you are", "author": "Theodore Roosevelt"},
    {"quote": "Happiness is not something ready made. It comes from your own actions", "author": "Dalai Lama"},
    {"quote": "The best time to plant a tree was 20 years ago. The second best time is now", "author": "Chinese Proverb"},
    {"quote": "You miss 100% of the shots you don't take", "author": "Wayne Gretzky"},
    {"quote": "Whether you think you can or you think you can't, you're right", "author": "Henry Ford"}
]

def generate_daily_html():
    # Create daily_html directory if not exists
    os.makedirs("daily_html", exist_ok=True)
    
    # Generate today's page
    today = datetime.now().strftime("%Y-%m-%d")
    daily_file = f"daily_html/{today}.html"
    
    # Select random quote
    selected_quote = random.choice(QUOTES)
    
    with open(daily_file, "w") as f:
        # Format the daily content
        daily_content = HTML_TEMPLATE.format(
            days="",  # Empty for daily pages
            date=today,
            quote=selected_quote["quote"],
            author=selected_quote["author"]
        )
        f.write(daily_content)
    
    # Update index.html with all days
    days = []
    for filename in sorted(os.listdir("daily_html"), reverse=True):
        if filename.endswith(".html"):
            date_str = filename[:-5]
            days.append(f'<div class="day"><a href="daily_html/{filename}">{date_str}</a></div>')
    
    # For index.html, show days grid but hide daily content
    index_html = HTML_TEMPLATE.format(
        days="\n".join(days),
        date="",
        quote="",
        author=""
    ).replace('<div class="daily-content">', '<div class="daily-content" style="display:none;">')
    
    with open("index.html", "w") as f:
        f.write(index_html)

if __name__ == "__main__":
    generate_daily_html()
