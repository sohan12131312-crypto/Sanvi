import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from groq import Groq

# Flask server for Render uptime keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Sanvi Bot (Groq Powered) is alive and running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Credentials
TELEGRAM_TOKEN = "8926160372:AAGV-L9MkXcwTbS0CzQPUhSBi5sjF0LX0GI"
GROQ_API_KEY = "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"

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        completion = client.chat.completions.create(
            model="model="llama3-8b-8192"",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Sanvi, a sarcastic, witty, and gaming-obsessed AI companion. "
                        "You love gaming, hate boring questions, and reply with heavy sarcasm "
                        "and a Gen-Z gaming persona in Hinglish."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=0.9,
            max_tokens=250,
        )
        
        reply_text = completion.choices[0].message.content
        if reply_text:
            await update.message.reply_text(reply_text)
        else:
            await update.message.reply_text("Bhai, kuch samajh nahi aaya, dhang se bol.")
            
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text(f"Error aa gaya: {str(e)[:80]}")

def main():
    t = threading.Thread(target=run_web)
    t.start()

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Sanvi Bot (Groq) is polling...")
    application.run_polling()

if __name__ == '__main__':
    main()
