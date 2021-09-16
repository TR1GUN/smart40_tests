# Итак здесь расположим наш тест для демона опроса ПУ

from working_directory.Template.Template_Meter_db_data_API.Template_read_handler_table import \
    ReceivingDataAccordingToJSON
from working_directory.Template.Template_Meter_daemon.Template_select_data_base_was_recording import \
    DataBaseWasRecordingInFact

from working_directory.Template.Template_Meter_daemon.Template_CheckUp_for_MeterDaemon import CheckUP
from working_directory.Template.Template_Setup import Setup
from working_directory.log import log
from time import sleep
from working_directory.sqlite import deleteMeterTable
import threading
import time
from datetime import datetime


# -------------------------------------------------------------------------------------------------------------------
#                       Делаем основной класс - От которого будем наследоваться
#                                     В него внесем общие методы
# -------------------------------------------------------------------------------------------------------------------
class MeterDaemon:
    """
    Этот класс преднозначен для тестирования демона опроса ПУ
    """
    API = 'uspd-meter_daemon'
    type_connect = 'virtualbox'
    error = None
    port = 7777

    list_measure = []

    MeterId_list = []
    DeviceIdx_list = []
    count_ts_to_record = 0

    JSON = {}
    database_was_recording = []
    JSON_meterdata_deconstruct = []

    InterfaceConfig = "9600,8n1"
    # тип конекта
    iface = 'Ethernet'
    # Имя счетчика - Берется из БД
    type_meter = 'SE303'
    # Серийник нашего счетчика
    address_meter = "134256651"
    # Количество элементов в дереве зависимостей
    count_tree = 2
    # Адресс нашего счетчика - айпишник-порт
    address = '192.162.205.6:2002'

    def __init__(self, type_connect: str = 'virtualbox'):
        self.type_connect = type_connect

        # Вначале чтоб ничего не терять - РЕДАЧИМ ТАБЛИЦУ ЗАПИСИ
        self._rewrite_ArchInfo()

    # ----------------------- Метод для Запуска Нужного нам JSON ------------------------------------------------------

    def Setup(self):
        """
        Метод для запуска НАШЕГО JSON

        :param JSON:
        :return:
        """

        print('JSON', self.JSON)
        JSON_Setup = Setup(JSON=self.JSON, API=self.API, type_connect=self.type_connect)
        # Получаем Ответ
        answer_JSON = JSON_Setup.answer_JSON

    # -------------------------------   Логирование ОШИБКИ  -----------------------------------------
    def write_log(self, result):
        # Теперь если есть ошибки - логируем их
        if len(result) > 0:
            result = log(API_name='Meter Daemon -' + str(self.list_measure),
                         Error=result,
                         JSON=self.JSON,
                         answer_JSON={'То что записано записанно': self.database_was_recording},
                         JSON_normal={'ТО что должно было быть записанно': self.JSON_meterdata_deconstruct})

        return result

    # -----------------------------------------------------------------------------------------------
    # ----------------------- Редактор наших полей  ArchInfo Под нужное значение   -----------------------------------
    def _rewrite_ArchInfo(self):
        '''
        Редактор наших полей  ArchInfo Под нужное значение
        :return:
        '''

        from working_directory.Template.Template_Meter_daemon.Template_ReWrite_field_Records import ReWriteFieldRecords
        from working_directory.Template.Template_Meter_daemon.Daemon_settings import ArchInfo_settings
        for x in range(len(self.list_measure)):
            record = ReWriteFieldRecords(measure=self.list_measure[x],
                                         count_records=ArchInfo_settings.get(self.list_measure[x]))

    # ----------------------- Метод для определения входных данных ------------------------------------------
    def _Define_test_data(self, list_measure, count_ts_to_record, count_tree):
        """
        В ЭТОМ МЕТОДЕ ПЕРЕЗАПИСЫВАЕМ наши тестовые данные что нам дали  - ЭТО ВАЖНО
        :param list_measure: # Тип данных - Список
        :param count_ts_to_record: # количество записей в БД
        :param count_tree:  # Количество элементов в дереве подключения
        :return:
        """
        # Количество уже записанных в БД данных
        self.count_ts_to_record = count_ts_to_record
        # Тип данных
        self.list_measure = list_measure
        # Количество элементов в дереве подключения
        self.count_tree = count_tree

        # обнуляем все наши Глобальные переменные
        self.JSON_meterdata = {}
        self.JSON_meterdata_deconstruct = {}
        self.JSON_record = {}

        self.MeterId_list = []
        self.DeviceIdx_list = []
        self.database_was_recording = []
        self.JSON_Meter_Dev = {}
        self.JSON = {}

    # ---------------------------- Метод для Генерации Нужных данных в MeterTable   -------------------------------

    def __recording_data_in_metertable(self, MeterConfig):
        '''
        Здесь  Генерируем нашу запись в MeterTable
        Возвращаем список внутрених айдищников и внешних - Это важно
        '''

        from working_directory.Template.Template_MeterJSON.Template_Record_MeterTable import GenerateRecordMeterTable
        from copy import deepcopy

        # ТЕПЕРЬ -  ЗАПИСЫВАЕМ ПО ОДНОМУ

        for i in MeterConfig:
            # ПОЛУЧАЕМ АДРЕСС СЧЕТЧИКА

            Generate_Record_Meter = GenerateRecordMeterTable(
                generate_count=1,
                count_tree=i.get('count_tree'),
                type_connect=i.get('iface'),
                type_meter=i.get('type_meter'),
                address_meter=i.get('address_meter'),
                adress=i.get('address'),
                InterfaceConfig=i.get('InterfaceConfig')
            )

            self.MeterId_list = self.MeterId_list + deepcopy(Generate_Record_Meter.MeterId_list)
            self.DeviceIdx_list = self.DeviceIdx_list + deepcopy(Generate_Record_Meter.DeviceIdx_list)
            del Generate_Record_Meter

    def __checkup_MeterConfig(self, MeterConfig):

        """В этом методе проверяем коректность Конфигов"""
        MeterConfig_Template = \
            {
                # Количество элементов в дереве зависимостей
                'count_tree': self.count_tree,
                # тип конекта
                'iface': self.iface,
                # Имя счетчика - Берется из БД
                'type_meter': self.type_meter,
                # Серийник нашего счетчика
                'address_meter': self.address_meter,
                # Адресс нашего счетчика
                'address': self.address,
                # ИтнерфесКонфиг
                'InterfaceConfig': self.InterfaceConfig,

            }
        # сначала проверяем что подали кеоректные данные
        if (len(MeterConfig)) and (type(MeterConfig) is list) > 0:
            for i in MeterConfig:
                # Теперь смотрим что КАЖДЫЙ элемент
                if type(i) is dict:
                    # Теперь проверяем ключи
                    for key in MeterConfig_Template:
                        if i.get(key) is None:
                            i[key] = MeterConfig_Template[key]
                else:
                    i = MeterConfig_Template

        # Eсли подали не корректные данные - ставим шаблонные
        else:
            MeterConfig = [MeterConfig_Template]

        return MeterConfig

    # ----------------------- Метод для Генерации Топика задания - Это важно ------------------------------------------

    def _GenerateJSON(self):
        """
        Метод для Генерации Топика задания - Это важно
        """
        from working_directory.Template.Template_Meter_daemon.Template_generator_JSON_for_mosquitto import \
            GenerateForMosquittoJSON
        from working_directory.Connect.JSON_format_coding_decoding import code_JSON

        JSON_dict = GenerateForMosquittoJSON(Measure_type_list=self.list_measure,
                                             MeterId_list=self.MeterId_list).jobs

        # Теперь Это все конфертируем в JSON
        JSON = code_JSON(JSON_dict)
        return JSON

    def RealMeter(self,
                  MeterConfig=[],
                  list_measure: list = ['ElMonthEnergy']):
        """
        Здесь содержиться Тесты для УЖЕ заполненой БД - Заполняется только ОДИН таймштамп
        """
        # Чистим БД
        deleteMeterTable()
        sleep(2)

        # Чистим БД
        deleteMeterTable()
        sleep(2)

        # переопределяем тэги :
        # Тип данных
        self.list_measure = list_measure
        MeterConfig = self.__checkup_MeterConfig(MeterConfig)

        # Теперь Записываем нужноe количество записей в MeterTable
        self.__recording_data_in_metertable(MeterConfig=MeterConfig)

        # Теперь генерируем наш JSON
        self.JSON = self._GenerateJSON()

        # Теперь что делаем - Теперь запускаем наш сформированный JSON в в мененеджер задааний
        self.Setup()

        # # И селектим в БД ПОСЛЕ ЗАПИСИ
        # JSON_select = {"measures": list_measure,
        #                 "ids": self.MeterId_list,
        #                 "tags": [], "time": [], "flags": [],
        #                 "method": "get"}
        #
        # result = ReceivingDataAccordingToJSON(JSON=JSON_select,
        #                                       Select_all=True).get_result()
        return 0


