from datetime import datetime
from data.scripts.check_exist import check

def logger(callername, message, stage):
    """
            Logs current action
            :param message: Action to log
            :param stage: Current stage
                """
    folder = 'logs'
    check(folder, True)
    today = datetime.now()

    if stage:
        stage_string = '[' + stage + '] '
    else:
        stage_string = ' '



    log_string = '[' + today.strftime("%d/%m/%y,%H:%M:%S") + ']' + '[' + callername.upper() + ']' + stage_string + message

    print(log_string)

    with open(folder + '/' + today.strftime("%y-%m-%d") + ".log", 'a', encoding="utf-8") as logfile:
        logfile.write(log_string + "\n")
