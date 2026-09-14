import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")

users = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if user_id not in users:
        users[user_id] = 0

    keyboard = [
        ["/balance", "/daily"],
        ["/refer", "/help"]
    ]

    text = (
        f"👋 Welcome {user.first_name}!\n\n"
        "💰 Income Bot\n\n"
        "Use the buttons/commands below:\n"
        "💵 /balance - Check balance\n"
        "🎁 /daily - Get daily bonus\n"
        "👥 /refer - Referral information\n"
        "ℹ️ /help - Help"
    )

    await update.message.reply_text(
        text,
        reply_markup=None
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    amount = users.get(user_id, 0)

    await update.message.reply_text(
        f"💰 Your Balance: {amount} points"
    )


async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    users.setdefault(user_id, 0)
    users[user_id] += 10

    await update.message.reply_text(
        "🎁 Daily Bonus Received!\n\n"
        "💰 +10 points added.\n"
        f"💵 Balance: {users[user_id]} points"
    )


async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    bot_username = context.bot.username

    link = f"https://t.me/{bot_username}?start={user_id}"

    await update.message.reply_text(
        "👥 Invite your friends!\n\n"
        "🔗 Your referral link:\n"
        f"{link}\n\n"
        "🎁 Referral rewards can be added later."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Help\n\n"
        "/start - Start bot\n"
        "/balance - Check balance\n"
        "/daily - Daily bonus\n"
        "/refer - Referral link"
    )


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is missing!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("refer", refer))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
