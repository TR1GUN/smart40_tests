# Здесь расположим класс который будет записывать нужные данные в MeterTable

from working_directory.Template.Template_MeterTable_db_API.Template_generator_settings_MeterTable import \
    GeneratorForSettingsMeterTable
from working_directory import sqlite
from working_directory.Template.Template_Meter_devices_API.Template_meters_settings import password2_dict, \
    password_dict, address_dict, ifaces_list, uart_list, Meter_Types_Hub, uart_tag


# ---------------------------------------------------------------------------------------------------------------------
#                                         КЛАСС ЗАПИСИ ОДНОЙ СТРОКИ В САМУ ТАБЛИЦУ
# ---------------------------------------------------------------------------------------------------------------------

class RecordingLineMeterTable:
    """
    Итак - Этот класс нужен для записи КОРЕКТНЫХ значений для METERTABLE - Это важно.

    ДЕЛАЕТ ТОЛЬКО ОДНУ ЗАПИСЬ
    """
    Interface: dict = {'Id': '0', 'Name': 'Interface'}
    MeterTypes: dict = {'Id': '0', 'Type': 'Meter'}
    MeterId = 0

    def __init__(self, ParentId: int = 0,
                 Addres: str = 'addres',
                 Password1: str = 'password_read',
                 Password2: str = 'password_write',
                 Interface: dict = None,
                 MeterTypes: dict = None,
                 InterfaceConfig=None
                 ):

        if MeterTypes is None:
            MeterTypes = self.MeterTypes
        if Interface is None:
            Interface = self.Interface

        # Записываем
        self.__recording_line_in_meter_table(
            ParentId=ParentId,
            Addres=Addres,
            Password1=Password1,
            Password2=Password2,
            Interface=Interface,
            MeterTypes=MeterTypes,
            InterfaceConfig=InterfaceConfig
        )

    def __recording_line_in_meter_table(
            self,
            ParentId: int = 0,
            Addres: str = 'addres',
            Password1: str = 'password_read',
            Password2: str = 'password_write',
            Interface: dict = None,
            MeterTypes: dict = None,
            InterfaceConfig=None
    ):

        """
        Так - Данная функция записывает ОДНУ строку в METERTABLE с указаными параметрами
        :param ParentId:
        :param Addres:
        :param Password1:
        :param Password2:
        :param Interface:
        :param MeterTypes:
        :return:
        """
        # вызываем генератор
        generate_meter_setting = GeneratorForSettingsMeterTable(
            count_settings=1,
            pId=ParentId,
            passRd=Password1,
            passWr=Password2,
            addr=Addres,
            Interface=Interface,
            MeterTypes=MeterTypes,
            InterfaceConfig=InterfaceConfig
        )
        # Теперь записываем наши данные
        sqlite.recording_MeterTable(generate_meter_setting.get_tuple())
        # Возвращаем наш MeterId
        self.MeterId = generate_meter_setting.MeterId


# ---------------------------------------------------------------------------------------------------------------------
#                                 КЛАСС ЗАПИСИ В ЗАВИСИМОСТИ ОТ ПАРАМЕТРОВ
# ---------------------------------------------------------------------------------------------------------------------

