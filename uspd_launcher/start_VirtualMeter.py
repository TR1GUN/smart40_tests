# Здесь Расположим Отдельную Функцию запуска ВИРТУАЛЬНОГО СЧЕТЧИКА - ЭТО ВАЖНО

def EmulatorMeter(port: int = 7777):
    """В этом методе подымаем локальный серевер с нашим виртуальным счетчиком"""
    from working_directory.Template.Template_Meter_devices_API.Template_socket_in_meters import SocketMeters
    Emulator = SocketMeters(conect_port=port)

    # После удаляем обьект
    del Emulator