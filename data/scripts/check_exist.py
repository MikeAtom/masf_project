from os import path, mkdir


def check(folder, create=False):
    if path.exists(folder):
        exist = True
    else:
        exist = False

    if create and not exist:
        mkdir(folder)
    return exist
