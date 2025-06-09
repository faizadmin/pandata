
from telegram.ext import Updater, MessageHandler, Filters
from telegram import Update
from telegram.ext import CallbackContext

# Aapki Bot Token
TOKEN = "7547945502:AAGzXv_2YiIzMjxSBg8qCyOne1vovIUfjvg"

# Messages ko store karne ke liye dictionary (chat-wise)
chat_messages = {}

def handle_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_message = update.message.text

    # Agar command "22data" hai
    if user_message.strip().lower() == "22data":
        messages = chat_messages.get(chat_id, [])
        if messages:
            combined_message = "\n".join(messages)
            update.message.reply_text(f"🗂️ Saved Messages:\n\n{combined_message}")
            chat_messages[chat_id] = []  # Clear after sending
        else:
            update.message.reply_text("❌ Koi message save nahi hua hai.")
    else:
        # Save message to list
        chat_messages.setdefault(chat_id, []).append(user_message)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add message handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    print("🤖 Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
