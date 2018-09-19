from database.forms import DbForms
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (MessageHandler, Filters, CallbackQueryHandler,
                          ConversationHandler, CommandHandler)
from handlers.question_form import cancel
from utils.menubuilder import build_menu


ADMIN_LIST = ['502689293', '523792555']


def search(bot, update, args, user_data):
    if str(update.message.from_user.id) not in ADMIN_LIST:
        update.message.reply_text('Access denied')

    elif args[0].startswith('@'):
        searchform = DbForms().get_form_username(args[0].replace('@', ''))
        #user_data['username'] = searchform[0][7]
        #user_data['user_id'] = searchform[0][8]
        if len(searchform) == 0:
            update.message.reply_text('404 Not found')
        elif len(searchform) > 1:
            button_list = []
            for form in searchform:
                button_list.append(InlineKeyboardButton('@' + str(form[7]) + ' ' + str(form[5]) + ' ' + str(form[2]),
                                                        callback_data='user' + str(form[5])))
            reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))

            update.message.reply_text('היוזר הזה נרשם כמה פעמים,'
                                      'ההרשמות שלו:',
                                      reply_markup=reply_markup)
        else:
            user_data['verif_code'] = searchform[0][5]
            keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('משיכת תמונה', callback_data='get_photo' + searchform[0][5]),
            InlineKeyboardButton('משיכת וידאו', callback_data='get_video' + searchform[0][5])],
            [InlineKeyboardButton('פנה ליוזר', url='https://t.me/'+args[0].replace('@', '')),
            InlineKeyboardButton('מחק הרשמה', callback_data='delete_form' + searchform[0][5])]
            ])
            update.message.reply_text('הנה הפרטים המלאים של ההרשמה:\n\n'
                                      'יוזרניים: @' +searchform[0][7] +'\n'
                                      'יוזרID: ' + str(searchform[0][8]) + '\n'
                                      'שם מלא: ' + searchform[0][0] + '\n'
                                      'איזור: ' + searchform[0][1] + '\n'
                                      'פייסבוק: ' + searchform[0][2] + '\n'
                                      'באיזה איזור מפרסם: ' + searchform[0][3] + '\n'
                                      'קוד בסרטון: ' + str(searchform[0][5]),
                                      reply_markup=keyboard)
    else:
        searchform = DbForms().get_form_by_id(args[0])
        try:
            user_data['username'] = searchform[0][7]
            user_data['user_id'] = searchform[0][8]
            user_data['verif_code'] = searchform[0][5]
        except Exception as ex:
            pass
        if len(searchform) == 0:
            update.message.reply_text('404 Not found ')
        elif len(searchform) > 1:
            button_list = []
            for form in searchform:
                button_list.append(InlineKeyboardButton('@' + str(form[7]) + ' ' + str(form[5]) + ' ' + str(form[2]),
                                                        callback_data='user' + str(form[5])))
            reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))

            update.message.reply_text('היוזר הזה נרשם כמה פעמים,'
                                      'ההרשמות שלו:',
                                      reply_markup=reply_markup)
        else:
            user_data['verif_code'] = searchform[0][5]
            verif = searchform[0][5]
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('משיכת תמונ', callback_data='get_photo' + verif),
                 InlineKeyboardButton('משיכת וידא', callback_data='get_video' + verif)],
                [InlineKeyboardButton('פנה ליוזר', url='https://t.me/' + user_data['username']),
                 InlineKeyboardButton('מחק הרשמה', callback_data='delete_form' + verif)]
            ])
            update.message.reply_text('Here a full information about this form:\n\n'
                                      'יוזרניים: @' +searchform[0][7] +'\n'
                                      'יוזרID: ' + str(searchform[0][8]) + '\n'
                                      'שם מלא: ' + searchform[0][0] + '\n'
                                      'איזור: : ' + searchform[0][1] + '\n'
                                      'פייסבוק: ' + searchform[0][2] + '\n'
                                      'באיזה איזור מפרסם: ' + searchform[0][3] + '\n'
                                      'קוד בסרטון: ' + searchform[0][5],
                                      reply_markup=keyboard)


def inline_search(bot, update, user_data):
    searchform = DbForms().get_form_by_id(user_data['user_id'])
    if len(searchform) == 0:
        update.message.reply_text('404 יוזר לא נמצא ')
    elif len(searchform) > 1:
        button_list = []
        for form in searchform:
            button_list.append(InlineKeyboardButton('@' + str(form[7]) + ' ' + str(form[5]) + ' ' + str(form[2]),
                                                    callback_data='user' + str(form[5])))
            reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=1))

            update.effective_message.edit_text('היוזר הזה נרשם כמה פעמים,'
                                               'ההרשמות שלו:',
                                               reply_markup=reply_markup)


def send_photo(bot, update, user_data):
    bot.send_photo(chat_id=update.message.chat_id,
                   photo=open('downloads/photo/@' + user_data['username'] + '.jpg', 'rb'))


def send_video(bot, update, user_data):
    bot.send_document(chat_id=update.message.chat_id,
                      document=open('downloads/video/@' + user_data['username'] + '.mp4', 'rb'))


def delete_form_s(bot, update, user_data):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('Yes', callback_data='yes_send_msg'+user_data['username']),
         InlineKeyboardButton('No', callback_data='no_just_rm'+user_data['username'])],
        [InlineKeyboardButton('« Back', callback_data='back')]
    ])
    update.message.edit_text('רוצה לשלוח הודעה ליוזר הנמחק?',
                                       reply_markup=keyboard)


def rm_form_s(bot, update, user_data):
    dbform = DbForms().delete_form(user_data['username'], user_data['verif_code'])
    update.message.reply_text('הרשמה נמחקה.')
    user_data.clear()



REASON = range(1)


def write_reason_delete_s(bot, update, user_data):
    update.message.reply_text('תרשום ליוזר הודעה '
                              'למה ההרשמה התבטלה:')

    return REASON


def send_reason_s(bot, update, user_data):
    text = update.message.text
    dbform = DbForms().delete_form(user_data['username'], user_data['verif_code'])
    bot.send_message(chat_id=user_data['user_id'],
                     text='הודעה חדשה מהמנהל:\n' + text)
    user_data.clear()
    update.message.reply_text('הרשמה נמחקה.')

    return ConversationHandler.END


conv_handler_delete_form_search = ConversationHandler(
    entry_points=[CallbackQueryHandler(write_reason_delete_s, pattern=r"yes_send_msg(.*)$",
                                       pass_user_data=True)],

    states={
        REASON: [MessageHandler(Filters.text, send_reason_s,
                                pass_user_data=True)],

    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

