import configparser
from data.scripts.check_exist import check


def config(file_path):
    """
        """
    global config_file
    config_file = file_path

    if check(config_file):
        output = read_config()
    else:
        output = create_config()

    return output


def create_config():
    global config_file

    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)

    config_parser.add_section("Bot")
    config_parser.set("Bot", "token", "")
    config_parser.set("Bot", "master", "")

    with open(config_file, "w") as config_file:
        config_parser.write(config_file)
    return False


def read_config():
    global config_file

    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)

    config_values = dict(config_parser.items("Bot"))
    return config_values