#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                                                   ОДИН СЧЕТЧИК
# -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################


class MeterDaemonSingleMeter(MeterDaemon):
    '''
    Этот класс преднозначен для тестирования демона опроса ПУ
    '''
    API = 'uspd-meter_daemon'
    type_connect = 'virtualbox'
    error = None
    port = 7777

    MeterId_list = []
    DeviceIdx_list = []
    count_ts_to_record = 0

    database_was_recording = []

    JSON_meterdata_deconstruct = []

    JSON_meterdata = {}
    JSON_Meter_Dev = {}
    JSON = {}
    InterfaceConfig = "9600,8n1"

    # тип конекта
    iface = 'Ethernet'
    # Имя счетчика - Берется из БД
    type_meter = 'SE303'
    # Серийник нашего счетчика
    address_meter = "141227285"
    # address_meter = "134256651"
    # серийник
    serial = '009218054000006'

    # Количество сгенерированных штук
    generate_count = 1
    # Количество степеней зависимости
    count_tree = 2

    JSON_record = {}

    # ----------------------------------------------------------------------------------------------------------------
    #                                            Вспомомгательные методы
    # ----------------------------------------------------------------------------------------------------------------
    def _definition_count_timestamp(self):
        """
        Определение количества таймштампов
        :return:
        """
        from working_directory.Template.Template_Meter_daemon.Daemon_settings import ArchInfo_settings
        from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
        # ГЕНЕРИРУЕМ НУЖНОЕ КОЛИЧЕСТВО ЗАПИСЕЙ
        count_timesatamp = {}

        measure_moment_list = \
            [
                # Template_list_ArchTypes.ElectricConfig_ArchType_name_list[0],
                # Template_list_ArchTypes.PulseConfig_ArchType_name_list[0],
                # Template_list_ArchTypes.DigitalConfig_ArchType_name_list[0],
                Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list[0],
                Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list[0],
                Template_list_ArchTypes.PulseValues_ArchType_name_list[0],
                Template_list_ArchTypes.DigitalValues_ArchType_name_list[0],
            ]

        for i in range(len(self.list_measure)):
            # Но если у нас мгновенное время - ставим 1
            if self.list_measure[i] in measure_moment_list:
                count_timesatamp[i] = 1
            else:
                count_timesatamp[i] = ArchInfo_settings.get(self.list_measure[i])

        return count_timesatamp

    # ---------------------------- Получение Нашего локального айпишника ---------------------------------------------
    def __GetIPConfig(self):
        """
        Получаем наш Айпишник - нужен для того чтоб сделать сервер с виртуальным счетчиком

        :return:
        """

        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", self.port))
        socket_name = (s.getsockname()[0])
        s.close()
        return socket_name + ':' + str(self.port)

    # ---------------------------- Генерация данных для Виртуального счетчика ----------------------------------------

    # Пока сделаем это отдельным методом - Как там будет дальше - я не знаю
    def _generate_data_to_meter_dev(self, count_timestamp={}):
        """
        В Этом Методе генерируем наши JSON для MeterDEV
        :return:
        """
        from working_directory.Template.Template_Meter_daemon.Template_generator_data_for_Meter_Dev import \
            GenerateDataForMeterDev

        JSON_Meter_Dev = GenerateDataForMeterDev(measure_list=self.list_measure,
                                                 count_timestamp=count_timestamp).JSON_Meter_Dev

        return JSON_Meter_Dev

    # ---------------------------- Метод для записи НАШИХ ДАННЫХ в ВИРТУАЛЬНЫЙ СЧЕТЧИК -------------------------------
    def _recording_data_in_virtual_meter(self):
        """
        Записываем НАШИ ДАННЫЕ  директорию виртуального счетчика
        :return:
        """
        from working_directory.Template.Template_Meter_devices_API.Template_record_values_for_meter import \
            RecordFromEmulatorMeter
        Record_JSON = RecordFromEmulatorMeter(self.JSON_Meter_Dev)
        Record_JSON = Record_JSON.GET_Record()

        return Record_JSON

    # ---------------------------- Метод для ЗАПУСКА НАШЕГО ВИРТУАЛЬНОГО СЧЕТЧКА -------------------------------

    # Лучше всего запускать в  отдельном потоке - Надо будет как нить разобраться
    def __EmulatorMeter(self):
        """В этом методе подымаем локальный серевер с нашим виртуальным счетчиком"""
        from working_directory.Template.Template_Meter_devices_API.Template_socket_in_meters import SocketMeters

        # Получаем наш список типов данных данных
        self.Emulator = SocketMeters(
                                     conect_port=self.port,
                                     data=self.JSON_record,
                                     serial=str(self.serial) + '_' + str(self.port)
                                     )

        # После удаляем объект
        # del self.Emulator

    # ---------------------------- Метод для Генерации Нужных данных в MeterTable   -------------------------------
    def __recording_data_in_metertable(self):
        """
        Здесь  Генерируем нашу запись в MeterTable
        Возвращаем список внутрених айдищников и внешних - Это важно
        """

        from working_directory.Template.Template_MeterJSON.Template_Record_MeterTable import GenerateRecordMeterTable

        address = self.__GetIPConfig()

        Generate_Record_Meter = GenerateRecordMeterTable(
            generate_count=self.generate_count,
            count_tree=self.count_tree,
            type_connect=self.iface,
            type_meter=self.type_meter,
            address_meter=self.address_meter,
            adress=address,
            InterfaceConfig=self.InterfaceConfig
        )

        self.MeterId_list = Generate_Record_Meter.MeterId_list
        self.DeviceIdx_list = Generate_Record_Meter.DeviceIdx_list

    # ---------------------------- Метод для достраивания данных до уровня MeterData     ------------------------------

    def __generate_data_to_meter_data(self):
        """Метод который достраивает JSON до уровня meter data"""
        import copy

        # Достраиваем JSON до уровня meter data
        from working_directory.Template.Template_Meter_daemon.Template_assembly_normal_JSON_like_POST_meter_Data import \
            AssemblyDictLikeMeterData

        JSON_dict_meterdata = AssemblyDictLikeMeterData(self.JSON_Meter_Dev, self.DeviceIdx_list , serial=str(self.serial) + '_' + str(self.port)).JSON

        # Здесь возвращаем глубокую копию ради избежания перезаписи . ЛОЛ
        return copy.deepcopy(JSON_dict_meterdata)

    # ---------------- Метод для Деконструкции данных MeterData до уровня селекта из БД ------------------------------
    def _deconstruct_JSON_meterdata_to_data_base(self):
        """
        Итак - Здесь проводим ДЕКОНСТРУКЦИЮ JSON MeterData до уровня селекта в БД
        :return:
        """

        from working_directory.Template.Template_MeterJSON.Template_Deconstruct import DeconstructJSON

        JSON_for_compare_to_data_base = DeconstructJSON(JSON=self.JSON_meterdata).JSON_deconstruct

        return JSON_for_compare_to_data_base

    # -------------------------------------  Метод для ЗАПИСИ В БД ЗНАЧЕНИЙ  ------------------------------------------
    def _record_values_in_database(self):
        """
        ЗДЕСЬ ЗАПИСЫВАЕМ НАШИ ЗАПИСИ В БД
        :param JSON_deconstruct:
        :return:
        """

        from working_directory.Template.Template_Meter_db_data_API.Template_record_value_to_database import \
            RecordValueToDataBase
        # RecordValueToDataBase.SET_Serial(serial=str(self.serial) + '_' + str(self.port))
        RecordValueToDataBase(JSON_deconstruct=self.JSON_meterdata_deconstruct , serial=str(self.serial) + '_' + str(self.port))

    # ----------------------- Метод для Генерации Топика задания - Это важно ------------------------------------------

    def _GenerateJSON(self):
        """
        Метод для Генерации Топика задания - Это важно
        """
        from working_directory.Template.Template_Meter_daemon.Template_generator_JSON_for_mosquitto import \
            GenerateForMosquittoJSON
        from working_directory.Connect.JSON_format_coding_decoding import code_JSON

        JSON_dict = GenerateForMosquittoJSON(Measure_type_list=self.list_measure,
                                             MeterId_list=self.MeterId_list).jobs

        # Теперь Это все конфертируем в JSON
        JSON = code_JSON(JSON_dict)
        return JSON

    # ----------------------- Метод для определения входных данных ------------------------------------------
    def _Define_test_data(self, list_measure, count_ts_to_record, count_tree):
        """
        В ЭТОМ МЕТОДЕ ПЕРЕЗАПИСЫВАЕМ наши тестовые данные что нам дали  - ЭТО ВАЖНО
        :param list_measure: # Тип данных - Список
        :param count_ts_to_record: # количество записей в БД
        :param count_tree:  # Количество элементов в дереве подключения
        :return:
        """
        # Количество уже записанных в БД данных
        self.count_ts_to_record = count_ts_to_record
        # Тип данных
        self.list_measure = list_measure
        # Количество элементов в дереве подключения
        self.count_tree = count_tree


        # обнуляем все наши Глобальные переменные
        self.JSON_meterdata = {}
        self.JSON_meterdata_deconstruct = {}
        self.JSON_record = {}
        self.MeterId_list = []
        self.DeviceIdx_list = []
        self.database_was_recording = []
        self.JSON_Meter_Dev = {}
        self.JSON = {}

    # ----------------------- Метод для Записывания данных в БД ------------------------------------------
    def _RECORD_DATABASE(self, JSON_record_for_data_base):
        """
        Записываем данные в БД
        :param JSON_record_for_data_base:
        :return:
        """

        # Ветка записи в БД - Получаем данные
        self.JSON_Meter_Dev = JSON_record_for_data_base

        # Ветка записи в БД - Валидация наших записей до уровня Meterdata
        self.JSON_meterdata = self.__generate_data_to_meter_data()

        # Ветка записи в БД - После чего проводим его деконструкцию
        self.JSON_meterdata_deconstruct = self._deconstruct_JSON_meterdata_to_data_base()

        # Ветка записи в БД - Теперь Этот ДЕКОНСТРУИРОВАННЫЙ JSON Отправляем на запись
        self._record_values_in_database()

    # ----------------------- Метод для Записывания данных в Счетчик ------------------------------------------
    def _RECORD_METER(self, JSON_for_MeterDev):
        """
        Записываем наши данные в счетчик

        :param JSON_for_MeterDev:
        :return:
        """
        # Ветка счетчика
        self.JSON_Meter_Dev = JSON_for_MeterDev

        # Ветка счетчика -  Записываем Наши данные в счетчик
        self.JSON_record  = self._recording_data_in_virtual_meter()

    # ----------------------- Метод для Разделения данных -  БД и Счетчик--------------------------------------
    def _Separate_Data(self):
        """
        В этом методе разделяем данные
        Что пойдетв БД , а что пойдет в Счетчик
        :return:
        """
        from working_directory.Template.Template_Meter_daemon.Template_separate_record import SeparateJSONfromMeterDev

        Data = {}

        # Теперь - что делаем - Мы разделяем Наши записи - Что пойдетв БД, что пойдет в счетчик
        Separate = SeparateJSONfromMeterDev(JSON_original=self.JSON_Meter_Dev,
                                            count_ts_to_record=self.count_ts_to_record)

        # Это значения которые будут записаны в БД
        Data['JSON_record_for_data_base'] = Separate.JSON_record_for_data_base

        # Это значения что будут подложены в ИМИТАТОР СЧЕТЧИКА
        Data['JSON_for_MeterDev'] = Separate.JSON_for_MeterDev

        return Data

    # -----------------------------------------------------------------------------------------------------------------
    #                                     Основная ФУНКЦИЯ ЗАПУСКА - Наша БД ЗАПОЛНЕНА
    # -----------------------------------------------------------------------------------------------------------------
    def DataBase_filled(self,
                        # Тип данных - Список
                        list_measure: list = ['ElMonthEnergy'],
                        # количество записей в БД
                        count_ts_to_record: int = 0,
                        # Количество элементов в дереве подключения
                        count_tree: int = 2
                        ):
        """
        Здесь содержится Тесты для УЖЕ заполненной БД - Заполняется только ОДИН таймштамп
        """
        # Чистим БД
        deleteMeterTable()
        sleep(2)

        # переопределяем тэги :
        self._Define_test_data(
            # Тип данных - Список
            list_measure=list_measure,
            # количество записей в БД
            count_ts_to_record=count_ts_to_record,
            # Количество элементов в дереве подключения
            count_tree=count_tree
        )

        # ТЕПЕРЬ - ГЕНЕРИРУЕМ НУЖНОЕ КОЛИЧЕСТВО ЗАПИСЕЙ
        count_timesatamp = self._definition_count_timestamp()

        # Генерируем данные данные для нашего счетчика
        self.JSON_Meter_Dev = self._generate_data_to_meter_dev(count_timesatamp)
        # Теперь - что делаем - Мы разделяем Наши записи - Что пойдетв БД, что пойдет в счетчик
        Separate = self._Separate_Data()

        # Это значения которые будут записаны в БД
        JSON_record_for_data_base = Separate.get('JSON_record_for_data_base')

        # Это значения что будут подложены в ИМИТАТОР СЧЕТЧИКА
        JSON_for_MeterDev = Separate.get('JSON_for_MeterDev')

        # Теперь Записываем нужное количество записей в MeterTable
        self.__recording_data_in_metertable()
        # --->
        # Ветка БД
        self._RECORD_DATABASE(JSON_record_for_data_base=JSON_record_for_data_base)
        # И селектим в БД ДО ЗАПИСИ
        data_base_before_recording = ReceivingDataAccordingToJSON(JSON=self.JSON_meterdata,
                                                                  Select_all=True).get_result()
        # Ветка счетчика
        self._RECORD_METER(JSON_for_MeterDev=JSON_for_MeterDev)

        # Валидируем наши записи до уровня Meterdata
        self.JSON_meterdata = self.__generate_data_to_meter_data()

        # После чего проводим его деконструкцию
        self.JSON_meterdata_deconstruct = self._deconstruct_JSON_meterdata_to_data_base()

        # Теперь генерируем наш JSON
        self.JSON = self._GenerateJSON()

        start_meter =  datetime.now()
        # # Теперь запускаем имитатор отдельным потоком
        server = threading.Thread(target=self.__EmulatorMeter)
        server.start()

        # --->
        # Теперь что делаем - Теперь запускаем наш сформированный JSON в в мененеджер задааний
        self.Setup()

        # После чего объеденяем потоки

        server.join()

        # Теперь - Надо Понять что все записалось в нашу таблицу
        print('Счтчик работал длился: ', datetime.now() - start_meter)
        sleep(20)

        # Итак - Теперь Перезаписываем Деконструируемый JSON

        # И селектим в БД ПОСЛЕ ЗАПИСИ
        data_base_after_recording = ReceivingDataAccordingToJSON(JSON=self.JSON_meterdata,
                                                                 Select_all=True).get_result()

        # И после чего ищем что записанно по факту
        self.database_was_recording = DataBaseWasRecordingInFact(
            database_before=data_base_before_recording,
            database_after=data_base_after_recording
        ).DataBase_was_recording

        # print('database_was_recording', self.database_was_recording)
        # print('JSON_meterdata_deconstruct', self.JSON_meterdata_deconstruct)
        result = CheckUP(DataBase_was_recording=self.database_was_recording,
                         JSON_deconstruct=self.JSON_meterdata_deconstruct).error_collector

        # Теперь если есть ошибки - логируем их

        result = self.write_log(result=result)

        return result

    # -----------------------------------------------------------------------------------------------------------------
    #                                     Основная ФУНКЦИЯ ЗАПУСКА - Наша БД ПУСТАЯ
    # -----------------------------------------------------------------------------------------------------------------
    def DataBase_clear(self,
                       list_measure: list = ['ElMonthEnergy'],
                       # Количество элементов в дереве подключения
                       count_tree: int = 2):
        """
        Здесь содержиться Тесты для УЖЕ заполненой БД - Заполняется только ОДИН таймштамп
        """
        # Чистим БД
        deleteMeterTable()
        sleep(2)

        # переопределяем тэги
        # переопределяем тэги :
        self._Define_test_data(
            # Тип данных - Список
            list_measure=list_measure,
            # количество записей в БД
            count_ts_to_record=None,
            # Количество элементов в дереве подключения
            count_tree=count_tree
        )
        # генерируем отрезки времени
        count_timesatamp = self._definition_count_timestamp()

        # Генерируем данные данные для нашего счетчика
        JSON_for_MeterDev = self._generate_data_to_meter_dev(count_timesatamp)

        # Теперь Записываем нужноe количество записей в MeterTable
        self.__recording_data_in_metertable()

        # Ветка счетчика -  Записываем Наши данные в счетчик
        self._RECORD_METER(JSON_for_MeterDev=JSON_for_MeterDev)

        # Валидируем наши записи до уровня Meterdata
        self.JSON_meterdata = self.__generate_data_to_meter_data()

        # И селектим в БД ДО ЗАПИСИ
        data_base_before_recording = ReceivingDataAccordingToJSON(JSON=self.JSON_meterdata,
                                                                  Select_all=True).get_result()

        # После чего проводим его деконструкцию
        self.JSON_meterdata_deconstruct = self._deconstruct_JSON_meterdata_to_data_base()

        # print(self.JSON_meterdata_deconstruct)

        for i in self.JSON_meterdata_deconstruct :
        #     for x in i :
        #         print(x)

            print(len(i))
        # Теперь генерируем наш JSON
        self.JSON = self._GenerateJSON()
        start_meter = datetime.now()
        # # Теперь запускаем имитатор отдельным потоком
        server = threading.Thread(target=self.__EmulatorMeter)
        server.start()

        time.sleep(3)
        # Теперь что делаем - Теперь запускаем наш сформированный JSON в в мененеджер задааний
        self.Setup()

        # После чего объеденяем потоки

        server.join()

        # Теперь - Надо Понять что все записалось в нашу таблицу

        sleep(10)
        print('Счтчик работал длился: ', datetime.now() - start_meter)
        # Итак - Теперь Перезаписываем Деконструируемый JSON

        # И селектим в БД ПОСЛЕ ЗАПИСИ
        data_base_after_recording = ReceivingDataAccordingToJSON(JSON=self.JSON_meterdata,
                                                                 Select_all=True).get_result()

        # И после чего ищем что записанно по факту
        self.database_was_recording = DataBaseWasRecordingInFact(
            database_before=data_base_before_recording,
            database_after=data_base_after_recording
        ).DataBase_was_recording

        # ТЕПЕРЬ НАДО - убрать записи с valid 0
        result = CheckUP(DataBase_was_recording=self.database_was_recording,
                         JSON_deconstruct=self.JSON_meterdata_deconstruct).error_collector

        # print(result)
        # print(result)
        # for i in result :
        #     print(i)

        # Теперь если есть ошибки - логируем их
        result = self.write_log(result=result)

        return result


