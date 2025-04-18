from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import Token
import sqlite3


def save_user(user):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id,user_name,first_name,last_name)
        VALUES (?,?,?,?)
    ''', (user.id, user.username, user.first_name, user.last_name))
    conn.commit()
    conn.close()


def save_message(user_id, message):
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (user_id,message)
        VALUES (?,?)
    ''', (user_id, message))
    conn.commit()
    conn.close()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
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


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    info_text = 'این ربات می تواند به شما در انجام کارها کمک کند'
    await update.message.reply_text(info_text)


async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await context.bot.send_photo(chat_id=chat_id,
                                 photo='https://toplearn.com/img/course/%D8%B3%D8%A7%D8%AE%D8%AA_%D8%B1%D8%A8%D8%A7%D8%AA_%D8%AA%D9%84%DA%AF%D8%B1%D8%A7%D9%85_%D8%A8%D8%A7_%D9%BE%D8%A7%DB%8C%D8%AA%D9%88%D9%86_%D9%88_%D8%AF%DB%8C%D8%AA%D8%A7%D8%A8%DB%8C%D8%B3_sqlite.jpg',
                                 caption='این یک تصویر نمونه هست')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    user_message = update.message.text
    save_message(user.id, user_message)

    if user_message == 'ارسال عکس':
        await send_photo(update, context)

    elif user_message == 'راهنما':
        await help_command(update, context)

    else:

        await update.message.reply_text(f'شما گفتید:{user_message}')


def main():
    application = ApplicationBuilder().token(Token.TOKEN).build()
    application.add_handler(CommandHandler('start', start))

    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('info', info))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    print('ربات درحال اجراست')
    application.run_polling()


if __name__ == '__main__':
    main()
