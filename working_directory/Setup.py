# Отдельный файл для запуска - и отладки
from working_directory.Template.Template_Setup import Setup
from uspd_launcher.start_VirtualMeter import EmulatorMeter
import time
import threading

# функция для ручного запуска имеющегося JSON
def Setup_(JSON , API , Type_Connect):
    """
    Функция для ручного запуска имеющегося JSON

    :param JSON: Наш JSON что мы отправляем
    :return: JSON что пришел ответом
    """
    # Если у нас необходим виртуальный счетчик , то врубаем его отдельным потоком
    threading_meter = False
    if API in ['uspd-meter_daemon','meterdev' ] :
        threading_meter = True
        server = threading.Thread(target=EmulatorMeter)
        server.start()

    time_start = time.time()
    print(Type_Connect)
    JSON_Setup = Setup(JSON=JSON, API=API, type_connect=Type_Connect)
    # Получаем Ответ
    answer_JSON = JSON_Setup.answer_JSON

    # Получаем время
    time_finis = time.time()

    print('JSON Обрабабатывался:', time_finis - time_start)

    if threading_meter:
        server.join()

    return answer_JSON


JSON = '{"method": "post", "measures": [{"measure": "ElConfig", "devices": [{"id": 1, "vals": [{"ts": 1555555555, "tags": [{"tag": "serial", "val": "1224915766"}, {"tag": "model", "val": "Test model Your ad could be here"}, {"tag": "cArrays", "val": 56}, {"tag": "isDst", "val": 1}, {"tag": "isClock", "val": 1}, {"tag": "isTrf", "val": 1}, {"tag": "isAm", "val": 1}, {"tag": "isRm", "val": 1}, {"tag": "isRp", "val": 1}, {"tag": "kI", "val": 51.0}, {"tag": "kU", "val": 23.0}, {"tag": "const", "val": -44.3798}]}]}]}]}'

API = 'uspd-meter_daemon'
# type_connect = 'virtualbox'
a = Setup_(JSON=JSON , API='meter_db_data_api' , Type_Connect='ssh')

print(a)