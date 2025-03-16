from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "7210536501:AAHZUlUH-RjJP0DdW7ttG1mOsZX-PKp3m0E"
users_contact_shared = set()  # Store users who have shared contact

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    if user_id in users_contact_shared:
        # User already shared contact, remove buttons & allow normal messaging
        await update.message.reply_text(
            "Welcome back! You have already shared your contact. You can now send messages.",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        # Send welcome image with caption
        await context.bot.send_photo(
            chat_id=chat_id,
            photo="Desktop/femcare logo.jpg",  # Replace with actual image URL or local file
            caption="👋 Welcome to the bot! Please share your contact to continue."
        )

        # Show ONLY the "Share My Contact" button (NO TEXT INPUT FIELD)
        contact_button = [[KeyboardButton("📲 Share My Contact", request_contact=True)]]
        reply_markup = ReplyKeyboardMarkup(contact_button, resize_keyboard=True, one_time_keyboard=True, input_field_placeholder=None)

        await update.message.reply_text(
            "Tap the button below to share your contact:", reply_markup=reply_markup
        )

async def contact_handler(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    contact = update.message.contact
    user_id = user.id

    if contact:
        phone_number = contact.phone_number
        username = user.username if user.username else "No username"

        # Save user as having shared contact
        users_contact_shared.add(user_id)

        # Remove button and allow free chatting
        await update.message.reply_text(
            f"✅ Contact received!\n\n📞 Phone: {phone_number}\n👤 Username: {username}\n\nYou can now send messages.",
            reply_markup=ReplyKeyboardRemove()
        )

async def block_messages(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id not in users_contact_shared:
        await update.message.reply_text("⚠️ You must share your contact first! Please press the '📲 Share My Contact' button.")
        return  # Stop further processing

def main():
    app = Application.builder().token("7210536501:AAHZUlUH-RjJP0DdW7ttG1mOsZX-PKp3m0E").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(MessageHandler(filters.ALL & ~filters.CONTACT, block_messages))  # Block all messages except contact

    app.run_polling()

if __name__ == "__main__":
    main()