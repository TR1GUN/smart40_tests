# Здесь прописываем Наши методы для Meter devices API, какие они должны быть

# Здесь расположим сборщик JSON из всех тех объектов что есть

import datetime
import threading
import time

from working_directory.Connect.JSON_format_coding_decoding import code_JSON
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from working_directory.Template.Template_Meter_devices_API import Template_list_job
from working_directory.Template.Template_Meter_devices_API.Template_answer_json import GenerateAnswer
from working_directory.Template.Template_Meter_devices_API.Template_error_handler import ErrorHeandler
from working_directory.Template.Template_Meter_devices_API.Template_generator_job import GeneratorJob
from working_directory.Template.Template_Setup import Setup
from working_directory.log import log


# Либа для формирования JSON запроса
#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                                                   КЛАСС РОДИТЕЛЬ
# -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################

class JOB:
    """
    КЛАСС ШАБЛОН ДЛЯ СВЯЗИ С НАШЕЙ АПИ
    """

    API = 'meterdev'
    type_connect = 'virtualbox'
    JSON = {}
    answer_JSON = {}
    JSON_answer_normal = {}
    JSON_dict = {}
    job_type = ''

    def Setup(self):
        """ Метод для запуска нашего JSON в Космос"""
        self.JSON = code_JSON(self.JSON_dict)

        # Замереем время
        time_start = time.time()

        JSON_Setup = Setup(JSON=self.JSON, API=self.API, type_connect=self.type_connect)
        # Получаем Ответ
        self.answer_JSON = JSON_Setup.answer_JSON

        # Получаем время
        time_finis = time.time()

        # ----------ПРИНТУЕМ---------------
        print('JSON Обрабабатывался:', time_finis - time_start)
        # Навсякий случай печатаем JSON ответа и что отправляли
        print('JSON\n', self.JSON)
        print('answer_JSON\n', self.answer_JSON)
        # ---------------------------------

        return self.answer_JSON

    # -------------------------------   Логирование ОШИБКИ  -----------------------------------------
    def write_log(self, result):
        """
        ЛОГИРУЕМ ОШИБКУ

        :param result:
        :return:
        """
        print(result)

        if len(result) > 0:
            result = log(API_name='Meter device API - ' + str(self.job_type),
                         Error=result,
                         JSON=self.JSON,
                         answer_JSON=self.answer_JSON,
                         JSON_normal={'JSON_answer_normal': self.JSON_answer_normal})
        return result


