from telebot import *
from os import path
from data.scripts.check_exist import check
from shutil import rmtree



def init(token ,temp_path):
    global bot, temp_folder

    bot = TeleBot(token, threaded=False)

    if check(temp_path):
        rmtree(temp_path)

    temp_folder = temp_path

    check(temp_path, create=True)



def post():
    import data.conductor as conductor
    @bot.message_handler(func=lambda message: True,
                         content_types=['audio', 'photo', 'voice', 'video', 'document', 'location', 'contact',
                                        'sticker'])
    def receiver(message):
        global temp_folder

        content_type = message.content_type
        user_id = message.from_user.id
        full_message = message

        if content_type == 'photo':
            file = message.photo[len(message.photo) - 1].file_id
            file_extension = '.jpg'
        else:
            file = getattr(getattr(full_message, content_type), 'file_id')
            filename, file_extension = path.splitext(getattr(getattr(full_message, content_type), 'file_name'))

        path_to_content = temp_folder + '/' + str(user_id) + '_' + str(message.id) + '_' + str(message.date) + file_extension

        content = open(path_to_content, 'wb')
        content.write(bot.download_file(bot.get_file(file).file_path))
        content.close()

        try:
            caption = message.caption
        except:
            caption = ''

        conductor.logic(user_id, path_to_content, content_type, full_message, caption=caption)

    @bot.message_handler(commands=['start', 'reset', 'modules', 'reload', 'quit'])
    def commander(message):
        user_id = message.from_user.id

        conductor.command(user_id, message.text)

    @bot.message_handler(func=lambda message: True, content_types=['text'])
    def receiver_text(message):
        if message.text[0] != '/':
            content_type = message.content_type
            user_id = message.from_user.id
            full_message = message

            conductor.logic(user_id, message.text, content_type, full_message)

    @bot.callback_query_handler(func=lambda call: True)
    def ringer(call):
        conductor.logic(call)

    bot.infinity_polling()
