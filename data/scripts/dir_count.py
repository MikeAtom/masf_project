import os

def dir_count(path):
    return len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])