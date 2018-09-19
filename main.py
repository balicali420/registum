from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, ConversationHandler, CallbackQueryHandler)
from handlers.start import start
from handlers.question_form import conv_handler
from handlers.admin_menu.forms_list import (forms_list, detailed_form, send_photo, send_video, delete_form,
                                            conv_handler_delete_form, rm_form, forms_list_copy,)
from handlers.admin_menu.search import search, inline_search
import logging
from handlers.testhandler import test

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Here registering functions and starting webhook|polling."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("TOKEN_HERE")
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(start, pattern='username_set'))
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('admin', forms_list))
    dp.add_handler(CallbackQueryHandler(detailed_form, pattern=r"test(.*)$",
                                        pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(send_photo, pattern=r"get_photo(.*)$",
                                        pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(send_video, pattern=r"get_video(.*)$",
                                        pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(delete_form, pattern=r"delete_form(.*)$",
                                        pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(rm_form, pattern=r"no_just_rm(.*)$",
                                        pass_user_data=True))
    # back
    dp.add_handler(CallbackQueryHandler(forms_list_copy, pattern='back_to_forms_list'))
    dp.add_handler(CallbackQueryHandler(detailed_form, pattern=r"beek(.*)$",
                                        pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(inline_search, pattern='back_to_search_list', pass_user_data=True))
    dp.add_handler(conv_handler_delete_form)
    dp.add_handler(CommandHandler('search', search, pass_args=True, pass_user_data=True))
    dp.add_handler(CallbackQueryHandler(detailed_form, pattern=r"user(.*)$",
                                        pass_user_data=True))
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler('test', test))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()