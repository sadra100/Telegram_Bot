from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import Token



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('سلام! به ربات من خوش آمدید.هرسوالی دارید بپرسید')


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


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
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
