from os import path, makedirs


def check(folder, create=False):
    if create and not path.exists(folder):
        makedirs(folder)
    return path.exists(folder)
