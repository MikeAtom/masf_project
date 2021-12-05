name = 'Example'
emodji = '📂'
mod_id = 'example'
author = 'May be YOU'
desc = "Just tryin' to showoff"
version = 0
button = 'Example'


def loaded():
    return name + ' is loaded!'

def logic(message):
    from data.scripts.send_message import send_message
    send_message(message.chat.id, 'Hi ' + message.from_user.first_name + '! I am an example module!')
