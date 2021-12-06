from data.core import logger
from data.scripts.check_exist import check
import configparser

folder = './data/users'
check(folder, True)


def create_profile(user_id):
    profile = configparser.ConfigParser()

    file_path = folder + '/' + str(user_id) + '.usr'

    profile.add_section("Conductor")
    profile.set('Conductor', "phase", "")
    profile.set('Conductor', "module", "")

    with open(file_path, "w") as config_file:
        profile.write(config_file)


def check_profile(user_id):
    file_path = folder + '/' + str(user_id) + '.usr'
    if not check(file_path):
        create_profile(user_id)
    return file_path


def read_profile(user_id, section, value):
    profile = configparser.ConfigParser()
    profile.read(check_profile(user_id))

    return profile.get(section, value)


def write_profile(user_id, section, value, set_to):
    profile = configparser.ConfigParser()
    file_path = check_profile(user_id)

    profile.read(file_path)
    profile.set(section, value, set_to)

    with open(file_path, "w") as config_file:
        profile.write(config_file)

