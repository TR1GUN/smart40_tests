# Отдельный файл для запуска - и отладки
from working_directory.Template.Template_Setup import Setup
import time

# функция для ручного запуска имеющегося JSON
def Setup_(JSON , API , Type_Connect):
    """
    Функция для ручного запуска имеющегося JSON

    :param JSON: Наш JSON что мы отправляем
    :return: JSON что пришел ответом
    """
    time_start = time.time()
    print(Type_Connect)
    JSON_Setup = Setup(JSON=JSON, API=API, type_connect=Type_Connect)
    # Получаем Ответ
    answer_JSON = JSON_Setup.answer_JSON

    # Получаем время
    time_finis = time.time()

    print('JSON Обрабабатывался:', time_finis - time_start)

    return answer_JSON


JSON = '{"job":"ElConfig","meters":[{"address":"192.168.202.146:7777","deviceidx":5,"iface":"Ethernet","password":"stone","password2":"island","type":94,"uart":"9600,8n1"},{"address":"141227285","deviceidx":6,"iface":"Hub","password":"373737373737","password2":"373737373737","type":5,"uart":"9600,8n1"}],"time":[{"end":2147483647,"start":1614860335}]}'

API = 'uspd-meter_daemon'
# type_connect = 'virtualbox'
a = Setup_(JSON=JSON , API='meterdev' , Type_Connect='virtualbox')

print(a)