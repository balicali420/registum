from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (ConversationHandler, CallbackQueryHandler,
                          MessageHandler, Filters, CommandHandler)
from database.forms import DbForms
from utils.menubuilder import build_menu
from handlers.question_form import cancel


ADMIN_LIST = ['502689293', '523792555']


def forms_list(bot, update):
    if str(update.message.from_user.id) not in ADMIN_LIST:
        update.message.reply_text('אין גישה!')
    else:
        dbforms = DbForms().get_all_forms()
        button_list = []
        for form in dbforms:
            button_list.append(InlineKeyboardButton('@' + str(form[7]) + ' ' + str(form[5]) + ' ' + str(form[2]), callback_data='test'+str(form[5])))
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))

        update.message.reply_text('רשימת היוזרים הרשומים:',
                                  reply_markup=reply_markup)


def forms_list_copy(bot, update):
    dbforms = DbForms().get_all_forms()
    button_list = []
    for form in dbforms:
        button_list.append(InlineKeyboardButton('@' + str(form[7]) + ' ' + str(form[5]) + ' ' + str(form[2]), callback_data='test'+str(form[5])))
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))

    update.effective_message.edit_text('רשימת היוזרים הרשומים:',
                                       reply_markup=reply_markup)


def detailed_form(bot, update, user_data):
    """Generates an detail form"""
    query = update.callback_query.data
    cb = ''
    if 'user' in query:
        cb = 'back_to_search_list'
    else:
        cb = 'back_to_forms_list'
    dbform = DbForms().get_form(query[4:])
    user_data['username'] = dbform[0][7]
    user_data['user_id'] = dbform[0][8]
    user_data['verif_code'] = dbform[0][5]
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('משיכת תמונה', callback_data='get_photo' + query[4:]),
         InlineKeyboardButton('משיכת וידא', callback_data='get_video' + query[4:])],
        [InlineKeyboardButton('פנה ליוזר', url='https://t.me/'+ dbform[0][7]),
         InlineKeyboardButton('מחק הרשמה', callback_data='delete_form' + query[4:])],
        [InlineKeyboardButton('« חזור', callback_data=cb)]
    ])
    update.effective_message.edit_text('הנה הפרטים המלאים של ההרשמה:\n\n'
                                       'יוזרניים: @' + dbform[0][7] + '\n'
                                       'יוזרID: : ' + str(dbform[0][8]) + '\n'
                                       'שם מלא: ' + dbform[0][0] + '\n'
                                       'איזור: : ' + dbform[0][1] + '\n'
                                       'פייסבוק: : ' + dbform[0][2] + '\n'
                                       'באיזה איזור מפרסם: ' + dbform[0][3] + '\n'
                                       'קוד בסרטון: ' + str(dbform[0][5]),
                                       reply_markup=keyboard)


def send_photo(bot, update, user_data):
    dbphoto = DbForms().get_form(update.callback_query.data[9:])
    bot.send_photo(chat_id=update.callback_query.message.chat_id,
                   photo=open('downloads/photo/@' + dbphoto[0][7] + '_' + update.callback_query.data[9:] + '.jpg', 'rb'))


def send_video(bot, update, user_data):
    dbvideo = DbForms().get_form(update.callback_query.data[9:])
    bot.send_document(chat_id=update.callback_query.message.chat_id,
                      document=open('downloads/video/@' + dbvideo[0][7] + '_' + dbvideo[0][5] + '.mp4', 'rb'))


def delete_form(bot, update, user_data):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('כ', callback_data='yes_send_msg'+update.callback_query.data[11:]),
         InlineKeyboardButton('לא', callback_data='no_just_rm'+update.callback_query.data[11:])],
        [InlineKeyboardButton('« חזור', callback_data='beek' + update.callback_query.data[11:])]
    ])
    update.effective_message.edit_text('רוצה לרשום סיבה למה היוזר התבטל?',
                                       reply_markup=keyboard)


def rm_form(bot, update, user_data):
    dbusername = DbForms().get_form(update.callback_query.data[10:])
    dbform = DbForms().delete_form(dbusername[0][7], str(update.callback_query.data[10:]))
    update.effective_message.reply_text('Form deleted.')
    user_data.clear()


REASON = range(1)


def write_reason_delete(bot, update, user_data):
    update.effective_message.reply_text('תרשום ליוזר הודעה '
                                        'למה ההרשמה התבטלה:')

    return REASON


def send_reason(bot, update, user_data):
    text = update.message.text
    verif = user_data['verif_code']
    dbusername = DbForms().get_form(verif)
    dbform = DbForms().delete_form(dbusername[0][7], dbusername[0][5])
    bot.send_message(chat_id=user_data['user_id'],
                     text='הודעה חדשה מהמנהל:\n' + text)
    user_data.clear()
    update.effective_message.reply_text('הרשמה נמחקה.')

    return ConversationHandler.END


conv_handler_delete_form = ConversationHandler(
    entry_points=[CallbackQueryHandler(write_reason_delete, pattern=r"yes_send_msg(.*)$",
                                       pass_user_data=True)],

    states={
        REASON: [MessageHandler(Filters.text, send_reason,
                                pass_user_data=True)],

    },

    fallbacks=[CommandHandler('cancel', cancel)]
)
