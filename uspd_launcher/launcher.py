# итак - Этот файл очень важный -
# ОН НУЖЕН ДЛЯ ЗАПУСКА ТЕСТОВ ВНУТРИ самой машины
#
# ПРИ установки тестов , его надо обязательно скопировать во внутрь виртуальной машины/докер контейнера
# через этот файл идет все взаимоденйствие

# Перед запуском тестов , надо обязательно прописать путь в настройках, где находится данный скрипт - ето важно !

import subprocess

def send_to_component(API, JSON):
    API_dict = \
        {
            'meterdev': '/etc/opt/uspd/meterdev/meterdev',
            'meter_db_data_api': '/etc/opt/uspd/meter_db_data_api/meter_db_data_api',
            'meter_db_settings': '/etc/opt/uspd/meter_db_settings/meter_db_settings'
        }
    API = API_dict[API]
    process = subprocess.Popen(API, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    process.stdin.write(str.encode(JSON))
    print('\n\n', str.encode(JSON), '\n\n')

    data, error = process.communicate()

    print(data)

import sys

API = sys.argv[1]

print('API', API)
JSON = sys.argv[2]
print('JSON', JSON)
send_to_component(API, JSON)