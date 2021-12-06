import data.core as core
import data.handlers.apihand as apihand
from data.handlers.userhand import write_profile, read_profile
from data.scripts.send_message import send_message

from time import sleep

bot = apihand.bot
master = core.master
dialog = False
command_used = False


def logic(message):
    global dialog, command_used
    if command_used:
        command_used = False
    else:
        match read_profile(message.from_user.id, 'Conductor', 'phase'):
            case '':
                if not dialog:
                    dialog = True
                    send_message(message.from_user.id, 'WOAH!')
                    sleep(4)
                    send_message(message.from_user.id, "You know it's really creepy when someone sneaks up from behind.")
                    sleep(5)
                    send_message(message.from_user.id, "Please, consider next time using /start to call me, for God's sake.")
                    sleep(3)
                    send_message(message.from_user.id, "Anyway...")
                    sleep(3)
                write_profile(message.from_user.id, 'Conductor', 'phase', 'auth')
                logic(message)
            case 'auth':
                i = 0
                modules_buttons = []
                if core.modules[1]:
                    while i < len(core.modules[1]):
                        modules_buttons.append(core.modules[1][i].button)
                        i += 1
                    send_message(message.from_user.id, 'What can I help you with?', keyboard='reply', buttons=modules_buttons)
                    write_profile(message.from_user.id, 'Conductor', 'phase', 'main_menu')
                else:
                    send_message(message.from_user.id, 'Sorry, but you have no modules installed.')

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
                    write_profile(message.from_user.id, 'Conductor', 'phase', 'module')
                    write_profile(message.from_user.id, 'Conductor', 'module', core.modules[1][mod].mod_id)
                    core.modules[1][mod].logic(message)
                else:
                    send_message(message.from_user.id, 'Incorrect module name')

            case 'module':
                # try:
                mod = core.modules[0][read_profile(message.from_user.id, 'Conductor', 'module')]
                core.modules[1][mod].logic(message)
                # except:
                #     send_message(message.from_user.id, 'Module error or you crashed me previous time!')
                #     sleep(2)
                #     set_phase(message, 'auth')
                #     logic(message)

    # else:
    # send_message(message.from_user.id, 'Access denied')


def command(message):
    global command_used
    match message.text:
        case '/start':
            if read_profile(message.from_user.id, 'Conductor', 'phase') != '':
                write_profile(message.from_user.id, 'Conductor', 'phase', 'auth')
        case '/reset':
            write_profile(message.from_user.id, 'Conductor', 'phase', '')
            command_used = True
        case '/modules':
            i = 0
            modules_list = ''
            while i < len(core.modules[1]):
                modules_list += core.modules[1][i].emodji + ' "' + core.modules[1][i].name + '" by ' + core.modules[1][
                    i].author + \
                                '\n   Version: ' + str(core.modules[1][i].version) + '\n   ' \
                                + core.modules[1][i].desc + '\n\n'
                i += 1
            send_message(message.from_user.id, modules_list)
            command_used = True
        case '/reload':
            core.module_setup()
        case '/quit':
            if read_profile(message.from_user.id, 'Conductor', 'phase') == 'module':
                send_message(message.from_user.id, 'Quiting')
                sleep(3)
                write_profile(message.from_user.id, 'Conductor', 'phase', 'auth')
            else:
                send_message(message.from_user.id, "Don't try to trick me! You are not in the module!!")

    logic(message)


"""
@bot.message_handler(commands=['start', 'reset'])
def commander(message):
        match message.text:
            case '/start':
                set_phase(message.from_user.id, 'auth')
                core.sender(message)
            case '/reset':
                bot.send_message(message.from_user.id, 'Fine. Back to the beginning... ', reply_markup=markup)
                core.sender(message)
                set_phase(message.from_user.id, 'auth')
"""
