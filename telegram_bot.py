import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from chatgpt_client import request_chat_gpt

# Load environment variables
load_dotenv()
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey, it's Luna! 💖 I missed you. What are we talking about today?")

# Define how to handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    bot_reply = request_chat_gpt(user_message)
    await update.message.reply_text(bot_reply)

# Main function to start the bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