#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                                   МНОГОПОТОЧНЫЙ ВАРИАНТ РАБОТЫ - ДО 10 СЧЕТЧИКОВ
# -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################


class MeterDaemonManyMeter(MeterDaemonSingleMeter):
    '''
    Этот класс предназначен для тестирования демона опроса ПУ
    '''
    API = 'uspd-meter_daemon'
    type_connect = 'virtualbox'
    error = None
    port = 7777
    count_thread = 0

    MeterId_list = []
    DeviceIdx_list = []
    count_ts_to_record = 0

    database_was_recording = []

    JSON_meterdata_deconstruct = []

    JSON_meterdata = {}
    JSON_Meter_Dev = {}
    JSON_record = {}
    JSON = {}

    ports = {}

    InterfaceConfig: str = "9600,8n1"

    count_meter = 1

    # тип конекта
    iface = 'Ethernet'
    # Имя счетчика - Берется из БД
    type_meter = 'SE303'
    # Серийник нашего счетчика
    address_meter = "141227285"
    # address_meter = "134256651"
    # Количество сгенерированных штук
    generate_count = 1
    # Количество степеней зависимости
    count_tree = 2

    setup_mosquitto = False

    # серийник
    serial = '009218054000006'

    # ----------------------------------------------------------------------------------------------------------------
    #                                            Вспомогательные методы
    # ----------------------------------------------------------------------------------------------------------------

    # ---------------------------- Метод для ЗАПУСКА НАШЕГО ВИРТУАЛЬНОГО СЧЕТЧКА -------------------------------

    # Лучше всего запускать в  отдельном потоке - Надо будет как нить разобраться
    def __EmulatorMeter(self):
        """В этом методе подымаем локальный серевер с нашим виртуальным счетчиком"""
        from working_directory.Template.Template_Meter_devices_API.Template_socket_in_meters import SocketMeters
        # Создаем словарь из наших потоков
        Thread_dict = {}
        # print('СОЗДАЕМ ')

        # Создаем словарь потоков из наших счетчиков
        for self.count_thread in range(self.count_meter):
            # Создаем словарь из портов
            port = self.ports['thread_' + str(self.count_thread)]
            DeviceId = self.DeviceIdx_list[self.count_thread]
            # Теперь по Этому DeviceID вытаскиваем данные для того чтоб протащить их в Счетчик
            Data = self.JSON_record[DeviceId]
            # и определяем серийник
            Serial = str(self.serial) + '_' + str(DeviceId)

            # Создаем поток
            Thread_dict['Thread_meter_' + str(self.count_thread)] = threading.Thread(target=SocketMeters,
                                                                                     args=(port, Data, Serial))
            # Запускаем его
            # Thread_dict['Thread_meter_' + str(self.count_thread)].start()

        # Теперь важная штука - надо предотвратить гонку потоков
        # Ждем когда Наступит момент запускать
        while True:
            if self.setup_mosquitto:
                break
        # ЗАПУСКАЕМ

        for Thread_meter in Thread_dict:
            Thread_dict[Thread_meter].start()
        # Ждем пока отработает
        sleep(20)

        Thread_list = list(Thread_dict.keys())
        # Теперь мониторим наши потоки
        while True:

            # Создаем список на удаление
            Thread_list_to_remove = []
            # Петебираем все потоки на предмет завершения
            for thread in Thread_list:
                # Если поток завершен
                if Thread_dict[thread].is_alive() is False:
                    # Убиваем его
                    Thread_dict[thread].join()
                    # После Добавляем в список на удаление
                    Thread_list_to_remove.append(thread)

            # Удаляем его из рабочих
            for i in Thread_list_to_remove:
                Thread_list.remove(i)
            # Если у нас нет рабочих потоков - То выходим из цикла
            if len(Thread_list) < 1:
                break

        self.setup_mosquitto = False

        return Thread_dict

    # ---------------------------- Метод для Генерации Нужных данных в MeterTable   -------------------------------

    def __recording_data_in_metertable(self):
        '''
        Здесь  Генерируем нашу запись в MeterTable
        Возвращаем список внутрених айдищников и внешних - Это важно
        '''

        from working_directory.Template.Template_MeterJSON.Template_Record_MeterTable import GenerateRecordMeterTable
        from copy import deepcopy

        # получаем наш айпишник
        Ip_addres = str(self.__GetIPConfig())

        # ТЕПЕРЬ -  ЗАПИСЫВАЕМ ПО ОДНОМУ
        for i in range(self.count_meter):
            # ПОЛУЧАЕМ АДРЕСС СЧЕТЧИКА
            adress = Ip_addres + str(self.ports['thread_' + str(i)])

            Generate_Record_Meter = GenerateRecordMeterTable(
                generate_count=1,
                count_tree=self.count_tree,
                type_connect=self.iface,
                type_meter=self.type_meter,
                address_meter=self.address_meter,
                adress=adress,
                InterfaceConfig=self.InterfaceConfig
            )

            self.MeterId_list = self.MeterId_list + deepcopy(Generate_Record_Meter.MeterId_list)
            self.DeviceIdx_list = self.DeviceIdx_list + deepcopy(Generate_Record_Meter.DeviceIdx_list)
            # del Generate_Record_Meter

    # ---------------------------- Метод для достраивания данных до уровня MeterData     ------------------------------

    def __generate_data_to_meter_data(self, JSON_Meter_Dev, deviceIdx):
        """Метод который достраивает JSON до уровня meter data"""

        # Достраиваем JSON до уровня meter data
        from working_directory.Template.Template_Meter_daemon.Template_assembly_normal_JSON_like_POST_meter_Data import \
            AssemblyDictLikeMeterData
        from copy import deepcopy

        MeterDev_to_Assembly = deepcopy(JSON_Meter_Dev)
        restructuring = AssemblyDictLikeMeterData(JSON_list = MeterDev_to_Assembly,
                                                  ids_meter = [deviceIdx],
                                                  serial = str(self.serial) + '_' + str(deviceIdx)
                                                  )

        JSON_dict_meterdata = restructuring.JSON

        JSON_dict_meterdata_GET = restructuring.JSON_GET

        # Здесь возвращаем глубокую копию ради избежания перезаписи . ЛОЛ

        self.JSON_meterdata[deviceIdx] = JSON_dict_meterdata

        return deepcopy(JSON_dict_meterdata)

    # ///////////////////

    # ----------------------------------------------------------------------------------------------------------------
    #                                            Вспомомгательные методы
    # ----------------------------------------------------------------------------------------------------------------
    # ------------------ Получаем свой айпишник на котором работает наш виртуальный счетчик ------------------------
    def __GetIPConfig(self):
        """
        Получаем наш Айпишник - нужен для того чтоб сделать сервер с виртуальным счетчиком

        :return:
        """

        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", self.port))
        socket_name = (s.getsockname()[0])
        s.close()

        return socket_name + ':'

    # ---------------------------- Генерация данных для Виртуального счетчика ----------------------------------------
    # Пока сделаем это отдельным методом - Как там будет дальше - я не знаю
    def _generate_data_to_meter_dev(self, count_timestamp={}):
        """
        В Этом Методе генерируем наши JSON для MeterDEV
        :return:
        """
        from working_directory.Template.Template_Meter_daemon.Template_generator_data_for_Meter_Dev import \
            GenerateDataForMeterDev

        JSON_Meter_Dev = {}

        # -Ссылки на данные будут по Device Idx
        for i in self.DeviceIdx_list:
            JSON_Meter_Dev[i] = GenerateDataForMeterDev(
                measure_list=self.list_measure,
                count_timestamp=count_timestamp).JSON_Meter_Dev

        return JSON_Meter_Dev

    # ---------------------------- Метод для записи НАШИХ ДАННЫХ в ВИРТУАЛЬНЫЙ СЧЕТЧИК -------------------------------
    def _recording_data_in_virtual_meter(self, JSON_Meter_Dev):
        """
        Записываем НАШИ ДАННЫЕ  директорию виртуального счетчика
        :return:
        """
        from working_directory.Template.Template_Meter_devices_API.Template_record_values_for_meter import \
            RecordFromEmulatorMeter
        Record_JSON = RecordFromEmulatorMeter(JSON_Meter_Dev).GET_Record()

        return Record_JSON

    # ---------------- Метод для Деконструкции данных MeterData до уровня селекта из БД ------------------------------
    def _deconstruct_JSON_meterdata_to_data_base(self, JSON_meterdata, deviceIdx):
        """
        Итак - Здесь проводим ДЕКОНСТРУКЦИЮ JSON MeterData до уровня селекта в БД
        :return:
        """

        from working_directory.Template.Template_MeterJSON.Template_Deconstruct import DeconstructJSON

        JSON_for_compare_to_data_base = DeconstructJSON(JSON=JSON_meterdata).JSON_deconstruct

        self.JSON_meterdata_deconstruct[deviceIdx] = JSON_for_compare_to_data_base
        return JSON_for_compare_to_data_base

    # -------------------------------------  Метод для ЗАПИСИ В БД ЗНАЧЕНИЙ  ------------------------------------------
    def _record_values_in_database(self, JSON_meterdata_deconstruct, DeviceIdx):
        """
        ЗДЕСЬ ЗАПИСЫВАЕМ НАШИ ЗАПИСИ В БД
        :param JSON_deconstruct:
        :return:
        """

        from working_directory.Template.Template_Meter_db_data_API.Template_record_value_to_database import \
            RecordValueToDataBase

        # RecordValueToDataBase.SET_Serial(serial=str(self.serial) + '_' + str(self.port))
        RecordValueToDataBase(JSON_deconstruct=JSON_meterdata_deconstruct,
                              serial=str(self.serial) + '_' + str(DeviceIdx))

    # ----------------------- Метод для Генерации Топика задания - Это важно ------------------------------------------

    def _GenerateJSON(self):
        """
        Метод для Генерации Топика задания - Это важно
        """
        from working_directory.Template.Template_Meter_daemon.Template_generator_JSON_for_mosquitto import \
            GenerateForMosquittoJSON
        from working_directory.Connect.JSON_format_coding_decoding import code_JSON

        JSON_dict = GenerateForMosquittoJSON(Measure_type_list=self.list_measure,
                                             MeterId_list=self.MeterId_list).jobs

        # Теперь Это все конфертируем в JSON
        JSON = code_JSON(JSON_dict)
        return JSON

    # ----------------------- Метод для определения входных данных ------------------------------------------
    def _Define_test_data(self, list_measure, count_ts_to_record, count_tree, count_meter):
        """
        В ЭТОМ МЕТОДЕ ПЕРЕЗАПИСЫВАЕМ наши тестовые данные что нам дали  - ЭТО ВАЖНО
        :param list_measure: # Тип данных - Список
        :param count_ts_to_record: # количество записей в БД
        :param count_tree:  # Количество элементов в дереве подключения
        :return:
        """
        # Количество уже записанных в БД данных
        self.count_ts_to_record = count_ts_to_record
        # Тип данных
        self.list_measure = list_measure
        # Количество элементов в дереве подключения
        self.count_tree = count_tree
        # Количество добавляемых счетчиков
        self.count_meter = count_meter

        # обнуляем все наши Глобальные переменные
        self.JSON_meterdata = {}
        self.JSON_meterdata_deconstruct = {}
        self.JSON_record = {}

    # ----------------------- Метод для Записывания данных в БД ------------------------------------------
    def _RECORD_DATABASE(self, JSON_record_for_data_base):
        """
        Записываем данные в БД
        :param JSON_record_for_data_base:
        :return:
        """

        for DeviceIdx in JSON_record_for_data_base:
            # Ветка записи в БД - Валидация наших записей до уровня Meterdata

            JSON_meterdata = self.__generate_data_to_meter_data(JSON_Meter_Dev=JSON_record_for_data_base[DeviceIdx],
                                                                deviceIdx=DeviceIdx)

            # Ветка записи в БД - После чего проводим его деконструкцию
            JSON_meterdata_deconstruct = self._deconstruct_JSON_meterdata_to_data_base(JSON_meterdata=JSON_meterdata,
                                                                                       deviceIdx=DeviceIdx)

            # Ветка записи в БД - Теперь Этот ДЕКОНСТРУИРОВАННЫЙ JSON Отправляем на запись
            self._record_values_in_database(JSON_meterdata_deconstruct=JSON_meterdata_deconstruct,
                                            DeviceIdx = DeviceIdx)

    # ----------------------- Метод для Селекта из БД ------------------------------------------
    def _SELECT_TO_DATABASE(self):

        from working_directory.Template.Template_Meter_db_data_API.Template_read_handler_table import \
            ReceivingDataAccordingToJSON
        data_base = {}

        for deviceidx in self.JSON_meterdata:
            data_base_full = ReceivingDataAccordingToJSON(JSON=self.JSON_meterdata.get(deviceidx),
                                                                Select_all=True).get_result()
            # print('data_base_full' , data_base_full)
            # Теперь - очищаем от ненужных айдишников
            data_base[deviceidx] = []
            for i in data_base_full:
                data_base_idx_list = []
                for x in i:
                    if x.get('id') == deviceidx:
                        data_base_idx_list.append(x)
                data_base[deviceidx].append(data_base_idx_list)
            # data_base[deviceidx] = data_base_measure_idx_list
        return data_base

    # ----------------------- Метод для Записывания данных в Счетчик ------------------------------------------
    def _RECORD_METER(self, JSON_for_MeterDev):
        """
        Записываем наши данные в счетчик

        :param JSON_for_MeterDev:
        :return:
        """

        for deviceIdx in JSON_for_MeterDev:
            # Ветка счетчика -  Записываем Наши данные в счетчик
            JSON_record = self._recording_data_in_virtual_meter(JSON_Meter_Dev=JSON_for_MeterDev.get(deviceIdx))
            self.JSON_record[deviceIdx] = JSON_record

    # ----------------------- определяем данные для Счетчика --------------------------------------
    def _Data_for_Meter(self, Meter_dev):

        """
        Те данные что должны были прийти из счетчика - Валидируем из Состояния Meter dev в состояние Meter data
        :param Meter_dev:
        :return:
        """

        Meter_data_from_meter = {}

        self.JSON_meterdata = {}

        for DeviceIdx in Meter_dev:
            # Валидируем наши записи до уровня Meterdata
            Meter_data = self.__generate_data_to_meter_data(JSON_Meter_Dev=Meter_dev[DeviceIdx],
                                                            deviceIdx=DeviceIdx)

            self.JSON_meterdata[DeviceIdx] = Meter_data
            # После чего проводим его деконструкцию
            Meter_data_deconstruct = self._deconstruct_JSON_meterdata_to_data_base(JSON_meterdata=Meter_data,
                                                                                   deviceIdx=DeviceIdx)
            Meter_data_from_meter[DeviceIdx] = Meter_data_deconstruct

        return Meter_data_from_meter

    # ----------------------- Метод для Разделения данных -  БД и Счетчик--------------------------------------
    def _Separate_Data(self):
        """
        В этом методе разделяем данные
        Что пойдетв БД , а что пойдет в Счетчик
        :return:
        """
        from working_directory.Template.Template_Meter_daemon.Template_separate_record import SeparateJSONfromMeterDev

        Data = {}

        JSON_record_for_data_base = {}
        JSON_for_MeterDev = {}
        for Meter_key in self.JSON_Meter_Dev:
            # Теперь - что делаем - Мы разделяем Наши записи - Что пойдетв БД, что пойдет в счетчик
            Separate = SeparateJSONfromMeterDev(JSON_original=self.JSON_Meter_Dev[Meter_key],
                                                count_ts_to_record=self.count_ts_to_record)

            JSON_record_for_data_base[Meter_key] = Separate.JSON_record_for_data_base
            JSON_for_MeterDev[Meter_key] = Separate.JSON_for_MeterDev
        # Это значения которые будут записаны в БД
        Data['JSON_record_for_data_base'] = JSON_record_for_data_base

        # Это значения что будут подложены в ИМИТАТОР СЧЕТЧИКА
        Data['JSON_for_MeterDev'] = JSON_for_MeterDev

        return Data

    # ----------------------- определяем порты что будем использовать ------------------------------------------
    def _definition_ports(self):
        """
        В этом Методе определяем порты на которых будем запускать наши виртуальные счетчики
        :return:
        """
        self.ports = {}
        for self.count_thread in range(self.count_meter):
            # Здесь - очень важно - нужны РАЗНЫЕ ПОРТЫ ДЛЯ ТОГО ЧТОБ создать нужное коллиество счетчиков
            port = self.port + self.count_thread
            self.ports['thread_' + str(self.count_thread)] = port

    # ----------------------- Смотрим Что записалось по факту ------------------------------------------
    def _get_DataBase_was_recording_in_fact(self, data_base_before_recording, data_base_after_recording):

        DataBase_was_recording_dict = {}

        for deviceId in data_base_before_recording:
            database_was_recording = DataBaseWasRecordingInFact(
                database_before=data_base_before_recording.get(deviceId),
                database_after=data_base_after_recording.get(deviceId)
            ).DataBase_was_recording
            DataBase_was_recording_dict[deviceId] = database_was_recording

        return DataBase_was_recording_dict

    # ----------------------- Здесь сравниваем ДВА JSON  --------------------------------------
    # ----------------------- Здесь сравниваем ДВА JSON  --------------------------------------
    def _get_CheckUP(self):
        """
        Здесь по отдельности проверяем снятые показания с каждого счетчика отдельно

        :return:
        """
        result = []

        # ТЕПЕРЬ - Каждый Device IDx проверяем отдельно - Це важно

        for DeviceIdx in self.DeviceIdx_list:
            # print('database_was_recording = ', self.database_was_recording.get(DeviceIdx))
            # print('JSON_meterdata_deconstruct = ', self.JSON_meterdata_deconstruct.get(DeviceIdx))

            resultCheckUp = CheckUP(DataBase_was_recording=self.database_was_recording.get(DeviceIdx),
                                    JSON_deconstruct=self.JSON_meterdata_deconstruct.get(DeviceIdx)
                                    ).error_collector
            if len(resultCheckUp) > 0:
                error = {'DeviceIdx': DeviceIdx,
                         'ОШИБКА': resultCheckUp}
                result.append(error)

        return result

    # -----------------------------------------------------------------------------------------------------------------
    #                                     Основная ФУНКЦИЯ ЗАПУСКА - Наша БД ЗАПОЛНЕНА
    # -----------------------------------------------------------------------------------------------------------------
    def DataBase_filled(self,
                        # Тип данных - Список
                        list_measure: list = ['ElMonthEnergy'],
                        # количество записей в БД
                        count_ts_to_record: int = 0,
                        # Количество элементов в дереве подключения
                        count_tree: int = 2,
                        # Количество добавляемых счетчиков
                        count_meter: int = 2,
                        ):
        """
        Здесь содержится Тесты для УЖЕ заполненной БД - Заполняется только ОДИН таймштамп
        """

        # Чистим БД
        deleteMeterTable()
        sleep(2)

        # переопределяем тэги :
        self._Define_test_data(
            # Тип данных - Список
            list_measure=list_measure,
            # количество записей в БД
            count_ts_to_record=count_ts_to_record,
            # Количество элементов в дереве подключения
            count_tree=count_tree,
            # Количество добавляемых счетчиков
            count_meter=count_meter
        )

        # ТЕПЕРЬ - ГЕНЕРИРУЕМ НУЖНОЕ КОЛИЧЕСТВО ЗАПИСЕЙ

        # -----> Генерация Meter Table
        # определяем порты
        self._definition_ports()
        # Теперь Записываем нужное количество записей в MeterTable
        self.__recording_data_in_metertable()

        # -----> Генерация Meter Data
        # генерируем отрезки времени
        count_timesatamp = self._definition_count_timestamp()

        # Генерируем данные данные для нашего счетчика
        self.JSON_Meter_Dev = self._generate_data_to_meter_dev(count_timesatamp)

        # print(self.JSON_Meter_Dev)
        # Теперь - что делаем - Мы разделяем Наши записи - Что пойдет в БД, что пойдет в счетчик
        Separate = self._Separate_Data()

        # Это значения которые будут записаны в БД
        JSON_record_for_data_base = Separate.get('JSON_record_for_data_base')

        # Это значения что будут подложены в ИМИТАТОР СЧЕТЧИКА
        JSON_for_MeterDev = Separate.get('JSON_for_MeterDev')

        # --->
        # Ветка БД
        self._RECORD_DATABASE(JSON_record_for_data_base=JSON_record_for_data_base)
        # И селектим в БД ДО ЗАПИСИ

        data_base_before_recording = self._SELECT_TO_DATABASE()

        # Ветка счетчика - Записываем данные в счетчик
        self._RECORD_METER(JSON_for_MeterDev=JSON_for_MeterDev)

        self.JSON_meterdata_deconstruct = self._Data_for_Meter(Meter_dev=JSON_for_MeterDev)

        # Теперь генерируем наш JSON
        self.JSON = self._GenerateJSON()

        # # Теперь запускаем имитатор отдельным потоком
        server = threading.Thread(target=self.__EmulatorMeter)
        server.start()
        #
        # --->
        # Подымаем Сервера счетчиков
        self.setup_mosquitto = True

        # Теперь что делаем - Теперь запускаем наш сформированный JSON в в мененеджер задааний
        self.Setup()

        # Теперь ждем пока счетчики отработают
        while True:
            if not self.setup_mosquitto:
                break
        # После чего объедением потоки
        server.join()

        # Теперь - Надо Понять что все записалось в нашу таблицу
        sleep(20)

        # И селектим в БД ПОСЛЕ ЗАПИСИ
        data_base_after_recording = self._SELECT_TO_DATABASE()

        # И после чего ищем что записано по факту

        self.database_was_recording = self._get_DataBase_was_recording_in_fact(
            data_base_after_recording=data_base_after_recording,
            data_base_before_recording=data_base_before_recording)

        # # print('database_was_recording', self.database_was_recording)
        # # print('JSON_meterdata_deconstruct', self.JSON_meterdata_deconstruct)
        result = self._get_CheckUP()

        # print(result)
        # Теперь если есть ошибки - логируем их

        result = self.write_log(result=result)

        return result

    # -----------------------------------------------------------------------------------------------------------------
    #                                     Основная ФУНКЦИЯ ЗАПУСКА - Наша БД ПУСТАЯ
    # -----------------------------------------------------------------------------------------------------------------
    def DataBase_clear(self,
                       list_measure: list = ['ElMonthEnergy'],
                       # Количество элементов в дереве подключения
                       count_tree: int = 2,
                       # Количество добавляемых счетчиков
                       count_meter: int = 2, ):
        """
        Здесь содержиться Тесты для УЖЕ заполненой БД - Заполняется только ОДИН таймштамп
        """
        # Чистим БД
        deleteMeterTable()
        sleep(2)

        # переопределяем тэги :
        self._Define_test_data(
            # Тип данных - Список
            list_measure=list_measure,
            # количество записей в БД
            count_ts_to_record=None,
            # Количество элементов в дереве подключения
            count_tree=count_tree,
            # Количество добавляемых счетчиков
            count_meter=count_meter
        )

        # ТЕПЕРЬ - ГЕНЕРИРУЕМ НУЖНОЕ КОЛИЧЕСТВО ЗАПИСЕЙ

        # -----> Генерация Meter Table
        # определяем порты
        self._definition_ports()
        # Теперь Записываем нужное количество записей в MeterTable
        self.__recording_data_in_metertable()

        # -----> Генерация Meter Data
        # генерируем отрезки времени
        count_timesatamp = self._definition_count_timestamp()

        # Генерируем данные данные для нашего счетчика
        self.JSON_Meter_Dev = self._generate_data_to_meter_dev(count_timesatamp)
        JSON_for_MeterDev = self.JSON_Meter_Dev

        # print(JSON_for_MeterDev)
        self.JSON_meterdata_deconstruct = self._Data_for_Meter(Meter_dev=JSON_for_MeterDev)

        # --->
        # И селектим в БД ДО ЗАПИСИ

        data_base_before_recording = self._SELECT_TO_DATABASE()

        # Ветка счетчика - Записываем данные в счетчик
        self._RECORD_METER(JSON_for_MeterDev=self.JSON_Meter_Dev)

        # Теперь генерируем наш JSON
        self.JSON = self._GenerateJSON()

        # # Теперь запускаем имитатор отдельным потоком
        server = threading.Thread(target=self.__EmulatorMeter)
        server.start()
        #
        # --->
        # Подымаем Сервера счетчиков
        self.setup_mosquitto = True

        # Теперь что делаем - Теперь запускаем наш сформированный JSON в в мененеджер задааний
        self.Setup()

        # Теперь ждем пока счетчики отработают
        while True:
            if not self.setup_mosquitto:
                break
        # После чего объедением потоки
        server.join()

        # Теперь - Надо Понять что все записалось в нашу таблицу
        sleep(20)

        # И селектим в БД ПОСЛЕ ЗАПИСИ
        data_base_after_recording = self._SELECT_TO_DATABASE()

        # И после чего ищем что записанно по факту

        self.database_was_recording = self._get_DataBase_was_recording_in_fact(
            data_base_after_recording=data_base_after_recording,
            data_base_before_recording=data_base_before_recording)

        # # print('database_was_recording', self.database_was_recording)
        # # print('JSON_meterdata_deconstruct', self.JSON_meterdata_deconstruct)
        result = self._get_CheckUP()

        # print(result)
        # Теперь если есть ошибки - логируем их

        result = self.write_log(result=result)

        return result


