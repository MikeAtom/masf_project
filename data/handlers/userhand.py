from data.core import logger
from data.scripts.check_exist import check
import configparser

folder = './data/users'
check(folder)


def create_profile(message):
    profile = configparser.ConfigParser()
    user_id = message.from_user.id
    username = message.from_user.username
    chat_id = message.chat.id

    file_path = folder + '/' + str(user_id) + '.usr'

    profile.add_section("Info")
    profile.set("Info", "username", username)
    profile.set("Info", "id", str(user_id))
    profile.set("Info", "chat_id", str(chat_id))
    profile.add_section("Data")
    profile.set("Data", "phase", "")
    profile.set("Data", "module", "")

    with open(file_path, "w") as config_file:
        profile.write(config_file)


def check_profile(message):
    file_path = folder + '/' + str(message.from_user.id) + '.usr'
    if not check(file_path):
        create_profile(message)
    return file_path


def check_phase(message):
    profile = configparser.ConfigParser()
    profile.read(check_profile(message))

    return profile.get("Data", "phase")


def set_phase(message, is_set):
    """
            Sets phase to entered value
            :param message:
            :param is_set: Change to
                """
    profile = configparser.ConfigParser()
    file_path = check_profile(message)

    profile.read(file_path)
    profile.set("Data", "phase", is_set)

    with open(file_path, "w") as config_file:
        profile.write(config_file)

    logger('Phase changed to ' + is_set, 'PHAS')


def check_mod(message):
    profile = configparser.ConfigParser()
    profile.read(check_profile(message))

    return profile.get("Data", "module")


def set_mod(message, is_set):
    """
            Sets phase to entered value
            :param message:
            :param is_set: Change to
                """
    profile = configparser.ConfigParser()
    file_path = check_profile(message)

    profile.read(file_path)
    profile.set("Data", "module", is_set)

    with open(file_path, "w") as config_file:
        profile.write(config_file)

    logger('Module changed to ' + is_set, 'MODL')
