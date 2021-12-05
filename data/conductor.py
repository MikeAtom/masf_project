import data.core as core
import data.handlers.apihand as apihand
import data.handlers.userhand as userhand
from data.scripts.send_message import send_message

from time import sleep

bot = apihand.bot
master = core.master
dialog = False
command_used = False

def logic(message, callback=False):
    global dialog, command_used
    if not callback and message.content_type == 'text' and message.text[0] == '/' and not command_used:
        command_used = True
        match message.text:
            case '/start':
                if userhand.check_phase(message) != '':
                    userhand.set_phase(message, 'auth')
            case '/reset':
                userhand.set_phase(message, 'auth')
            case '/modules':
                i = 0
                modules_list = ''
                while i < len(core.modules[1]):
                    modules_list += core.modules[1][i].emodji + ' "' + core.modules[1][i].name + '" by ' + core.modules[1][i].author + \
                                    '\n   Version: ' + str(core.modules[1][i].version) + '\n   ' \
                                    + core.modules[1][i].desc + '\n\n'
                    i += 1
                    send_message(message.chat.id, modules_list)
            case '/quit':
                if userhand.check_phase(message) == 'module':
                    send_message(message.chat.id, 'Quiting')
                    sleep(3)
                    userhand.set_phase(message, 'auth')
                else:
                    send_message(message.chat.id, "Don't try to trick me! You are not in the module!!")
        logic(message)
    else:
        command_used = False
        match userhand.check_phase(message):
            case '':
                if message.text != '/start' and not dialog:
                    dialog = True
                    send_message(message.chat.id, 'WOAH!')
                    sleep(4)
                    send_message(message.chat.id, "You know it's really creepy when someone sneaks up from behind.")
                    sleep(5)
                    send_message(message.chat.id, "Please, consider next time using /start to call me, for God's sake.")
                    sleep(3)
                    send_message(message.chat.id, "Anyway...")
                    sleep(3)
                userhand.set_phase(message, 'auth')
                logic(message)
            case 'auth':
                global chat_id
                chat_id = message.chat.id

                i = 0
                modules_buttons = []
                if core.modules[1]:
                    while i < len(core.modules[1]):
                        modules_buttons.append(core.modules[1][i].button)
                        i += 1
                    send_message(chat_id, 'What can I help you with?', keyboard='reply', buttons=modules_buttons)
                    userhand.set_phase(message, 'main_menu')
                else:
                    send_message(chat_id, 'Sorry, but you have no modules installed.')

            case 'main_menu':
                global mod
                mod = 0
                correct = False
                while mod < len(core.modules[1]):
                    if message.text == core.modules[1][mod].button:
                        correct = True
                        break
                    mod += 1
                if correct:
                    userhand.set_phase(message, 'module')
                    userhand.set_mod(message, core.modules[1][mod].mod_id)
                    core.modules[1][mod].logic(message)
                else:
                    send_message(message.chat.id, 'Incorrect module name')

            case 'module':
                #try:
                mod = core.modules[0][userhand.check_mod(message)]
                core.modules[1][mod].logic(message)
                # except:
                #     send_message(message.from_user.id, 'Module error or you crashed me previous time!')
                #     sleep(2)
                #     userhand.set_phase(message, 'auth')
                #     logic(message)

    # else:
    # send_message(message.chat.id, 'Access denied')


"""
@bot.message_handler(commands=['start', 'reset'])
def commander(message):
        match message.text:
            case '/start':
                userhand.set_phase(message.chat.id, 'auth')
                core.sender(message)
            case '/reset':
                bot.send_message(message.chat.id, 'Fine. Back to the beginning... ', reply_markup=markup)
                core.sender(message)
                userhand.set_phase(message.chat.id, 'auth')
"""
