# Здесь пускай валяются общие конфиги


# Конфиг для определеняи пути апих.

path_to_API = \
    {
'meterdev' : '/etc/opt/uspd/meterdev/meterdev',
# 'meter_db_data_api':'etc/opt/uspd/meter_db_data_api/meter_db_data_api',
'meter_db_data_api':'/etc/opt/uspd/meter_db_data_api/meter_db_data_api',
'meter_db_settings':'etc/opt/uspd/meter_db_settings_api/meter_db_settings_api',
'uspd-meter_daemon':'mosquitto_pub -t \'/meterdaemon/\' --stdin-line'
    }
