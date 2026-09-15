import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Flask server
app = Flask(__name__)

@app.route('/')
def home():
    return "Sanvi Bot is alive and running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

TELEGRAM_TOKEN = "8926160372:AAEkzi_mPy-FpcgckZZPir6u4lMYCXIgtQg"
GEMINI_API_KEY = "AQ.Ab8RN6K5ibSH19CNtjaFFYfDeNz8ZXU_aTeDZt8Afa69pVPisQ"

# Google Cloud / Vertex AI key ke liye explicit transport/configure
genai.configure(api_key=GEMINI_API_KEY)

# Model configuration for Cloud keys
model = genai.GenerativeModel(
    model_name="models/gemini-pro"
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = model.generate_content(user_message)
        if response and response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("Kuch bol hi nahi rahi Sanvi, lagta hai game lag kar gaya.")
    except Exception as e:
        print(f"Error details: {e}")
        await update.message.reply_text(f"Technical Error: {str(e)[:80]}")

def main():
    t = threading.Thread(target=run_web)
    t.start()

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Sanvi Bot is polling...")
    application.run_polling()

if __name__ == '__main__':
    main()
