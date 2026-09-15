import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# 1. Chota sa Flask server (Render ke Free tier ko zinda rakhne ke liye)
app = Flask(__name__)

@app.route('/')
def home():
    return "Sanvi Bot is alive and running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# 2. Telegram Bot aur Gemini API setup
TELEGRAM_TOKEN = "8926160372:AAFSmZn3dsUcbOOHa0xPj3k9G46Ms0ODGDU"
GEMINI_API_KEY = "AQ.Ab8RN6LJAY4C_DpAepnLY6qmCd1H42Iukxr16AJp4_xgLmhq_Q"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
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
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Bhai, dimaag mat kha, mera server thoda confuse ho gaya hai.")

def main():
    # Background mein Flask server chalu karo
    t = threading.Thread(target=run_web)
    t.start()

    # Telegram bot start karo
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Sanvi Bot is polling...")
    application.run_polling()

if __name__ == '__main__':
    main()
