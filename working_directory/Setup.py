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


JSON = '{"method": "post", "measures": [{"measure": "ElMomentQuality", "devices": [{"id": 1, "vals": [{"ts": 0, "tags": [{"tag": "UA", "val": 92.49}, {"tag": "UB", "val": -3.0791}, {"tag": "UC", "val": -42.8529}, {"tag": "IA", "val": -38.8463}, {"tag": "IB", "val": 85.7441}, {"tag": "IC", "val": 27.1104}, {"tag": "PS", "val": -59.3813}, {"tag": "PA", "val": -31.1666}, {"tag": "PB", "val": 66.8526}, {"tag": "PC", "val": 57.1044}, {"tag": "QS", "val": 71.4915}, {"tag": "QA", "val": 7.8683}, {"tag": "QB", "val": -52.3546}, {"tag": "QC", "val": 3.1176}, {"tag": "SS", "val": -76.1389}, {"tag": "SA", "val": null}, {"tag": "SB", "val": null}, {"tag": "SC", "val": null}, {"tag": "AngAB", "val": 86.7864}, {"tag": "AngBC", "val": 19.6697}, {"tag": "AngAC", "val": 82.0702}, {"tag": "kPS", "val": 52.3005}, {"tag": "kPA", "val": -98.3878}, {"tag": "kPB", "val": -50.6393}, {"tag": "kPC", "val": -11.4}, {"tag": "Freq", "val": 34.59}]}]}]}]}'

API = 'uspd-meter_daemon'
# type_connect = 'virtualbox'
a = Setup_(JSON=JSON , API='meterdev' , Type_Connect='virtualbox')

print(a)