# Данный файл запускает тесты что находятся в test_MeterTable_db_API.py через pytest

# Запускаем тесты  в нужном файле с полным логированием и сохранением отчета в xml
command = 'python -m pytest test_Meter_db_settings_API.py -vv --junitxml=result_test_meter_db_api.xml'

command = 'python -m pytest test_Meter_db_data_API.py -vv --html=report.html '


command = 'python -m pytest test_Meter_db_data_API.py -vv --html=report.html '
import os

os.system(command)

'python -m pytest test_Meter_db_data_API.py -vv --junitxml=result_test_meter_db_api.xml'

'python -m pytest test_Meter_db_data_API.py -vv --html=report.html '

'python -m pytest  -vv --html=report.html '


'python -m pytest test_Meter_devices_API.py -vv --html=report.html '



'python -m pytest test_Meter_devices_API.py --type_connect=virtualbox -vv --html=report.html '

'python -m pytest test_Meter_db_data_API.py  --type_connect=virtualbox -vv --html=report.html'

'python -m pytest test_Castrom_set.py  --type_connect=virtualbox -vv --html=report.html'
