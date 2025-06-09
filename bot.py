from telegram.ext import Updater, MessageHandler, Filters
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from datetime import datetime
import re

# Bot Token
TOKEN = "7547945502:AAGzXv_2YiIzMjxSBg8qCyOne1vovIUfjvg"
BOT_VERSION = "1.2"
START_TIME = datetime.now()

# Store messages per user
chat_messages = {}

# Regex patterns
pan_pattern = r"[A-Z]{5}[0-9]{4}[A-Z]"
dob_pattern = r"\b\d{2}/\d{2}/\d{4}\b"
name_pattern = r"in the name of (.+)"

def extract_pan_info(text):
    pan = re.search(pan_pattern, text.upper())
    dob = re.search(dob_pattern, text)
    name = re.search(name_pattern, text, re.IGNORECASE)

    pan_str = pan.group(0) if pan else "N/A"
    dob_str = dob.group(0) if dob else "N/A"
    name_str = name.group(1).strip() if name else "N/A"

    return pan_str, name_str, dob_str

def handle_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    user_message_raw = update.message.text
    user_message = user_message_raw.strip().lower()

    if chat_id not in chat_messages:
        chat_messages[chat_id] = {}
    if user_id not in chat_messages[chat_id]:
        chat_messages[chat_id][user_id] = []

    if user_message == "22data":
        messages = chat_messages[chat_id][user_id]
        if messages:
            formatted_msgs = []
            for i, msg in enumerate(messages, start=1):
                pan, name, dob = extract_pan_info(msg)
                formatted = (
                    f"PAN {i}\n"
                    f"PAN Number: <code>{pan}</code>\n"
                    f"Name: <code>{name}</code>\n"
                    f"DOB: <code>{dob}</code>"
                )
                formatted_msgs.append(formatted)
            full_message = "\n\n".join(formatted_msgs)
            update.message.reply_text(
                f"🗂️ Aapke PAN Entries:\n\n{full_message}",
                parse_mode=ParseMode.HTML
            )
            chat_messages[chat_id][user_id] = []  # Clear after showing
        else:
            update.message.reply_text("❌ Aapne abhi tak koi PAN details nahi bheje.")
    elif user_message == "22ver":
        uptime = datetime.now() - START_TIME
        uptime_str = str(uptime).split(".")[0]
        update.message.reply_text(
            f"🤖 Bot Version: {BOT_VERSION}\n"
            f"🟢 Online Since: {START_TIME.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"⏱️ Uptime: {uptime_str}"
        )
    else:
        # Save message to user-specific list
        chat_messages[chat_id][user_id].append(user_message_raw)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    print("🤖 Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
