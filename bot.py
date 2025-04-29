from config import BOT_TOKEN,DATABASE_PATH
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from db_utils import save_user
import logging

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [
        [KeyboardButton('شروع'), KeyboardButton('راهنما'), KeyboardButton('اطلاعات'), KeyboardButton('ارسال عکس')]]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text('سلام! به ربات من خوش آمدید.هرسوالی دارید بپرسید', reply_markup=reply_markup)


def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))

    application.run_polling()


if __name__ == '__main__':
    main()

