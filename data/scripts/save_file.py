from data.handlers.apihand import bot

def save_file(message, file_path, file_name, file_type):
    path = file_path + '/' + file_name + '.' + file_type
    new_file = open(path, 'wb')
    new_file.write(bot.download_file(bot.get_file(message.document.file_id).file_path))
    return path