config_path = 'config.ini'
modules_path = './modules'
temp_path = './files/temp'


def initial():
    """
            Bot initialization
            """
    try:
        global logger_script
        import data.scripts.logger as logger_script
    except:
        pass
    global stage

    logger('Initialization started', 'INIT')

    config_setup()
    module_setup()
    apihand_setup()

    logger('Initialization completed', 'POST')

    apihand.post()


def config_setup():
    """
        Sets global values
            """
    logger('Config initializing', 'INIT')

    try:
        import data.handlers.confhand as confhand
        data = confhand.config(config_path)
        global token, master
        token = data["token"]
        master = data["master"]
    except:
        exit('Config handler is corrupt or non-existent!')

    if not token == '':
        logger('Token passed successfully', 'INIT')
        pass
    else:
        logger('Token failed', 'EXPT')
        exit('Invalid token. Enter API Token in ' + config_path + '!')

    if not master == '':
        logger('Master ID passed successfully', 'INIT')
        pass
    else:
        logger('No Master ID, bot will be public!', 'WARN')

    logger('Config initialized successfully ', 'INIT')


def apihand_setup():
    try:
        global apihand
        import data.handlers.apihand as apihand

        apihand.init(token, temp_path)

        logger('API handler loaded successfully', 'INIT')
    except:
        exit('API handler is corrupt or non-existent!')


def module_setup():
    loaded = False
    try:
        global modhand, modules
        import data.handlers.modhand as modhand

        loaded = True

        logger('Modules handler loaded successfully', 'INIT')
    except:
        modules = [[], []]  # dict{mod_id: current internal id}, list[current internal ids]
        logger('Modules handler is corrupt or non-existent, no modules will be present', 'WARN')

    if loaded:
        modules = modhand.module_loader(modules_path)


def logger(message, stage=False, *args):
    try:
        import inspect
        from os import path
        frame = inspect.stack()[1]
        caller_name = str(
            (path.splitext(path.basename(frame[0].f_code.co_filename))[0]))  # file which called for logger
        logger_script.logger(caller_name, message, stage, *args)
    except:
        print('No logging script is present')

