from fnmatch import filter
from os import listdir
from pathlib import Path

def dir_search(path, mask):
    items_available = []
    for files in filter(listdir(path), mask):
        items_available.append(Path(files).stem)
    return items_available