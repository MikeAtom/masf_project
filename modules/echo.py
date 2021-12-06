name = 'Echo'
emodji = '📡'
mod_id = 'echo'
author = 'MikeAtom'
desc = "Advanced echo module that can relay all content_types of messages"
version = 0
button = 'Echo'


def loaded():
    return name + ' is loaded!'


def logic(user_id, content, content_type, full_message, caption):
    from data.scripts.send_message import send_message

    send_message(user_id, content, content_type)

