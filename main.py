from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from textblob import TextBlob
from collections import defaultdict

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Required for Flask sessions

# Memory store for multiple users
chat_histories = defaultdict(list)

import csv
from datetime import datetime

def log_chat(user_msg, sentiment, intent, bot_reply):
    with open("chat_logs.csv", mode="a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_msg,
            sentiment,
            intent,
            bot_reply
        ])

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity < -0.2:
        return "Frustrated"
    elif polarity > 0.2:
        return "Happy"
    else:
        return "Neutral"


def detect_intent(text):
    text = text.lower()
    if any(x in text for x in ["bill", "charged", "amount"]):
        return "Billing"
    elif any(x in text for x in ["internet", "network", "connection","signal",'speed']):
        return "Technical Issue"
    elif any(x in text for x in ["recharge", "balance","top-up"]):
        return "Recharge"
    elif any(x in text for x in ["plan", "offers","package"]):
        return "Plan Info"
    else:
        return "General"


import httpx
import os

from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
 # Replace with your Groq key

def generate_gpt_response(user_id, message, sentiment, intent):
    prompt_intro = "You are a helpful telecom customer service assistant."
    
    # 🧠 Get chat history for this user
    history = chat_histories[user_id]

    # 🧱 Add current message to the history
    history.append({"role": "user", "content": f"User: {message} (Sentiment: {sentiment}, Intent: {intent})"})

    # 🧠 Build full memory-aware messages list
    messages = [{"role": "system", "content": prompt_intro}] + history

    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-70b-8192",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 200
        }

        response = httpx.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"].strip()

        # Add assistant reply to history
        history.append({"role": "assistant", "content": reply})

        return reply

    except Exception as e:
        print("❌ GPT Error:", e)
        return "Sorry, I'm currently having trouble generating a response."


@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body")
    user_id = request.form.get("From")

    print("📩 Incoming SMS request received!")
    print("From:", user_id)
    print("Body:", incoming_msg)

    sentiment = analyze_sentiment(incoming_msg)
    intent = detect_intent(incoming_msg)
    print(f"🧠 Sentiment: {sentiment}, Intent: {intent}")

    response = generate_gpt_response(user_id, incoming_msg, sentiment, intent)
    print(f"🤖 GPT Response: {response}")

    log_chat(incoming_msg, sentiment, intent, response)

    msg = MessagingResponse()
    msg.message(response)
    return str(msg)

if __name__ == "__main__":
    app.run(debug=True)