class RecordingParentTreeMeterTable:
    """Даннынй класс добавляет нужное дерево зависимостей в MeterTAble
        По умолчанию - связка виртуального счетчика - ХАБ ИЗЯрнета - СЧЕТЧИК"""
    id = []
    type_connect = 'Ethernet'

    # НАСТРОЙКИ ДЛЯ ХАБА
    type_connect_hub = 'Hub'
    type_meter = 'SE303'
    address_meter = ''
    InterfaceConfig = ''
    MeterId = 0
    count_tree = 0
    adress = None
    Meter_MeterId = None

    def __init__(self,
                 count_tree: int = 2,
                 type_connect: str = 'Ethernet',
                 type_meter: str = 'SE303',
                 address_meter: str = "141227285",
                 adress: str = "192.168.202.146:7777",
                 InterfaceConfig: str = uart_tag):

        self.count_tree = count_tree
        # Переопределяем Поля
        self.InterfaceConfig = InterfaceConfig
        self.address_meter = address_meter
        self.type_connect = type_connect
        self.type_meter = type_meter
        self.adress = adress

        # Теперь Определяем тип счетика
        self.__define_type_Meter()
        # Теперь определяем тип подключения
        self.__define_type_connect()

        # Теперь строим наше дерево зависимостей
        self.__record_tree_in_MeterTable()

    def __record_tree_in_MeterTable(self):

        """"Эта функция НУЖНА чтоб построить дерево зависимостей """
        i = self.count_tree
        if i > 1:
            # ПУНКТ ПЕРВЫЙ : Ставим ХАБ
            self.__record_recording_hub_in_MeterTable()

            i = i - 1
            # ПУНКТ ВТОРОЙ - ДОБАВЛЯЕМ ПРОМЕЖУТОЧНЫЕ ЗАПИСИ

            while i > 1:
                self.__record_recording_parent_tree_in_MeterTable()
                i = i - 1
            # ПУНКТ Третий - Добавляем САМ СЧЕТЧИК
            self.__record_recording_meter_in_MeterTable(iface=self.type_connect_meter_dict)
        else:
            # Иначе Добавляем ТОЛЬКО САМ СЧЕТЧИК
            self.__record_recording_meter_in_MeterTable(iface=self.type_connect_meter_dict)

    def __record_recording_meter_in_MeterTable(self, iface):
        """Здесь делаем запись нашего счетчика - Он является верхушкой дерева зависимостей"""

        # Вызываем запись - возвращаем значение meterid для постороения зависимостей

        Record_Meter = RecordingLineMeterTable(ParentId=self.MeterId,
                                               Addres=self.address_meter,
                                               Password1=password_dict[str(self.MeterTypes_Meter['Id'])],
                                               Password2=password2_dict[str(self.MeterTypes_Meter['Id'])],
                                               Interface=iface,
                                               MeterTypes=self.MeterTypes_Meter,
                                               InterfaceConfig=self.InterfaceConfig)

        # Возвращаем значение
        self.MeterId = Record_Meter.MeterId
        self.Meter_MeterId = Record_Meter.MeterId

    def __record_recording_hub_in_MeterTable(self):
        """Здесь делаем ЗАПИСЬ ПЕРВИЧНОГО ХАБА!!!"""

        # Вызываем запись - возвращаем значение meterid для постороения зависимостей
        Record_Meter = RecordingLineMeterTable(ParentId=self.MeterId,
                                               Addres=self.adress,
                                               Password1='Meter be away',
                                               Password2='Meter be away',
                                               Interface=self.type_connect_hub_dict,
                                               MeterTypes=self.MeterTypes_Hub,
                                               InterfaceConfig=self.InterfaceConfig)

        # Возвращаем значение
        self.MeterId = Record_Meter.MeterId

    def __record_recording_parent_tree_in_MeterTable(self):
        """здесь очень важно - Данная функция строит дерево зависимостей из промежуточных хабов"""
        # Вызываем запись - возвращаем значение meterid для постороения зависимостей
        Record_Meter = RecordingLineMeterTable(ParentId=self.MeterId,
                                               Addres='1',
                                               Password1='stone',
                                               Password2='island',
                                               Interface=self.type_connect_meter_dict,
                                               MeterTypes=self.MeterTypes_Hub,
                                               InterfaceConfig=self.InterfaceConfig)

        # Возвращаем значение
        self.MeterId = Record_Meter.MeterId

    def __get_meter_types(self):
        """здесь ищем наш счетчик """

        MeterTypes = sqlite.readtable_return_dict(collum='Id , Type ', table_name='MeterTypes WHERE Type LIKE \'' + str(
            self.type_meter) + '\'')
        return MeterTypes[0]

    def __get_Interface_types(self, type):

        'Здесь ищем наши типы подключений'
        InterfaceTypes = sqlite.readtable_return_dict(collum='Id , Name ',
                                                      table_name='MeterIfaces WHERE Name =  \'' + str(
                                                          type) + '\'')
        # А теперь переопределяем
        return InterfaceTypes[0]

    def __define_type_connect(self):

        '''
        Здесь Определяем наш тип конекта к счетчику
        :return:
        '''

        # Итак - Если у нас канал ИЗЯРНЕТ или число элементов дерева подключения БОЛЬШЕ ЧЕМ 1 , то ставим - ХАБ

        if (self.type_connect == 'Ethernet') or (self.count_tree > 1):
            self.type_connect_meter_dict = self.__get_Interface_types(type=self.type_connect_hub)
            # А Теперь ставим конект на первичный хаб
            self.type_connect_hub_dict = self.__get_Interface_types(type=self.type_connect)
            # Чтоб не выстрелить себе в ногу - Если канал изярнет , и количество элементов дерева меньше 2 -
            # выставляим их на 2
            if self.count_tree < 2:
                self.count_tree = 2

        # Иначе - Ставим его
        else:
            self.type_connect_meter_dict = self.__get_Interface_types(type=self.type_connect)

    def __define_type_Meter(self):
        """
        Здесь определяем тип счетчика
        :return:
        """

        # ПУНКТ ПЕРВЫЙ -  ЗАБИРАЕМ тип счетчика
        self.MeterTypes_Meter = self.__get_meter_types()

        # Итак - Если у нас канал ИЗЯРНЕТ или число элементов дерева подключения БОЛЬШЕ ЧЕМ 1 , то ставим - ХАБ

        if (self.type_connect == 'Ethernet') or (self.count_tree > 1):
            self.MeterTypes_Hub = Meter_Types_Hub


