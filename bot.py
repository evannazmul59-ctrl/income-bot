import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

users = {}
withdraw_requests = []

TASKS = [
    {
        "name": "📢 Task 1",
        "url": "https://example.com",
        "reward": 20,
    },
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.setdefault(user_id, 0)

    await update.message.reply_text(
        "👋 Welcome to Income Site!\n\n"
        "💰 /balance - Balance\n"
        "📋 /tasks - Available tasks\n"
        "🎁 /daily - Daily bonus\n"
        "👥 /refer - Referral link\n"
        "💸 /withdraw - Withdraw points\n"
        "ℹ️ /help - Help"
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(
        f"💰 Your Balance: {users.get(user_id, 0)} points"
    )


async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.setdefault(user_id, 0)
    users[user_id] += 10

    await update.message.reply_text(
        f"🎁 Daily Bonus: +10 points\n\n"
        f"💰 Balance: {users[user_id]} points"
    )


async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "📋 Available Tasks\n\n"

    for i, task in enumerate(TASKS, 1):
        text += (
            f"{i}. {task['name']}\n"
            f"💰 Reward: {task['reward']} points\n"
            f"🔗 {task['url']}\n\n"
        )

    text += "⚠️ Complete only legitimate tasks."
    await update.message.reply_text(text)


async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = context.bot.username

    link = f"https://t.me/{username}?start={user_id}"

    await update.message.reply_text(
        f"👥 Your Referral Link:\n\n{link}"
    )


async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    balance_amount = users.get(user_id, 0)

    if not context.args:
        await update.message.reply_text(
            "💸 Withdraw\n\n"
            "Example: /withdraw 100\n"
            "Minimum: 100 points"
        )
        return

    try:
        amount = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Enter a valid number.")
        return

    if amount < 100:
        await update.message.reply_text(
            "❌ Minimum withdrawal is 100 points."
        )
        return

    if amount > balance_amount:
        await update.message.reply_text(
            f"❌ Insufficient balance.\n"
            f"Your balance: {balance_amount} points"
        )
        return

    users[user_id] -= amount

    withdraw_requests.append({
        "user_id": user_id,
        "amount": amount
    })

    await update.message.reply_text(
        "✅ Withdrawal request submitted!\n\n"
        f"💰 Amount: {amount} points\n"
        "⏳ Status: Pending"
    )

    if ADMIN_ID:
        await context.bot.send_message(
            ADMIN_ID,
            f"💸 NEW WITHDRAW REQUEST\n\n"
            f"👤 User ID: {user_id}\n"
            f"💰 Amount: {amount} points"
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Help\n\n"
        "/start\n"
        "/balance\n"
        "/tasks\n"
        "/daily\n"
        "/refer\n"
        "/withdraw"
    )


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN is missing!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("tasks", tasks))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("refer", refer))
    app.add_handler(CommandHandler("withdraw", withdraw))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