# # -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                                               Тестовые Запуски
# -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################
# from time import sleep
# from working_directory.sqlite import deleteMeterTable

# # ------------------------------------------- Реальный СЧЕТЧИК --------------------------------------------------------
# deleteMeterTable()
# sleep(1)
# #
# MeterDaemon_result = MeterDaemon('ssh').RealMeter(list_measure=['ElMomentEnergy'],
#                                                                   MeterConfig=[])
# print(MeterDaemon_result)


# # ------------------------------------------- ОДИН СЧЕТЧИК --------------------------------------------------------
deleteMeterTable()
sleep(1)
#
# MeterDaemon_result = MeterDaemonSingleMeter('ssh').DataBase_clear(list_measure=['ElConfig'],
#                                                                   count_tree=2)
# print(MeterDaemon_result)
#
#

from datetime import datetime
start = datetime.now()

MeterDaemon_result = MeterDaemonSingleMeter(type_connect='ssh').DataBase_filled(
            list_measure=['ElJrnlPwr'],
            count_ts_to_record=10,
            count_tree=2)
print('прогон длился: ', datetime.now() - start)
print(MeterDaemon_result)
# # ----------------------------------------- МНОГОПОТОЧНЫЙ РЕЖИМ ----------------------------------------------------
# Чистим БД
# deleteMeterTable()
# sleep(1)
# #
# result = MeterDaemonManyMeter(type_connect='ssh').DataBase_filled(list_measure=['ElMomentEnergy'], count_meter=10,
#                                                                   count_ts_to_record=0)
# print(result)

# a = MeterDaemonSingleMeter().DataBase_filled(list_measure=['ElArr1ConsPower'], count_ts_to_record=100000)
# print(a)
# print(datetime.datetime.now())
# print(a)
# for i in ['ElConfig',
# 'ElMomentEnergy',
# 'ElDayEnergy',
# 'ElMonthEnergy',
# 'ElDayConsEnergy',
# 'ElMonthConsEnergy',
# 'ElMomentQuality',
# 'ElArr1ConsPower'] :


# lol = ['ElArr1ConsPower']
#
# for i in lol :
#
#     deleteMeterTable()
#     sleep(1)
#
#     MeterDaemon_result = MeterDaemonSingleMeter('ssh').DataBase_clear(list_measure=[i],
#                                                                       count_tree=2)
#     print(MeterDaemon_result)