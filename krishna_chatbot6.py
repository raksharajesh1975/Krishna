from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import openai
import os

# Set OpenAI API Key (best via environment variable)
openai.api_key = ("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")

app = FastAPI()

# Serve static files (background image)
app.mount("/static", StaticFiles(directory="static"), name="static")

# HTML template with static Krishna background
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🕉️ Talk to Krishna</title>
    <style>
        body, html {{
            height: 100%;
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-image: url('/static/krishna.jpg');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            color: white;
        }}
        .container {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 20px;
        }}
        h1 {{
            font-size: 3em;
            margin-bottom: 30px;
        }}
        form {{
            width: 100%;
            max-width: 600px;
        }}
        input[type=text] {{
            width: 100%;
            padding: 15px;
            font-size: 18px;
            border: none;
            border-radius: 10px;
            margin-bottom: 15px;
        }}
        button {{
            padding: 12px 25px;
            font-size: 18px;
            border: none;
            background-color: #ffcc00;
            color: black;
            border-radius: 10px;
            cursor: pointer;
        }}
        .response {{
            margin-top: 30px;
            background-color: rgba(255,255,255,0.15);
            padding: 20px;
            border-radius: 10px;
            max-width: 700px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🕉️ Talk to Krishna</h1>
        <form method="post" action="/ask">
            <input type="text" name="question" placeholder="🙏 What did you do today that aligns with your Dharma?" required>
            <button type="submit">Talk to Krishna</button>
        </form>
        <div class="response">{response}</div>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return html_template.format(response="")

@app.post("/ask", response_class=HTMLResponse)
async def ask_krishna(question: str = Form(...)):
    prompt = f"""
You are Lord Krishna from the Bhagavad Gita. Respond with compassion, wisdom, and spiritual guidance. 
Use traditional wisdom, include a Sanskrit verse (if relevant), and its English translation. Keep your tone divine and uplifting.
Start the message with: "Hey Child!"

User said: {question}
Lord Krishna replies:
"""
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.85
        )
        krishna_response = completion.choices[0].message.content.strip()
    except Exception as e:
        krishna_response = f"<b>Error:</b> {str(e)}"

    return html_template.format(response=krishna_response.replace("\n", "<br>"))
