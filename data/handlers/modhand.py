from importlib import import_module
from fnmatch import filter
from os import listdir
from pathlib import Path
from data.core import logger
from data.scripts.check_exist import check


def module_import(module):
    return import_module('modules.' + module, package=module)


def module_loader(folder):
    modules_enabled = []
    modules_ids = {}
    i = 0
    if check(folder):
        for module in module_search(folder):
            logger('Trying to enable module ' + '"' + module + '"...', 'INIT')
            try:
                module = module_import(module)
                logger(module.name + ' by ' + module.author + ' is loaded', 'INIT')
                modules_enabled.append(module)
                modules_ids[module.mod_id] = i
                i += 1
            except:
                logger('Failed!', 'WARN')
    modules = [modules_ids, modules_enabled]
    return modules


def module_search(path):
    modules_available = []
    for files in filter(listdir(path), '*.py'):
        modules_available.append(Path(files).stem)
    return modules_available
