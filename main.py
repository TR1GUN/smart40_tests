# Итак здесь расположим наш тест для демона опроса ПУ
from working_directory.Template.Template_Meter_daemon.Template_generator_JSON_for_mosquitto import \
    GenerateForMosquittoJSON
from working_directory.Connect.JSON_format_coding_decoding import code_JSON
from working_directory.Template.Template_Meter_db_data_API.Template_read_handler_table import \
    ReceivingDataAccordingToJSON
from working_directory.Template.Template_Meter_daemon.Template_separate_record import SeparateJSONfromMeterDev
from working_directory.Template.Template_Meter_daemon.Template_select_data_base_was_recording import \
    DataBaseWasRecordingInFact
# RecordValueToDataBase,
# from working_directory.Template.Template_Meter_db_data_API.Template_checkup_from_Meter_db_data_API import CheckUP , POSTCheckUP
from working_directory.Template.Template_Meter_daemon.Template_CheckUp_for_MeterDaemon import CheckUP
from working_directory.Template.Template_Setup import Setup
from working_directory.log import log
from time import sleep
from working_directory.sqlite import deleteMeterTable
import threading
import time


# -------------------------------------------------------------------------------------------------------------------
#                       Делаем основной класс - От которого будем наследоваться
#                                     В него внесем общие методы
# -------------------------------------------------------------------------------------------------------------------
class MeterDaemon:
    '''
    Этот класс преднозначен для тестирования демона опроса ПУ
    '''
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

    InterfaceConfig =  "9600,8n1"
    # тип конекта
    iface =   'Ethernet'
    # Имя счетчика - Берется из БД
    type_meter  =   'SE303'
    # Серийник нашего счетчика
    address_meter  =   "134256651"
    # Количество элементов в дереве зависимостей
    count_tree =  2
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
                'count_tree' : self.count_tree,
                # тип конекта
                'iface': self.iface,
                # Имя счетчика - Берется из БД
                'type_meter': self.type_meter,
                # Серийник нашего счетчика
                'address_meter': self.address_meter,
                # Адресс нашего счетчика
                'address' : self.address ,
                # ИтнерфесКонфиг
                'InterfaceConfig': self.InterfaceConfig,



            }
        # сначала проверяем что подали кеоректные данные
        if (len(MeterConfig)) and (type(MeterConfig) is list) > 0 :
            for i in MeterConfig :
                # Теперь смотрим что КАЖДЫЙ элемент
                if type(i) is dict :
                    # Теперь проверяем ключи
                    for key in MeterConfig_Template :
                        if i.get(key) is None :
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
    # address_meter = "141227285"
    address_meter = "134256651"

    # Количество сгенерированных штук
    generate_count = 1
    # Количество степеней зависимости
    count_tree = 2

    # ----------------------------------------------------------------------------------------------------------------
    #                                            Вспомомгательные методы
    # ----------------------------------------------------------------------------------------------------------------
    def _definition_count_timestamp(self):
        """
        Определение количества таймштампов
        :return:
        """
        from working_directory.Template.Template_Meter_daemon.Daemon_settings import ArchInfo_settings
        # ГЕНЕРИРУЕМ НУЖНОЕ КОЛИЧЕСТВО ЗАПИСЕЙ
        count_timesatamp = {}
        for i in range(len(self.list_measure)):
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

    # ---------------------------- Метод для ЗАПУСКА НАШЕГО ВИРТУАЛЬНОГО СЧЕТЧКА -------------------------------

    # Лучше всего запускать в  отдельном потоке - Надо будет как нить разобраться
    def __EmulatorMeter(self):
        """В этом методе подымаем локальный серевер с нашим виртуальным счетчиком"""
        from working_directory.Template.Template_Meter_devices_API.Template_socket_in_meters import SocketMeters

        # Получаем наш список типов данных данных
        self.Emulator = SocketMeters(conect_port=self.port)

        # После удаляем обьект
        # del self.Emulator

    # ---------------------------- Метод для Генерации Нужных данных в MeterTable   -------------------------------

    def __recording_data_in_metertable(self):
        '''
        Здесь  Генерируем нашу запись в MeterTable
        Возвращаем список внутрених айдищников и внешних - Это важно
        '''

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

        JSON_dict_meterdata = AssemblyDictLikeMeterData(self.JSON_Meter_Dev, self.DeviceIdx_list).JSON

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

        RecordValueToDataBase(JSON_deconstruct=self.JSON_meterdata_deconstruct)

    # ----------------------- Метод для Генерации Топика задания - Это важно ------------------------------------------

    def _GenerateJSON(self):
        """
        Метод для Генерации Топика задания - Это важно
        """
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
        self._recording_data_in_virtual_meter()

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
        self.JSON_Meter_Dev = []
        self.list_measure = []

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
        Separate = SeparateJSONfromMeterDev(JSON_original=self.JSON_Meter_Dev,
                                            count_ts_to_record=self.count_ts_to_record)

        # Это значения которые будут записаны в БД
        JSON_record_for_data_base = Separate.JSON_record_for_data_base

        # Это значения что будут подложены в ИМИТАТОР СЧЕТЧИКА
        JSON_for_MeterDev = Separate.JSON_for_MeterDev

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

        # # Теперь запускаем имитатор отдельным потоком
        server = threading.Thread(target=self.__EmulatorMeter)
        server.start()

        # --->
        # Теперь что делаем - Теперь запускаем наш сформированный JSON в в мененеджер задааний
        self.Setup()

        # После чего объеденяем потоки

        server.join()

        # Теперь - Надо Понять что все записалось в нашу таблицу

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

        print('database_was_recording', self.database_was_recording)
        print('JSON_meterdata_deconstruct', self.JSON_meterdata_deconstruct)
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

        # Генерируем данные данные для нашего счетчика
        JSON_for_MeterDev = self._generate_data_to_meter_dev()

        # Теперь Записываем нужноe количество записей в MeterTable
        self.__recording_data_in_metertable()

        # Теперь генерируем наш JSON
        self.JSON = self._GenerateJSON()

        # Теперь что делаем - Теперь запускаем наш сформированный JSON в в мененеджер задааний
        self.Setup()

        # И селектим в БД ПОСЛЕ ЗАПИСИ
        result = ReceivingDataAccordingToJSON(JSON=self.JSON_meterdata,
                                                                 Select_all=True).get_result()
        return result


    def RealMeter(self,
                       MeterConfig = [],
                       list_measure: list = ['ElMonthEnergy'],
                       # Количество элементов в дереве подключения
                       count_tree: int = 2):
        """
        Здесь содержиться Тесты для УЖЕ заполненой БД - Заполняется только ОДИН таймштамп
        """
        # Чистим БД
        deleteMeterTable()
        sleep(2)

        MeterConfig = [{
        # ИтнерфесКонфиг
        'InterfaceConfig' : "9600,8n1" ,
        # тип конекта
        'iface'  :  'Ethernet' ,
        # Имя счетчика - Берется из БД
        'type_meter'  :  'SE303',
        # Серийник нашего счетчика
        'address_meter'  :  "134256651" ,
        }]
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
            count_tree=count_tree
        )

        # Теперь Записываем нужноe количество записей в MeterTable
        self.__recording_data_in_metertable()

        # Теперь генерируем наш JSON
        self.JSON = self._GenerateJSON()

        # Теперь что делаем - Теперь запускаем наш сформированный JSON в в мененеджер задааний
        self.Setup()

        # И селектим в БД ПОСЛЕ ЗАПИСИ
        result = ReceivingDataAccordingToJSON(JSON=self.JSON_meterdata,
                                              Select_all=True).get_result()
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
deleteMeterTable()
sleep(1)

MeterDaemon_result = MeterDaemon('ssh').RealMeter(list_measure=['ElMomentEnergy'],
                                                                  MeterConfig=[])
print(MeterDaemon_result)


# # ------------------------------------------- ОДИН СЧЕТЧИК --------------------------------------------------------
# deleteMeterTable()
# sleep(1)
#
# MeterDaemon_result = MeterDaemonSingleMeter('ssh').DataBase_clear(list_measure=['ElMomentEnergy'],
#                                                                   count_tree=2)
# print(MeterDaemon_result)

# MeterDaemon_result = MeterDaemonSingleMeter(type_connect='ssh').DataBase_filled(
#             list_measure=['ElMomentEnergy'],
#             count_ts_to_record=0,
#             count_tree=2
#                                                  )
# print(MeterDaemon_result)
# # ----------------------------------------- МНОГОПОТОЧНЫЙ РЕЖИМ ----------------------------------------------------
# Чистим БД

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
