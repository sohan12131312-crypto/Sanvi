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

# API Keys & Setup
TELEGRAM_TOKEN = "8926160372:AAEkzi_mPy-FpcgckZZPir6u4lMYCXIgtQg"
GEMINI_API_KEY = "AQ.Ab8RN6K5ibSH19CNtjaFFYfDeNz8ZXU_aTeDZt8Afa69pVPisQ"

# Google Cloud / Vertex style ya direct configure
genai.configure(api_key=GEMINI_API_KEY)

# Model initialization with safety/fallback
generation_config = {
    "temperature": 0.9,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "You are Sanvi, a sarcastic, witty, and gaming-obsessed AI companion. "
        "You love gaming, hate boring questions, and reply with heavy sarcasm "
        "and a Gen-Z gaming persona."
    )
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = model.generate_content(user_message)
        if response and response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("Bhai, kuch samajh nahi aaya, dhang se bol.")
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text(f"Error aa gaya: {str(e)[:50]}")

def main():
    t = threading.Thread(target=run_web)
    t.start()

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Sanvi Bot is polling...")
    application.run_polling()

if __name__ == '__main__':
    main()
