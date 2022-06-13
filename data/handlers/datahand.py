import configparser
from data.scripts.check_exist import check

def create_data(file_path, sections):
    if not check(file_path + '.item'):
        data = configparser.ConfigParser()

        data.add_section("Info")
        for section in sections:
            data.set('Info', section, "")

        with open(file_path + '.item', "w") as file:
            data.write(file)


def read_data(file_path, section):
    data = configparser.ConfigParser()
    data.read(file_path + '.item', encoding="utf8")

    return data.get("Info", section)


def write_data(file_path, section, value):
    data = configparser.ConfigParser()

    data.read(file_path + '.item', encoding="utf8")
    data.set("Info", section, value)

    with open(file_path + '.item', "w", encoding='utf8', errors='ignore') as file:
        data.write(file)