# ---------------------------------------------------------------------------------------------------------------------
#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                                             РЕАЛЬНЫЙ СЧЕТЧИК
# -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################
# ---------------------------------------------------------------------------------------------------------------------
class RealMeter(JOB):
    """
    Класс для работы с РЕАЛЬНЫМ счетчиком

    Здесь не производиться работа сравнивания значения счетчика. Только Валидация JSON ответа

    """
    error = None
    time_dict = {'set_castrom_time': False, "start": 0, "end": 0}

    # Итак - если задаем кастромное время , то надо указать промежуток - По умолчанию старт в 2017 - и конец сегодня
    def __init__(self, set_castrom_time: bool = False, start: int = 1506180007,
                 end: int = int(time.mktime(datetime.datetime.now().timetuple())), type_connect: str = 'virtualbox'):

        """
        Итак - если задаем кастромное время ,
        то надо указать промежуток - По умолчанию старт в 2017 - и конец сегодня

        :param set_castrom_time: Задаем кастрмное время - если да , то можно указать начало и конец
        :param start: Стартовое время - по умолчанию 2017 год
        :param end: Конечное время - По умолчанию - сегодня
        """
        self.error = []
        self.type_connect = type_connect
        if set_castrom_time:
            # ЕСЛИ ЗАДАНО КАСТРОМНОЕ ВРЕМЯ - ТО ЕСТЕСТВЕННО ПЕРЕОПРЕДЛЕЛЯЕМ ЕГО
            self.time_dict = {'set_castrom_time': True, "start": start, "end": end}

    # ----------------------------------------------------------------------------------------------------------------
    # -----------------------КАНАЛ ВЗАИМОДЕЙСТВИЯ - ПОСЛЕДОВАТЕЛЬНЫЙ ПОРТ---------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------

    def __iface_Serial_Port(self, job_type: str, iface: str = 'Iface3', type_connect: str = 'virtualbox',
                            address_settings: str = 'Iface3'):
        """
            Метод для работы с РЕАЛЬНЫМ СЧЕТЧИКОМ -
            Инерфейс подключения - Serial Port

            - НЕ РАБОТАЕТ

            РЕАЛИЗОВАННО :

            Работает только валидация JSON

            :param job_type:
            :param iface:
            :param docker:
            :return:
            """

        self.job_type = job_type
        self.type_connect = type_connect

        # Итак - сначала мы генерируем наш JSON
        self.JSON_dict = GeneratorJob(job=job_type,
                                      iface='Iface3',
                                      address_settings=address_settings,
                                      set_castrom_time=self.time_dict['set_castrom_time'],
                                      start=self.time_dict['start'],
                                      end=self.time_dict['end'],
                                      relay_state=True,
                                      count_time=1,
                                      generate_random_meter_type=False).job
        # Запускаем
        answer_JSON = self.Setup()

        # Ищем JSON  которые завершились с ошибкой
        if answer_JSON['res'] == 0:

            # Теперь опускаем в обработчик и деконструктор
            result = ErrorHeandler(JSON=answer_JSON, job_type=job_type)
        else:
            # ЕСли иначе то выводим номер ошобки и ее тип
            result = [answer_JSON]

        result = self.write_log(result=result)

        return result

    # ----------------------------------------------------------------------------------------------------------------
    # ---------------------------------КАНАЛ ВЗАИМОДЕЙСТВИЯ - ETHERNET -----------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------

    def iface_Ethernet(self, job_type: str, ipconfig: str = '192.168.205.6:2002', type_connect: str = 'virtualbox'):
        """
        Метод для работы с РЕАЛЬНЫМ СЧЕТЧИКОМ -
        Инерфейс подключения - Ethernet


        РЕАЛИЗОВАННО :

        Работает только валидация JSON

        :param job_type: Сюда пихаем ту переменную что хотим считать
        :param ipconfig: Сюда пихаем Те сетевое расположение счетчика. По умолчанию - Энергомера 303 со стенда
        :param docker: Нужно выставить TRUE для того чтоб провалиться во внутрь локально запущеного Docker-контейнера
        и пускать команду через docker exec

        :return: Возвращает пустоту

        """
        self.job_type = job_type
        self.type_connect = type_connect

        # Итак - сначала мы генерируем наш JSON
        self.JSON_dict = GeneratorJob(job=job_type,
                                      iface='Ethernet',
                                      address_settings=ipconfig,
                                      set_castrom_time=self.time_dict['set_castrom_time'],
                                      start=self.time_dict['start'],
                                      end=self.time_dict['end'],
                                      relay_state=True,
                                      count_time=1,
                                      generate_random_meter_type=False).job

        # Запускаем
        answer_JSON = self.Setup()

        # Ищем JSON  которые завершились с ошибкой
        if answer_JSON['res'] == 0:

            # Теперь опускаем в обработчик и деконструктор
            result = ErrorHeandler(JSON=answer_JSON, job_type=job_type)
            # Берем сборщик ошибок
            result = result.error_collector
        else:
            # ЕСли иначе то выводим номер ошобки и ее тип
            result = [answer_JSON]

        result = self.write_log(result=result)

        return result


# ---------------------------------------------------------------------------------------------------------------------
#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                                             ЭМУЛЯТОР СЧЕТЧИКА
# -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################
# ---------------------------------------------------------------------------------------------------------------------


