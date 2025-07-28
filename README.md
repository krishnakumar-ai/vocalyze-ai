# 📞 Vocalyze AI – Agentic AI-Driven Customer Experience (Phase 1)

Vocalyze AI is a smart telecom customer support system built using Flask, Twilio WhatsApp API, Groq's LLaMA3 GPT model, sentiment & intent analysis, and an interactive Streamlit dashboard for analytics.

## 🔥 Features

✅ WhatsApp chatbot via Twilio  
✅ Sentiment analysis using TextBlob  
✅ Intent classification using rule-based NLP  
✅ GPT-powered smart responses (via Groq LLaMA3)  
✅ User-specific memory context  
✅ Logs all chats to `chat_logs.csv`  
✅ Streamlit dashboard with filters, charts, and CSV export  
✅ Deployed on Render

---

## 🏗️ Project Structure

vocalyze-ai/
│
├── main.py # Flask server for Twilio WhatsApp webhook
├── dashboard.py # Streamlit dashboard for chat analytics
├── chat_logs.csv # Chat history log (auto-created)
├── .env # Stores API keys (not pushed to GitHub)
├── requirements.txt # Project dependencies
├── Procfile # For deployment on Render
└── README.md


---

## ⚙️ Technologies Used

- **Python 3.10+**
- **Flask**
- **Twilio WhatsApp API**
- **TextBlob (sentiment)**
- **Groq (LLaMA3 model)**
- **httpx**
- **Streamlit (dashboard)**
- **pandas**

---

## 🚀 How It Works

### 1. Incoming WhatsApp Message

User sends a WhatsApp message ➝ Twilio ➝ POST to `/sms` route in Flask.

### 2. NLP Pipeline

Flask server:
- Performs **sentiment analysis**
- Detects **intent**
- Passes context to **Groq GPT model** for smart reply
- Saves everything to `chat_logs.csv`
- Sends response back to WhatsApp

### 3. Chat Dashboard

Run `dashboard.py` using Streamlit to:
- View all conversations
- Filter by sentiment, intent, or keyword
- See charts for sentiment and intent
- Export filtered CSV

---

## 📦 Installation

### 🔧 1. Clone the repo

```bash
git clone https://github.com/krishnakumar-ai/vocalyze-ai.git
cd vocalyze-ai
# 2.create .env file
api_key

# 3.Twilio Console
# 4. Install 

#Future Improvements
Store chats in database (SQLite/PostgreSQL)

Dashboard admin login

Advanced ML-based intent classification

Host dashboard online

Real-time notification for frustrated users