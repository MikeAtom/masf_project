from telebot import *
import data.core as core

bot = TeleBot(core.token, threaded=False)


def post():
    import data.conductor as conductor
    @bot.message_handler(func=lambda message: True,
                         content_types=['audio', 'photo', 'voice', 'video', 'document', 'location', 'contact',
                                        'sticker'])
    def receiver(message):
        conductor.logic(message)

    @bot.message_handler(commands=['start', 'reset', 'modules', 'reload', 'quit'])
    def commander(message):
        conductor.command(message)

    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def receiver(message):
        if message.text[0] != '/':
            conductor.logic(message)

    @bot.callback_query_handler(func=lambda call: True)
    def ringer(call):
        conductor.logic(call)

    bot.infinity_polling()
