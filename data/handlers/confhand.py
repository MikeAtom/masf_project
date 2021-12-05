import configparser
from data.scripts.check_exist import check

def config(file_path):
    """
        """
    if check(file_path):
        output = read_config(file_path)
    else:
        output = create_config(file_path)

    return output


def create_config(file_path):
    config_parser = configparser.ConfigParser()
    config_parser.read(file_path)

    config_parser.add_section("Bot")
    config_parser.set("Bot", "token", "")
    config_parser.set("Bot", "master", "")

    with open(file_path, "w") as config_file:
        config_parser.write(config_file)
    return False


def read_config(file_path):
    config_parser = configparser.ConfigParser()
    config_parser.read(file_path)

    config_values = dict(config_parser.items("Bot"))
    return config_values
