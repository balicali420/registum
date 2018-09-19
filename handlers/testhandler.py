from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler


def start(bot, update):
    reply_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('🔐 Button1', callback_data='button1')],
        [InlineKeyboardButton('🌐 Button2', callback_data='button2')],
        [InlineKeyboardButton('✅ Button3', callback_data='button3')],
        [InlineKeyboardButton('📶 Button4', callback_data='button4')],
        [InlineKeyboardButton('📌 Button5', callback_data='button5')]
    ])
    update.message.reply_text('Here an example of text formatting\n'  # \n will make one enter
                              '*Here an example of bold text*\n\n'  # \n\n makes two enters \n\n\n 3 enters etc
                              '[Google](http://google.com)\n You just write this words and all ok'
                              '_Here an example of italic text_\n'
                              '`Here an example of code text`\njust write',
                              reply_markup=reply_keyboard, parse_mode=ParseMode.MARKDOWN)


def main():
    updater = Updater('TOKEN_HERE')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