# ---------------------------------------------------------------------------------------------------------------------
#                                 КЛАСС Генерации нужного количество записей в METER TABLE
# ---------------------------------------------------------------------------------------------------------------------
class GenerateRecordMeterTable:
    """Данный класс генерирует нужное количество записей в MeterTable"""

    MeterId_list = []
    DeviceIdx_list = []
    generate_count = 1
    count_tree = None
    type_connect = None
    type_meter = None
    address_meter = None
    adress = None
    InterfaceConfig = None

    def __init__(self,
                 # Количество добавляемых записей
                 generate_count: int = 1,
                 # Количество элементов в дереве подключения
                 count_tree: int = 2,
                 # тип конекта
                 type_connect: str = 'Ethernet',
                 # Имя счетчика - Берется из БД
                 type_meter: str = 'SE303',
                 # Серийник нашего счетчика
                 address_meter: str = "141227285",
                 # Первичный Адресс счетчика\Хаба
                 adress: str = "192.168.202.146:7777",
                 # uart_tag
                 InterfaceConfig: str = uart_tag):

        # переопределяем тэги
        self.generate_count = generate_count
        self.count_tree = count_tree
        self.type_connect = type_connect
        self.type_meter = type_meter
        self.address_meter = address_meter
        self.adress = adress
        self.InterfaceConfig = InterfaceConfig

        # Запускаем Генератор
        self.__generate_record_metertable()



        self.DeviceIdx_list = self.get_select_deviceidx()

    def __generate_record_metertable(self):

        for i in range(self.generate_count):
            # Генерируем нужное количество записей
            Record = RecordingParentTreeMeterTable(
                count_tree=self.count_tree,
                type_connect=self.type_connect,
                type_meter=self.type_meter,
                address_meter=self.address_meter,
                adress=self.adress,
                InterfaceConfig=self.InterfaceConfig
            )


            # Итак - Если мы добавили счетчик и он не пустота - Добавляем в массив
            if Record.Meter_MeterId is not None:
                self.MeterId_list = self.MeterId_list + [Record.Meter_MeterId]

    def get_select_deviceidx(self):
        '''
        А теперь селектим все внутрение айдишники и добавляем их в список
        :return:
        '''

        command_select_MeterId_list = ''
        for i in range(len(self.MeterId_list)):
            command_select_MeterId_list = command_select_MeterId_list + str(self.MeterId_list[i]) + ' , '

        command_select_MeterId_list = command_select_MeterId_list[:-2]

        command = 'SELECT DeviceIdx FROM MeterTable WHERE MeterId in ' + '( ' + command_select_MeterId_list + ' ) '
        # Селектим их через нашу БД
        result_list = sqlite.execute_command_to_read_return_dict(command=command)
        result = []
        for i in result_list:
            result.append(i['DeviceIdx'])
        return result
