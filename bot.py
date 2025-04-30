from config import BOT_TOKEN
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from db_utils import save_user,save_message,initialized_database
import logging

#Setting log
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user=update.effective_user
    save_user(user)
    buttons = [
        [KeyboardButton('شروع'), KeyboardButton('راهنما'), KeyboardButton('اطلاعات'), KeyboardButton('ارسال عکس')]]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text('سلام! به ربات من خوش آمدید.هرسوالی دارید بپرسید', reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = ':این ربات به شما کمک می کند\n' \
                '/start-شروع\n' \
                '/help-نمایش راهنما\n' \
                '/info-دریافت اطلاعات\n' \
                'یادکمه های زیر را امتحان کنید'
    await update.message.reply_text(help_text)



async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_message = update.message.text
    save_message(user.id, user_message)
    await update.message.reply_text(f'شما گفتید:{user_message}')


def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


    application.run_polling()


if __name__ == '__main__':
    initialized_database()
    main()

