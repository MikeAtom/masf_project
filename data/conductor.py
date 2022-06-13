import data.core as core
import data.handlers.apihand as apihand
from data.handlers.userhand import write_profile, read_profile
from data.scripts.send_message import send_message

from time import sleep

bot = apihand.bot
master = core.master
dialog = False


def logic(user_id, content, content_type, full_message=None, caption='', command=False):
    global dialog
    if not command:
        match read_profile(user_id, 'Conductor', 'phase'):
            case '':
                if not dialog and content_type == 'text':
                    dialog = True
                    send_message(user_id, 'WOAH!')
                    sleep(4)
                    send_message(user_id, "You know it's really creepy when someone sneaks up from behind.")
                    sleep(5)
                    send_message(user_id, "Please, consider next time using /start to call me, for God's sake.")
                    sleep(3)
                    send_message(user_id, "Anyway...")
                    sleep(3)
                write_profile(user_id, 'Conductor', 'phase', 'auth')
                logic(user_id, content, content_type)
            case 'auth':
                if content_type == 'text':
                    i = 0
                    modules_buttons = []
                    if core.modules[1]:
                        while i < len(core.modules[1]):
                            modules_buttons.append(core.modules[1][i].button)
                            i += 1
                        send_message(user_id, 'What can I help you with?', keyboard='reply', buttons=modules_buttons)
                        write_profile(user_id, 'Conductor', 'phase', 'main_menu')
                    else:
                        send_message(user_id, 'Sorry, but you have no modules installed.')
            case 'main_menu':
                if content_type == 'text':
                    global mod
                    mod = 0
                    correct = False
                    while mod < len(core.modules[1]):
                        if content == core.modules[1][mod].button:
                            correct = True
                            break
                        mod += 1
                    if correct:
                        write_profile(user_id, 'Conductor', 'phase', 'module')
                        write_profile(user_id, 'Conductor', 'module', core.modules[1][mod].mod_id)
                        core.modules[1][mod].logic(user_id, content, content_type, full_message, caption)
                    else:
                        send_message(user_id, 'Incorrect module name')

            case 'module':
                # try:
                mod = core.modules[0][read_profile(user_id, 'Conductor', 'module')]
                core.modules[1][mod].logic(user_id, content, content_type, full_message, caption)
                # except:
                #     send_message(user_id, 'Module error or you crashed me previous time!')
                #     sleep(2)
                #     set_phase(message, 'auth')
                #     logic(message)

    # else:
    # send_message(user_id, 'Access denied')


def command(user_id, command):
    global command_used
    match command:
        case '/start':
            if read_profile(user_id, 'Conductor', 'phase') == '':
                write_profile(user_id, 'Conductor', 'phase', 'auth')
            else:
                send_message(user_id, "I'm already here")
            command_used = False
        case '/reset':
            write_profile(user_id, 'Conductor', 'phase', '')
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
            send_message(user_id, modules_list)
            command_used = True
        case '/reload':
            core.module_setup()
            command_used = False
        case '/quit':
            if read_profile(user_id, 'Conductor', 'phase') == 'module':
                send_message(user_id, 'Quiting')
                sleep(1)
                write_profile(user_id, 'Conductor', 'phase', 'auth')
            else:
                send_message(user_id, "Don't try to trick me! You are not in the module!!")
            command_used = False

    logic(user_id, command, 'text', command=command_used)
