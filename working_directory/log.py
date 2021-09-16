# Итак , здесь расположим нашу функцию логирования
from time import time
import write_file
import json

def log(API_name: str, Error: list, JSON: dict, answer_JSON: dict , JSON_normal = None):
    """
    ФУнкция Логирования - как показывает практика - Ошибки лучше логировать , а не выводить принтом

    :param API_name:  Сюда пихать название апи - НУЖНО для названия лога
    :param Error: Сам сборщик ошибок
    :param JSON: JSON что отправляем
    :param answer_JSON: JSON что получили
    :return: Получаем имя логированного файла

    """
    fille_name = 'Error' + API_name + ' log JSON in ' + str(int(time())) + '.txt'

    if JSON_normal is None:
        JSON = json.dumps(JSON)
        answer_JSON = json.dumps(answer_JSON)

        writen_text = '\n JSON: \n\n' + str(JSON) + '\n\nОтвет на JSON: \n\n ' + str(answer_JSON) + \
                      '\n\n\nРезультат сравнения: \n\n ' + str(Error) + \
                      str('\n\n-------------------------------------------------------\n')
    else:
        JSON = json.dumps(JSON)
        answer_JSON = json.dumps(answer_JSON)
        JSON_normal = json.dumps(JSON_normal)

        writen_text = '\n JSON: \n\n' + str(JSON) + '\n\nОтвет на JSON: \n\n ' + str(answer_JSON) + \
                      '\n\n Предпологаемый ответ на JSON: \n\n' + str(JSON_normal) + \
                      '\n\n\nРезультат сравнения: \n\n ' + str(Error) + \
                      str('\n\n-------------------------------------------------------\n')

    writen_text.encode('utf-8')
    write_file.write_file(file_name=fille_name, writen_text=writen_text)

    result = [{'error': 'Ошибка при сравнении. Залогировано в файле', 'file': fille_name}]

    return result

