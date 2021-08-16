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
    # # Если у нас необходим виртуальный счетчик , то врубаем его отдельным потоком
    # threading_meter = False
    # if API in ['uspd-meter_daemon','meterdev' ] :
    #     threading_meter = True
    #     server = threading.Thread(target=EmulatorMeter)
    #     server.start()

    time_start = time.time()
    print(Type_Connect)
    JSON_Setup = Setup(JSON=JSON, API=API, type_connect=Type_Connect)
    # Получаем Ответ
    answer_JSON = JSON_Setup.answer_JSON

    # Получаем время
    time_finis = time.time()

    print('JSON Обрабабатывался:', time_finis - time_start)

    # if threading_meter:
    #     server.join()

    return answer_JSON


JSON ='{"job": "ElConfig", "time": {"start": 1627329600, "end": 1627333200}, "meters": [{"type": 94, "iface": "Ethernet", "address": "192.168.205.6:2002"}, {"type": 5, "password": "373737373737", "deviceidx": 1, "iface": "Hub", "address": "141227285", "uart": "9600,8n1"}]}'

API = 'meterdev'
# type_connect = 'virtualbox'
a = Setup_(JSON=JSON , API='meterdev' , Type_Connect='ssh')

print(a)