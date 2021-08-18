from working_directory.sqlite import deleteMeterTable
from working_directory.Meter_daemon import MeterDaemonSingleMeter
import threading
from time import sleep

from working_directory.Template.Template_Meter_daemon.Template_select_data_base_was_recording import \
    DataBaseWasRecordingInFact
from working_directory.Template.Template_Meter_daemon.Template_CheckUp_for_MeterDaemon import CheckUP


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
            Serial = str(DeviceId)

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

        print('Thread_dict', Thread_dict)

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

        # После проверяем что ЭТО У НАС отработало
        # i = 0
        #
        # while i != self.count_meter:
        #     # Завершенные потоки
        #     completed_thread = []
        #     for thread in Thread_dict:
        #
        #         print('is_alive() ', Thread_dict[thread].is_alive())
        #         if Thread_dict[thread].is_alive() is False:
        #             Thread_dict[thread].join()
        #             i = i + 1
        #             completed_thread.append(thread)
        #
        #     for complete in completed_thread:
        #         completed_thread.pop(complete)
        # while True:
        #     for thread in Thread_dict:
        #         if Thread_dict[thread] is False:
        #             break
        # Теперь надо их обьеденить в один - После того как он отработал

        # for thread in Thread_dict:
        #     print('ЗАВЕРШАЕМ', Thread_dict[thread])
        #     Thread_dict[thread].join()
        # print('lol lol lol')

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
        restructuring = AssemblyDictLikeMeterData(MeterDev_to_Assembly, [deviceIdx])


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
    def _record_values_in_database(self, JSON_meterdata_deconstruct):
        """
        ЗДЕСЬ ЗАПИСЫВАЕМ НАШИ ЗАПИСИ В БД
        :param JSON_deconstruct:
        :return:
        """

        from working_directory.Template.Template_Meter_db_data_API.Template_record_value_to_database import \
            RecordValueToDataBase

        RecordValueToDataBase(JSON_deconstruct=JSON_meterdata_deconstruct)

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
            self._record_values_in_database(JSON_meterdata_deconstruct=JSON_meterdata_deconstruct)

    # ----------------------- Метод для Селекта из БД ------------------------------------------
    def _SELECT_TO_DATABASE(self):

        from working_directory.Template.Template_Meter_db_data_API.Template_read_handler_table import \
            ReceivingDataAccordingToJSON
        data_base = {}

        for deviceidx in self.JSON_meterdata:
            data_base[deviceidx] = ReceivingDataAccordingToJSON(JSON=self.JSON_meterdata.get(deviceidx),
                                                                Select_all=True).get_result()
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
    def _get_CheckUP(self):
        """
        Здесь по отдельности проверяем снятые показания с каждого счетчика отдельно

        :return:
        """
        result = []

        # ТЕПЕРЬ - Каждый Device IDx проверяем отдельно - Це важно

        for DeviceIdx in self.DeviceIdx_list:

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
        self.JSON_Meter_Dev = []
        self.list_measure = []

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

        # И после чего ищем что записанно по факту

        self.database_was_recording = self._get_DataBase_was_recording_in_fact(
            data_base_after_recording=data_base_after_recording,
            data_base_before_recording=data_base_before_recording)

        # # print('database_was_recording', self.database_was_recording)
        # # print('JSON_meterdata_deconstruct', self.JSON_meterdata_deconstruct)
        result = self._get_CheckUP()

        print(result)
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
                       count_meter: int = 2,):
        """
        Здесь содержиться Тесты для УЖЕ заполненой БД - Заполняется только ОДИН таймштамп
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

        print(result)
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
#
# MeterDaemon_result = MeterDaemon('ssh').RealMeter(list_measure=['ElMomentEnergy'],
#                                                                   MeterConfig=[])
# print(MeterDaemon_result)


# # ------------------------------------------- ОДИН СЧЕТЧИК --------------------------------------------------------
deleteMeterTable()
sleep(1)

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


result = MeterDaemonManyMeter(type_connect='ssh').DataBase_clear(list_measure=['ElMomentEnergy'], count_meter=10)
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
