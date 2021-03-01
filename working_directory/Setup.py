# Отдельный файл для запуска - и отладки
from working_directory.Template.Template_Setup import Setup
import time

# функция для ручного запуска имеющегося JSON
def Setup(JSON , API , Type_Connect):
    """
    Функция для ручного запуска имеющегося JSON

    :param JSON: Наш JSON что мы отправляем
    :return: JSON что пришел ответом
    """
    time_start = time.time()
    JSON_Setup = Setup(JSON=JSON, API=API, type_connect=Type_Connect)
    # Получаем Ответ
    answer_JSON = JSON_Setup.answer_JSON

    # Получаем время
    time_finis = time.time()

    print('JSON Обрабабатывался:', time_finis - time_start)

    return answer_JSON
