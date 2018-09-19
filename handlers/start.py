from telegram import ReplyKeyboardMarkup
import database.users
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    if update.message.chat.username is None:
        update.message.reply_text('📌 ??? ??? ???????? ?????? ??? ??????? ???? ???? ?? ????? ?? ?????? ???.')
    else:
        user = add_user(update)
        reply_keyboard = ReplyKeyboardMarkup([['התחל הרשמה 📝']],
                                             resize_keyboard=True)
        update.message.reply_text('ברוכים הבאים לבוט ההרשמות.\n'
                                  'כאן תוכלו להרשם.',
                                  reply_markup=reply_keyboard)


def add_user(update):
    dbusers = database.users.DbUsers()
    user = dbusers.get_single(user_id=update.message.from_user.id)
    try:
        if user == None:
            new_user = []
            new_user.append(update.message.from_user.id)
            new_user.append(update.message.chat.username)
            new_user.append(update.message.chat.first_name)
            new_user.append(update.message.chat.last_name)
            dbusers.add_new(new_user)
        else:
            pass
    except Exception as ex:
        logger.error(str(ex))