class VirtualMeter(JOB):
    """
    Класс для работы с ВИРТУАЛЬНЫМ счетчиком

   Здесь расположим всю основную работу со счетчиком

    """
    error = None
    time = {'set_castrom_time': False, "start": 0, "end": 0}
    type_connect: str = 'virtualbox'
    port = 7777
    JSON_answer_normal = {}

    def __init__(self, type_connect: str = 'virtualbox'):
        self.error = []
        self.type_connect = type_connect

    # ---------------------------------------------------------------------------------------------------------------
    #                                      СЛУЖЕБНЫЕ МЕТОДЫ
    # ---------------------------------------------------------------------------------------------------------------

    def __EmulatorMeter(self):
        """В этом методе подымаем локальный серевер с нашим виртуальным счетчиком"""
        from working_directory.Template.Template_Meter_devices_API.Template_socket_in_meters import SocketMeters
        self.Emulator = SocketMeters(conect_port=self.port)

        # После удаляем обьект
        del self.Emulator

    def __GetIPConfig(self):
        """
        Получаем наши настройки конфигов, которые нужны для конфигов

        :return:
        """

        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", self.port))
        socket_name = (s.getsockname()[0])
        s.close()
        return socket_name + ':' + str(self.port)

    # ----------------------------------ЗАПИСЬ НАШИХ ЗНАЧЕНИЙ---------------------------------------------------------
    def __Save_values(self):
        """В ЭТОМ МЕТОДЕ ЗАПСИЫВАЕМ НАШ ОЖИДАЕНМЫЙ JSON в имитатор счетчика"""
        from working_directory.Template.Template_Meter_devices_API.Template_record_values_for_meter import \
            RecordFromEmulatorMeter
        from copy import deepcopy
        # ЗДЕСЬ -  ЗАПИСЫВАЕМ НАШ ЭТАЛОННЫЙ JSON в сам счетчик
        record = RecordFromEmulatorMeter(JSON_list=[deepcopy(self.JSON_answer_normal)])

    # ----------------------------------------------------------------------------------------------------------------
    # -----------------------КАНАЛ ВЗАИМОДЕЙСТВИЯ - ПОСЛЕДОВАТЕЛЬНЫЙ ПОРТ---------------------------------------------
    # ----------------------------------------------------------------------------------------------------------------

    def __iface_Serial_Port(self, job_type: str):
        # Для начала формируем  JSON
        JSON_dict = GeneratorJob(job=job_type, iface='Iface3', relay_state=True, count_time=1,
                                 generate_random_meter_type=False).job

        # Теперь это все упаковываем в JSON
        JSON = code_JSON(JSON_dict)
        # Теперь его отправляем на нужную нам в космос
        JSON_Setup = Setup(JSON)
        answer_JSON = JSON_Setup.answer_JSON

    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------КАНАЛ ВЗАИМОДЕЙСТВИЯ - ETHERNET ------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def iface_Ethernet(self, job_type: str, port: int = 7777):

        self.job_type = job_type
        self.port = port

        # Получаем наши конфиги
        ipconfig = self.__GetIPConfig()

        # Для начала формируем  JSON, с которого будем считывать
        Answer = GenerateAnswer(job=job_type)
        # Берем сам JSON

        self.JSON_answer_normal = Answer.JSON
        # И записываем его
        self.__Save_values()

        # Берем таймштампы
        timestamp_of_request = Answer.timestamp_of_request
        # Используем эти таймштампы
        self.time['set_castrom_time'] = True
        self.time['start'] = timestamp_of_request['start']
        self.time['end'] = timestamp_of_request['end']

        # print('JSON_answer_normal', JSON_answer_normal)

        # Итак - сначала мы генерируем наш JSON
        self.JSON_dict = GeneratorJob(job=job_type,
                                      iface='Ethernet',
                                      address_settings=ipconfig,
                                      set_castrom_time=self.time['set_castrom_time'],
                                      start=self.time['start'],
                                      end=self.time['end'],
                                      relay_state=True,
                                      count_time=1,
                                      generate_random_meter_type=False).job

        # Теперь запускаем имитатор отдельным потоком
        server = threading.Thread(target=self.__EmulatorMeter)
        server.start()

        # Немного ждем для инициализации
        time.sleep(2)
        # Отправляем ,  Получаем Ответ
        answer_JSON = self.Setup()
        # После того как получили ответ - убиваем наш процесс виртуального счетчика - Но не раньше чем закончиться обмен
        time.sleep(5)
        # После чего обьеденяем потоки
        server.join()
        # Ищем JSON  которые завершились с ошибкой

        # print('JSON_answer_normal\n', self.JSON_answer_normal)
        if answer_JSON['res'] == 0:
            # Теперь опускаем в обработчик и деконструктор
            result = ErrorHeandler(JSON=answer_JSON,
                                   job_type=job_type,
                                   JSON_answer_normal=self.JSON_answer_normal)
            # Берем сборщик ошибок
            result = result.error_collector
        else:
            # ЕСли иначе то выводим номер ошобки и ее тип
            result = [answer_JSON]

        result = self.write_log(result=result)

        return result


# ---------------------------------------------------------------------------------------------------------------------
#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                                               Тестовые данные
# -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################
# ---------------------------------------------------------------------------------------------------------------------
# Сделаем список из всех возможных ArchType

ArchTypes_full_list = \
    Template_list_ArchTypes.JournalValues_ArchType_name_list + \
    Template_list_ArchTypes.DigitalValues_ArchType_name_list + \
    Template_list_ArchTypes.PulseValues_ArchType_name_list + \
    Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list + \
    Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list + \
    Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list + \
    Template_list_ArchTypes.DigitalConfig_ArchType_name_list + \
    Template_list_ArchTypes.PulseConfig_ArchType_name_list + \
    Template_list_ArchTypes.ElectricConfig_ArchType_name_list

Set_job_list = Template_list_job.GetTime_list + \
               Template_list_job.SetTime_list + \
               Template_list_job.SyncTime_list + \
               Template_list_job.GetRelay_list + \
               Template_list_job.SetRelay_list + \
               Template_list_job.GetSerial_list

full = ArchTypes_full_list + Set_job_list

# ---------------------------------------------------------------------------------------------------------------------

JournalValues_list = [
    'ElJrnlPwr',
    'ElJrnlTimeCorr',
    'ElJrnlReset',
    'ElJrnlTrfCorr',
    'ElJrnlOpen',
    'ElJrnlUnAyth',
    'ElJrnlPwrA',
    'ElJrnlPwrB',
    'ElJrnlPwrC',
    'ElJrnlLimUAMax',
    'ElJrnlLimUAMin',
    'ElJrnlLimUBMax',
    'ElJrnlLimUBMin',
    'ElJrnlLimUCMax',
    'ElJrnlLimUCMin'
]
# ---------------------------------------------------------------------------------------------------------------------
#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                                         ТЕСТОВЫЕ ЗАПУСКИ
# -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################
# ---------------------------------------------------------------------------------------------------------------------


# test = VirtualMeter(type_connect='ssh').iface_Ethernet(job_type='ElJrnlTrfCorr')
# print(test)
