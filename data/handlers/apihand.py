from telebot import *
import data.core as core


bot = TeleBot(core.token, threaded=False)


def post():
    @bot.message_handler(func=lambda message: True,
                         content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact',
                                        'sticker'])
    def receiver(message):
        core.sender(message)


    @bot.callback_query_handler(func=lambda call: True)
    def ringer(call):
        core.sender(call, callback=True)


    bot.infinity_polling()