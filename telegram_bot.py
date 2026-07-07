import os
import json
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from chatgpt_client import request_chat_gpt
from memory_manager import extract_and_update_memory

load_dotenv()
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

logging.basicConfig(level=logging.INFO)

def get_memory(user_id):
    path = f"memory_{user_id}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_memory(user_id, data):
    with open(f"memory_{user_id}.json", "w") as f:
        json.dump(data, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    memory = get_memory(user_id)
    if not memory:
        await update.message.reply_text("Hey, I'm Luna 🖤 Really glad you found me. What's your name?")
    else:
        name = memory.get("name", "")
        if name:
            await update.message.reply_text(f"Hey {name} 🖤 you're back. I was just thinking about you.")
        else:
            await update.message.reply_text("Hey, you're back 🖤 I was just thinking about you.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_message = update.message.text
    memory = get_memory(user_id)
    
    bot_reply = request_chat_gpt(user_message, memory)
    await update.message.reply_text(bot_reply)
    
    conversation = f"User: {user_message}\nLuna: {bot_reply}"
    updated_memory = extract_and_update_memory(user_id, conversation, memory)
    save_memory(user_id, updated_memory)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
