import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Yahan apna real token aur key daalein
TELEGRAM_TOKEN = "8926160372:AAFSmZn3dsUcbOOHa0xPj3k9G46Ms0ODGDU"
GEMINI_API_KEY = "AQ.Ab8RN6Juhw9iv_EJpnWMYtl2KWtRE1o_hL-XzZdgJ9XotmnZSw"

genai.configure(api_key=GEMINI_API_KEY)

system_instruction = (
    "You are Sanvi, a sarcastic, Hinglish-speaking, BGMI-obsessed gamer girl. "
    "You reply with attitude, gaming slang, and a lot of sass."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = model.generate_content(user_message)
    await update.message.reply_text(response.text)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
