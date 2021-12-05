name = 'Echo'
emodji = '📡'
mod_id = 'echo'
author = 'MikeAtom'
desc = "Advanced echo module that can relay all types of messages"
version = 0
button = 'Echo'


def loaded():
    return name + ' is loaded!'


def logic(message):
    from data.scripts.send_message import send_message
    type = message.content_type
    chat_id = message.chat.id
    try:
        caption = message.caption
    except:
        caption = None

    if type == 'text':
        send_message(chat_id, message.text, file=type)
    elif type == 'photo':
        send_message(chat_id, message.json['photo'][0]['file_id'], caption=caption,
                     file=type)  # На эту строчку ушёл час
    else:
        contents = getattr(message, type + '.file_id')
        send_message(chat_id, contents, caption=caption, file=type)
