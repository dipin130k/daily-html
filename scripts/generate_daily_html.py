import os
import json
from datetime import datetime, timedelta

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
        }}
        .quote {{
            font-size: 1.8rem;
            font-style: italic;
            text-align: center;
            margin-bottom: 20px;
            line-height: 1.4;
        }}
        .author {{
            text-align: right;
            font-size: 1.1rem;
            opacity: 0.8;
        }}
        .image-placeholder {{
            height: 200px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 25px 0;
            font-style: italic;
        }}
        .action-button {{
            display: block;
            width: 200px;
            margin: 30px auto;
            padding: 12px 20px;
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
            <h2>Daily Inspiration for {date}</h2>
            <div class="quote">"{quote}"</div>
            <div class="author">- {author}</div>
            
            <div class="image-placeholder">
                [Your Inspirational Image Here]
            </div>
            
            <p>Today's challenge: {challenge}</p>
            
            <a href="#" class="action-button">Start My Day Right</a>
        </div>
    </div>
</body>
</html>
"""

QUOTES = [
    {"quote": "The only way to do great work is to love what you do", "author": "Steve Jobs"},
    {"quote": "Believe you can and you're halfway there", "author": "Theodore Roosevelt"},
    {"quote": "It always seems impossible until it's done", "author": "Nelson Mandela"},
    {"quote": "Success is not final, failure is not fatal: It is the courage to continue that counts", "author": "Winston Churchill"},
    {"quote": "The future belongs to those who believe in the beauty of their dreams", "author": "Eleanor Roosevelt"},
    {"quote": "Do what you can, with what you have, where you are", "author": "Theodore Roosevelt"},
    {"quote": "Happiness is not something ready made. It comes from your own actions", "author": "Dalai Lama"},
    {"quote": "The best time to plant a tree was 20 years ago. The second best time is now", "author": "Chinese Proverb"},
    {"quote": "You miss 100% of the shots you don't take", "author": "Wayne Gretzky"},
    {"quote": "Whether you think you can or you think you can't, you're right", "author": "Henry Ford"},
    {"quote": "The journey of a thousand miles begins with one step", "author": "Lao Tzu"},
    {"quote": "That which does not kill us makes us stronger", "author": "Friedrich Nietzsche"},
    {"quote": "Life is what happens when you're busy making other plans", "author": "John Lennon"},
    {"quote": "When the going gets tough, the tough get going", "author": "Joe Kennedy"},
    {"quote": "You must be the change you wish to see in the world", "author": "Mahatma Gandhi"},
    {"quote": "You only live once, but if you do it right, once is enough", "author": "Mae West"},
    {"quote": "Tough times never last, but tough people do", "author": "Robert H. Schuller"},
    {"quote": "Get busy living or get busy dying", "author": "Stephen King"},
    {"quote": "Twenty years from now you will be more disappointed by the things that you didn't do than by the ones you did do", "author": "Mark Twain"},
    {"quote": "Great minds discuss ideas; average minds discuss events; small minds discuss people", "author": "Eleanor Roosevelt"}
]

CHALLENGES = [
    "Compliment three people today",
    "Learn something new outside your comfort zone",
    "Spend 15 minutes in meditation or quiet reflection",
    "Do one act of kindness without expecting anything in return",
    "Write down three things you're grateful for",
    "Take a 30-minute walk in nature",
    "Reach out to someone you haven't spoken to in a while",
    "Try a new healthy recipe for dinner",
    "Read a chapter of an inspiring book",
    "Write a short journal entry about your goals",
    "Create a small piece of art (drawing, poem, music)",
    "Exercise for at least 30 minutes",
    "Declutter one area of your living space",
    "Set a new personal or professional goal",
    "Practice a skill you've been wanting to improve",
    "Watch an educational documentary",
    "Donate to a cause you care about",
    "Try a digital detox for 2 hours",
    "Write a thank-you note to someone who helped you",
    "Plan your ideal day and try to implement it"
]

def get_next_quote():
    """Get the next quote in sequence without repeating until all are used"""
    # Load state
    state_file = "quote_state.json"
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            state = json.load(f)
    else:
        state = {"last_used": -1, "used_quotes": []}
    
    # Reset if all quotes have been used
    if len(state["used_quotes"]) >= len(QUOTES):
        state["used_quotes"] = []
    
    # Find next available quote
    next_index = (state.get("last_used", -1) + 1) % len(QUOTES)
    while next_index in state["used_quotes"]:
        next_index = (next_index + 1) % len(QUOTES)
    
    # Update state
    state["last_used"] = next_index
    state["used_quotes"].append(next_index)
    
    # Save state
    with open(state_file, "w") as f:
        json.dump(state, f)
    
    return QUOTES[next_index]

def get_next_challenge():
    """Get the next challenge in sequence without repeating until all are used"""
    # Load state
    state_file = "challenge_state.json"
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            state = json.load(f)
    else:
        state = {"last_used": -1, "used_challenges": []}
    
    # Reset if all challenges have been used
    if len(state["used_challenges"]) >= len(CHALLENGES):
        state["used_challenges"] = []
    
    # Find next available challenge
    next_index = (state.get("last_used", -1) + 1) % len(CHALLENGES)
    while next_index in state["used_challenges"]:
        next_index = (next_index + 1) % len(CHALLENGES)
    
    # Update state
    state["last_used"] = next_index
    state["used_challenges"].append(next_index)
    
    # Save state
    with open(state_file, "w") as f:
        json.dump(state, f)
    
    return CHALLENGES[next_index]

def generate_daily_html():
    # Create daily_html directory if not exists
    os.makedirs("daily_html", exist_ok=True)
    
    # Generate today's page
    today = datetime.now().strftime("%Y-%m-%d")
    daily_file = f"daily_html/{today}.html"
    
    # Get next quote and challenge
    selected_quote = get_next_quote()
    selected_challenge = get_next_challenge()
    
    with open(daily_file, "w") as f:
        # Format the daily content
        daily_content = HTML_TEMPLATE.format(
            days="",  # Empty for daily pages
            date=today,
            quote=selected_quote["quote"],
            author=selected_quote["author"],
            challenge=selected_challenge
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
        author="",
        challenge=""
    ).replace('<div class="daily-content">', '<div class="daily-content" style="display:none;">')
    
    with open("index.html", "w") as f:
        f.write(index_html)

if __name__ == "__main__":
    generate_daily_html()
