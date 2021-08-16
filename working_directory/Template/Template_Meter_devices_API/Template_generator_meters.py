# Здесь опишем класс который будет генерировать нужные нам meters
from working_directory.Template.Template_Meter_devices_API import Template_list_job
from working_directory.sqlite import execute_command_to_read_return_dict
from working_directory.Template.Template_Meter_devices_API import Template_meters_settings
import random


class GenerateMeters:
    """
    Класс для генерации поля meter  в json запроса
    """

    meters = []
    meter_type = None

    # Генерируем ли рандомом
    __generate_random_meter_type = None
    # Какой интерфейс используем в первую очередь
    __iface = None
    # Служебные- Какой тип мы выбираем
    __job = None

    # Порт - Иногда нужен
    __port = None

    # А вот тут важно - Настройки по умолчанию
    __default = False

    address = None

    def __init__(self,
                 job: str,
                 generate_random_meter_type: bool = False,
                 iface: str = 'Ethernet',
                 port: str = '192.168.202.167:777',
                 default: bool = False,
                 address: str = "134256651"):
        """
        Конструктор массива meters

        :param job: сюда пихаем наш элемент что запрашиваем
        :param generate_random_meter_type: Генерируем ли рандомом тип счетчика
        :param iface: сюда спускаем интерфейс
        :param port: Сюда пихаем наш порт или ip адресс:порт
        :param default: Булевый параметр - Настройки по умолчанию. Игнорируется настройки порта
        """

        # Создаем пустой массив
        self.meters = []
        self.meter_type = None

        # Переопределяем
        self.__generate_random_meter_type = generate_random_meter_type
        self.__iface = iface
        self.__job = job
        self.__port = port
        self.__default = default
        self.address = address

        self.meters = self.__generate_meter_settings()

    def __generate_meter_settings(self):

        # формируем наш settings
        settings = {}

        # тип устройства
        settings['type'] = self.__generate_meter_type()

        # А теперь опреденляем пароли:
        settings["password"] = Template_meters_settings.password_dict[str(settings['type'])]
        # Если у нас идет запись - то добавляем второй пароль

        Set_job_list = Template_list_job.SetRelay_list + Template_list_job.SyncTime_list + Template_list_job.SetTime_list
        if self.__job in Set_job_list:
            settings["password2"] = Template_meters_settings.password2_dict[str(settings['type'])]

        # Ставим заглушку
        settings['deviceidx'] = 0
        settings['deviceidx'] = 0

        # Теперь определяем интерфейс, с упаковыванием это в meters

        meters = self.__generate_meters_iface(settings=settings)

        return meters

    def __generate_meters_iface(self, settings: dict):

        # А вот тут жаришка.
        meters = []
        # Получаем интерфейс
        iface = self.__iface
        # Здесь Делаем адресс
        try:
            # Итак - если настройки по умолчанию:
            if self.__default:
                # По интерфейсу определяем адрес
                address = Template_meters_settings.address_dict[iface]
            # Иначе - Ставим сюда порт что задавали
            else:
                address = self.__port


        except:
            address = 'Адресса нет'
        # Получаем uart
        uart = Template_meters_settings.uart_tag

        # А теперь собираем этот зоопарк
        # в зависимости от того что это за интерфейс генерируем два или несколько элементов
        # Если у нас канал обмена это изя р нет
        if iface == Template_meters_settings.ifaces_list[0]:
            settings_first = {}
            settings_two = settings

            # Собираем первый элемент

            settings_first["type"] = self.__generate_hub()
            # settings_first["type"] = settings["type"]
            settings_first["iface"] = iface
            settings_first["address"] = address
            # Собираем второй элемент

            # settings_two["type"] = self.__generate_hub()
            settings_two["iface"] = "Hub"
            # settings_two["address"] = '141227285'
            # settings_two["address"] = Template_meters_settings.address

            # Поставим адрес который спускаем сверху
            if self.address is None :
                settings_two["address"] = Template_meters_settings.address
            else:
                settings_two["address"] = self.address
            settings_two["uart"] = uart

            # Упаковываем это
            meters.append(settings_first)
            meters.append(settings_two)

        # Иначе - изготавляем параметры для последовательного порта
        else:
            settings["iface"] = iface
            settings["address"] = address
            settings["uart"] = uart

            meters.append(settings)

        return meters

    def __generate_hub(self):
        # здесь надо сгенерировать хаб

        # Но генерировать мы его не будем
        hub = 94
        return hub

    def __generate_meter_type(self):

        """ Генератор прибора учета.
        В зависимости от generate_random_meter_type два сценария -
        Если True -
                    Определяем рандомно прибор учета
        Если False -
                    Определяем фиксированный прибор учета
        """
        # Если у нас generate_random_meter_type в неправде - то добавляем фиксированный счетчик
        if not self.__generate_random_meter_type:
            # Пишем счетчик Энергомера
            meter_type = 5
        # Иначе - генерируем рандомно
        else:
            # для начала селектим все возможные варианты счетчиков
            command = ' SELECT Id FROM MeterTypes '
            meters = execute_command_to_read_return_dict(command)
            # Рандомно выбираем его -
            meter_type = meters[random.randint(0, len(meters))]['Id']

        return meter_type
