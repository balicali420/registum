import logging
from telegram import ReplyKeyboardRemove
from telegram.ext import (ConversationHandler, MessageHandler, Filters,
                          CommandHandler, RegexHandler)
from utils.generate_code import generate_code
import database.forms

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

NAME, GEO, CHANNEL, POSTS_TYPE, PHOTO, VIDEO = range(6)


def form(bot, update, user_data):
    update.message.reply_text(
        'שלב ראשון \n'
        'אנא הכנס את שמך המלא:')

    return NAME


def name(bot, update, user_data):
    user_data['name'] = update.message.text
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('הכנס את המספר פלאפון שממנו פתחתה את היוזר !!')

    return GEO


def geo(bot, update, user_data):
    user_data['geo'] = update.message.text
    user_data['username'] = update.message.chat.username
    user = update.message.from_user
    logger.info("Geo of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('מאיפה אתה בארץ ? ואיזה איזור מעוניין לעבוד ?:')

    return CHANNEL


def channel(bot, update, user_data):
    user_data['channel'] = update.message.text
    user = update.message.from_user
    logger.info("Channel to manage of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('שלח לינק של הפייסבוק הפרטי שלך:')

    return POSTS_TYPE


def posts_type(bot, update, user_data):
    user_data['posts_type'] = update.message.text
    user = update.message.from_user
    logger.info("Amount of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('תמונה סלפי עם תעודת זהות שלך צמוד אליך ושיראו אותה ברור!:')

    return PHOTO


def photo(bot, update, user_data):
    user_data['photo'] = 'test'
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)

    logger.info("User %s uploaded an photo", user.first_name)
    code = generate_code()
    user_data['code'] = code
    user_data['verif_code'] = code
    update.message.reply_text('לצורך אימות שאינך מתחזה. '
                              'סרטון סלפי שלך עם 50 גרם ואומר אני רוצה ליהות סוחר מאומת בישראנאביס והקוד שלי הוא:'
                               + code)
    photo_file.download('downloads/photo/@' + str(user.username) + '_' + str(code) + '.jpg')

    return VIDEO


def video(bot, update, user_data):
    user_data['video'] = 'test'
    user_data['user_id'] = update.message.from_user.id
    user = update.message.from_user
    gif_file = bot.get_file(file_id=update.message.video.file_id)
    gif_file.download('downloads/video/@' + update.message.from_user.username + '_' + str(user_data['code']) + '.mp4')
    logger.info("verification code of %s: %s", user.first_name, 'user_video.mp4')
    update.message.reply_text('תודה על הרשמתך לקבוצה שלנו'
                              ' מנהל יבדוק שהכל תקין ויצור קשר בהקדם.')

    form_info = []
    form_info.append(user_data['name'])
    form_info.append(user_data['geo'])
    form_info.append(user_data['channel'])
    form_info.append(user_data['posts_type'])
    form_info.append(user_data['photo'])
    form_info.append(user_data['verif_code'])
    form_info.append(user_data['video'])
    form_info.append(user_data['username'])
    form_info.append(user_data['user_id'])
    dbform = database.forms.DbForms()
    dbform.create_form(form_info)
    bot.send_message(chat_id=502689293 && chat_id=674045820, text='הרשמה חדשה מ @' + str(user_data['username'])
                     + ' id:' + str(user_data['user_id']))
    user_data.clear()
    return ConversationHandler.END


def text(bot, update, user_data):
    update.message.reply_text('שאלה זאת מקבלת תמונות בלבד אנא שלח סלפי עם התעודת זהות בברור')

    return PHOTO


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('האימות שלך בוטל אם ברצונך לשלוח שוב אנא התחל אימות מחדש.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[RegexHandler('^התחל באימות 📝$', form, pass_user_data=True)],

    states={
        NAME: [MessageHandler(Filters.text, name, pass_user_data=True)],

        GEO: [MessageHandler(Filters.text, geo, pass_user_data=True)],

        CHANNEL: [MessageHandler(Filters.text, channel, pass_user_data=True)],

        POSTS_TYPE: [MessageHandler(Filters.text, posts_type, pass_user_data=True)],

        PHOTO: [MessageHandler(Filters.photo, photo, pass_user_data=True),
                MessageHandler(Filters.text, text, pass_user_data=True)],

        VIDEO: [MessageHandler(Filters.document | Filters.video | Filters.animation, video, pass_user_data=True)],

    },

    fallbacks=[CommandHandler('cancel', cancel)]
)
