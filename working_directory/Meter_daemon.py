# Итак здесь расположим наш тест для демона опроса ПУ
from working_directory.Template.Template_Meter_daemon.Template_generator_JSON_for_mosquitto import \
    GenerateForMosquittoJSON
# from working_directory.Template.Template_Meter_db_data_API.Template_parse_answer_JSON import ParseAnswerMeterDataJSON
from working_directory.Template.Template_Meter_daemon.Template_assembly_normal_JSON_like_POST_meter_Data import \
    AssemblyDictLikeMeterData, RecordFromEmulatorMeter, DecostructMeterDataJSONForDaemon
from working_directory.Connect.JSON_format_coding_decoding import code_JSON
from working_directory.Template.Template_Meter_devices_API.Template_answer_json import GenerateAnswer
from working_directory.Template.Template_Meter_db_data_API.Template_read_handler_table import \
    ReceivingDataAccordingToJSON
from working_directory.Template.Template_Meter_db_data_API.Template_checkup_from_Meter_db_data_API import CheckUP
from working_directory.Template.Template_Setup import Setup
import datetime
import threading
import time


class MeterDaemon:
    '''
    Этот класс преднозначен для тестирования демона опроса ПУ
    '''
    API = 'uspd-meter_daemon'
    type_connect = 'virtualbox'
    error = None
    port = 7777

    def __init__(self, type_connect: str = 'virtualbox'):
        self.type_connect = type_connect

    # ---------------------------- Вспомомгательные методы ---------------------------------------------------

    def __GetIPConfig(self):
        """
        Получаем наш Айпишник - нужен для того чтоб сделать

        :return:
        """

        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", self.port))
        socket_name = (s.getsockname()[0])
        s.close()
        return socket_name + ':' + str(self.port)

    # def __setup_VirtualMeter(self):
    #     """ В Этом методе реализовываем наш виртуальный счетчик """
    #
    #
    #     # для начала генерируем JSON который мы ожидаем
    #     # Для начала формируем  JSON, с которого будем считывать
    #     job_type = self.job_type[0]
    #
    #     Answer = GenerateAnswer(job=job_type)
    #     # Берем сам JSON
    #     JSON_answer_normal = Answer.JSON
    #
    #     print('-----------JSON_answer_normal', JSON_answer_normal)
    #
    #     return JSON_answer_normal

    def __setup_VirtualMeter(self):
        """ В Этом методе реализовываем наш виртуальный счетчик """

        # для начала генерируем JSON который мы ожидаем
        # Для начала формируем  JSON, с которого будем считывать
        job_type = self.job_type
        JSON_answer_normal_list = []
        # Теперь что делаем - по очереди генерируем наши JSON для счетчика
        for i in range(len(job_type)):
            Answer = GenerateAnswer(job=job_type[i]).JSON
            # Берем сам JSON

            print('lololol',Answer)
            JSON_answer_normal_list.append(Answer)

        return JSON_answer_normal_list

    # ---------------------------------------------------------------------------------------------------------------------
    def __EmulatorMeter(self):
        """В этом методе подымаем локальный серевер с нашим виртуальным счетчиком"""
        from working_directory.Template.Template_Meter_devices_API.Template_socket_in_meters import SocketMeters

        print('Запустили')

        # Получаем наш список типов данных данных
        self.Emulator = SocketMeters(conect_port=self.port)

        # После удаляем обьект
        del self.Emulator
        print('УБИЛИ')

    # ---------------------------------------------------------------------------------------------------------------------
    #                                     Основная ФУНКЦИЯ ЗАПУСКА
    # ---------------------------------------------------------------------------------------------------------------------

    def VirtualMeter(self,
                     job_type: list = ['ElConfig', "ElMomentEnergy", 'ElArr1ConsPower'],
                     # Количество добавляемых записей
                     generate_count: int = 1,
                     # Количество элементов в дереве подключения
                     count_tree: int = 2,
                     # тип конекта
                     iface: str = 'Ethernet',
                     # Имя счетчика - Берется из БД
                     type_meter: str = 'SE303',
                     # Серийник нашего счетчика
                     address_meter: str = "141227285",
                     # Первичный Адресс счетчика\Хаба
                     adress: str = "192.168.202.146:7777",
                     # uart_tag
                     InterfaceConfig: str = "9600,8n1"):
        # переопределяем тэги

        self.job_type = job_type
        self.generate_count = generate_count
        self.count_tree = count_tree
        self.iface = iface
        self.type_meter = type_meter
        self.address_meter = address_meter
        self.adress = adress
        self.InterfaceConfig = InterfaceConfig

        # Получаем порт

        # Запускаем наш генератор данных
        JSON_answer_normal_meterdev = self.__setup_VirtualMeter()
        # Записываем данные для счетчика
        Record_JSON = RecordFromEmulatorMeter(JSON_answer_normal_meterdev)

        # Генерируем нашу запись в MeterTable и Получаем айдишники


        # ГЕНИРИРУЕМ НАШУ ЗАДАЧУ
        JSON_dict = GenerateForMosquittoJSON(
            job_type=self.job_type,
            generate_count=self.generate_count,
            count_tree=self.count_tree,
            type_connect=self.iface,
            type_meter=self.type_meter,
            address_meter=self.address_meter,
            adress=self.adress,
            InterfaceConfig=self.InterfaceConfig
        )

        DeviceIdx = JSON_dict.DeviceIdx_list
        JSON_dict = JSON_dict.jobs

        # Достраиваем JSON до уровня meter data
        JSON_dict_meterdata = AssemblyDictLikeMeterData(JSON_answer_normal_meterdev, DeviceIdx).JSON
        # Селектим БД до записи
        data_base_before_recording = ReceivingDataAccordingToJSON(JSON=JSON_dict_meterdata,
                                                                  Select_all=True).get_result()
        # Теперь Это все конфертируем в JSON
        JSON = code_JSON(JSON_dict)

        # print(JSON)

        # # Теперь запускаем имитатор отдельным потоком
        server = threading.Thread(target=self.__EmulatorMeter)
        server.start()
        #
        # Теперь что делаем - Теперь запускаем наш сформированный JSON в в мененеджер задааний
        # А Теперь очень важный момент - Смотрим какой способ запуска выбираем
        JSON_Setup = Setup(JSON=JSON, API=self.API, type_connect=self.type_connect)
        # Получаем Ответ
        answer_JSON = JSON_Setup.answer_JSON

        # После чего объеденяем потоки

        server.join()

        # Теперь - Надо Понять что все записалось в нашу таблицу

        time.sleep(10)

        # Теперь селектим БД после записи
        data_base_after_recording = ReceivingDataAccordingToJSON(JSON=JSON_dict_meterdata, Select_all=True).get_result()


        # И селектим в БД только записи что мы сделали
        data_base_was_recorded = ReceivingDataAccordingToJSON(JSON=JSON_dict_meterdata, Select_all=False).get_result()



        print('data_base_before_recording\n' , data_base_before_recording)

        print('data_base_after_recording\n' , data_base_after_recording)

        print('data_base_was_recorded\n', data_base_was_recorded)


        # print()
        # JSON_dict_meterdata['res'] = 0
        # Теперь деконструируем JSON для сравнения с БД

        print(JSON_dict_meterdata)
        JSON_for_compare_to_data_base = DecostructMeterDataJSONForDaemon(JSON=JSON_dict_meterdata).JSON_deconstruct


        print('JSON_for_compare_to_data_base\n' , JSON_for_compare_to_data_base)

        # Теперь пихаем это все в обработчик
        result = CheckUP().checkup_post(database_before=data_base_before_recording,
                                        database_after=data_base_after_recording,
                                        database_was_recording=data_base_was_recorded,
                                        json_content=JSON_for_compare_to_data_base)

        print(result)




a = MeterDaemon().VirtualMeter(job_type=['ElConfig'])
# 'ElConfig','ElMomentEnergy', 'ElMomentQuality' , 'ElArr1ConsPower'