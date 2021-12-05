from data.handlers.apihand import bot, types

def send_message(chat_id, content, file=None, caption='', keyboard=None, buttons=[]):
    """
            Sets phase to entered value
            :param chat_id: Chat ID
            :param content: Message content
            :param file: File type (Optional)
            :param keyboard: 'inline' or 'reply' (Optional)
            :param buttons: for inline - [text, callback data], for reply - text (Optional)
                    """

    if keyboard is not None:
        if keyboard == 'inline':
            i = key_amount = 0
            key_markup = []
            markup = types.InlineKeyboardMarkup(row_width=3)

            for text, data in buttons:
                key_markup.append(types.InlineKeyboardButton(text=text, callback_data=data))  # создание массива кнопок
                key_amount += 1
        elif keyboard == 'reply':
            i = key_amount = 0
            key_markup = []
            markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)

            for text in buttons:
                key_markup.append(types.KeyboardButton(text=text))  # создание массива кнопок
                key_amount += 1

        while i // 3 < key_amount // 3:
            markup.add(key_markup[i], key_markup[i + 1], key_markup[i + 2])  # задача кнопок 3 в ряд
            i += 3
        while key_amount - i > 0:  # задача оставшихся кнопок
            if key_amount - i == 2:  # если осталось 2
                markup.add(key_markup[i], key_markup[i + 1])
                i += 2
            else:  # если осталась 1
                markup.add(key_markup[i])
                i += 1
    else:
        markup = types.ReplyKeyboardRemove(selective=False)

    if type(content) is str and file is None:
        file = 'text'
    elif file is None:
        file = 'document'

    match file:
        case 'text':
            bot.send_message(chat_id, content, reply_markup=markup)
        case 'document':
            bot.send_document(chat_id, content, caption=caption, reply_markup=markup)
        case 'photo':
            bot.send_photo(chat_id, content, caption=caption, reply_markup=markup)
        case 'video':
            bot.send_video(chat_id, content, caption=caption, reply_markup=markup)
        case 'audio':
            bot.send_audio(chat_id, content, caption=caption, reply_markup=markup)
        case 'sticker':
            bot.send_sticker(chat_id, content, reply_markup=markup)
        case 'voice':
            bot.send_voice(chat_id, content, reply_markup=markup)
        # case 'location':

        # case 'contact':
