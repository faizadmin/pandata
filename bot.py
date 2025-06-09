
from telegram.ext import Updater, MessageHandler, Filters
from telegram import Update
from telegram.ext import CallbackContext
from datetime import datetime

# Bot Token
TOKEN = "7547945502:AAGzXv_2YiIzMjxSBg8qCyOne1vovIUfjvg"
BOT_VERSION = "1.0"
START_TIME = datetime.now()

# Messages dictionary: {chat_id: {user_id: [messages]}}
chat_messages = {}

def handle_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_message = update.message.text.strip().lower()

    # Initialize chat and user if not present
    if chat_id not in chat_messages:
        chat_messages[chat_id] = {}
    if user_id not in chat_messages[chat_id]:
        chat_messages[chat_id][user_id] = []

    if user_message == "22data":
        messages = chat_messages[chat_id][user_id]
        if messages:
            combined_message = "\n".join(messages)
            update.message.reply_text(f"ðŸ—‚ï¸ Aapke Saved Messages:\n\n{combined_message}")
            chat_messages[chat_id][user_id] = []  # Clear after sending
        else:
            update.message.reply_text("âŒ Aapke koi message save nahi huye.")
    elif user_message == "22ver":
        uptime = datetime.now() - START_TIME
        uptime_str = str(uptime).split(".")[0]
        update.message.reply_text(f"ðŸ¤– Bot Version: {BOT_VERSION}\nðŸŸ¢ Online Since: {START_TIME.strftime('%Y-%m-%d %H:%M:%S')}\nâ±ï¸ Uptime: {uptime_str}")
    else:
        # Save message to user-specific list
        chat_messages[chat_id][user_id].append(update.message.text)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add handler for all text messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    print("ðŸ¤– Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
