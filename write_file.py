import os


def write_file_JSON(file_name: str, writen_text):
    '''
    Функция для записи в файл.
    Она очень важна

    :param file_name: Имя файла
    :param writen_text: Текст что надо записать
    :return:
    '''
    path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
    path_log = path + "/log/"
    if not os.path.exists(path_log): os.makedirs(path_log)
    a = open(path + "/" + str(file_name), 'a')
    a.write(writen_text)
    a.close()


def write_file(file_name: str, writen_text):
    '''
    Функция для записи в файл.
    Она очень важна

    :param file_name: Имя файла
    :param writen_text: Текст что надо записать
    :return:
    '''
    path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
    path_log = path + "/log/"
    if not os.path.exists(path_log): os.makedirs(path_log)
    a = open(path_log + str(file_name), 'w')
    a.write(writen_text)
    a.close()


def write_file_JSON_on_Emulator(writen_text):
    '''
    Функция для записи в файл.
    Она очень важна

    :param file_name: Имя файла
    :param writen_text: Текст что надо записать
    :return:
    '''
    from Emulator.ParserXML import path
    path_values = path + '/' + 'values.json'

    a = open(path_values, 'w')
    a.write(writen_text)
    a.close()


def write_log_file(file_name: str, writen_text, folder: str = ''):
    '''
    Функция для записи в файл.
    Она очень важна

    :param folder: ДОП дирректория
    :param file_name: Имя файла
    :param writen_text: Текст что надо записать
    :return: Возвращает имя файла
    '''
    path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
    path_log = path + "/log/" + folder
    if not os.path.exists(path_log): os.makedirs(path_log)
    a = open(path_log + str(file_name), 'w')
    a.write(writen_text)
    a.close()

    return path_log + str(file_name)


def append_write_log_file(file_name: str, writen_text):
    '''
    Функция для записи в файл.
    Она очень важна

    :param file_name: Имя файла
    :param writen_text: Текст что надо записать
    :return:
    '''
    a = open(file_name, 'a')
    a.write(writen_text)
    a.close()
