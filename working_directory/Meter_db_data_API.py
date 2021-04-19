# Здесь расположены тесты для нашей апишеки meter_db_data_api

from working_directory.Template.Template_Meter_db_data_API.Template_checkup_from_Meter_db_data_API import \
    GETCheckUP, \
    POSTCheckUP
# Либа для формирования JSON запроса
from working_directory.Template.Template_MeterJSON.Template_generate_meter_data_JSON import GeneratorJSON
from working_directory.Template.Template_MeterJSON.Template_Deconstruct import DeconstructJSON
from working_directory.Template.Template_Meter_db_data_API.Template_record_value_to_database import \
    RecordValueToDataBase

from working_directory.Template.Template_Setup import Setup

from working_directory.Template.Template_Meter_db_data_API.Template_read_handler_table import \
    ReceivingDataAccordingToJSON
from working_directory.Connect.JSON_format_coding_decoding import decode_JSON, code_JSON

from working_directory.Template.Template_Meter_db_data_API.Template_parse_answer_JSON import ParseAnswerMeterDataJSON
import time, datetime
from working_directory.log import log

import threading


# # -------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------
#                       Делаем основной класс - От которого будем наследоваться
#                                     В него внесем общие методы
# -------------------------------------------------------------------------------------------------------------------


class MeterData:
    """Класс для работы с Компонентом MeterData"""

    type_connect: str = 'virtualbox'
    API = 'meter_db_data_api'
    JSON = {}
    answer_JSON = {}
    JSON_dict = {}

    def Setup(self):
        """МЕТОД ЗАПУСКА JSON"""

        self.JSON = code_JSON(self.JSON_dict)
        # для измерения времени работы API ставим таймер
        time_start = time.time()
        # Сделаем запуск через ДОКЕР
        JSON_Setup = Setup(JSON=self.JSON, API=self.API, type_connect=self.type_connect)
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


#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                                                   GET
# -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################
class GET(MeterData):
    """
            Класс для работы с методом GET компонента Meter Data API
    """

    type_connect: str = 'virtualbox'
    API = 'meter_db_data_api'
    JSON = {}
    answer_JSON = {}

    def __init__(self, type_connect: str = 'virtualbox'):
        self.type_connect = type_connect

    # ----------------------------------------------------------------------------------------------
    #                                   Вспомомгательные методы
    # -----------------------------------------------------------------------------------------------
    # ---------------------------   ПРОВЕРКА УСПЕШНОСТИ ОПЕРАЦИИ  -----------------------------------
    def _error_handler(self, answer_JSON):
        if answer_JSON.get('res') != 0:
            result = [{'error': 'Ошибка в полученном JSON', 'JSON': self.JSON, 'answer_JSON': answer_JSON}]
        else:
            result = []

        return result

    # -------------------------------   Логирование ОШИБКИ  -----------------------------------------
    def _write_log(self, result):
        if len(result) > 0:
            result = log(API_name='Meter db data API - POST - ' + str(self.list_measure),
                         Error=result,
                         JSON=self.JSON,
                         answer_JSON=self.answer_JSON,
                         JSON_normal={'БД': ''})
        return result

    # -----------------------------------------------------------------------------------------------
    # Еcли мы отправляем массив данных :
    def Сustom_measures(self,
                        #
                        list_measure: list = ['ElConfig'],
                        # Количество отрезков времени , которые запрашиваем
                        select_count_ts: int = 1,
                        # Количество Id которые запрашиваем
                        select_count_id: int = 3,
                        # Количество отрезков времени , которые генерируем
                        generate_count_ts: int = 1,
                        # Количество Id которые генерируем
                        generate_count_id: int = 3,
                        # Количество тэгов или список тэгов которые попадут в JSON
                        count_tags: int or list = 2,
                        # Маркер селекта по device_idx - внутрений айдишник
                        select_device_idx: bool = True,
                        # Маркер селекта по meter_id - внешний айдишник
                        select_meter_id: bool = True,
                        # Маркер селекта всего что есть. Взаимоисключающий с select_meter_id, select_device_idx и serial
                        select_id_all: bool = False,
                        # Маркер селекта последнего времени. Взаимоисключающий с select_count_ts и out_of_bounds
                        select_last_time: bool = False,
                        # Маркер выхода за границы существующего времени - Важен для настройки лимита времени
                        out_of_bounds: bool = False,
                        # Маркер селекта по serial - серийный номер в config
                        serial: bool = True,
                        # Тэги которые надо переопределить
                        tags: dict = {}):
        # Включаем обработчик
        result = []
        self.list_measure = list_measure

        Generator = GeneratorJSON(measure=list_measure,
                                  count_ts=generate_count_ts,
                                  count_id=generate_count_id,
                                  Castrom_Value=tags)
        # Получаем данные - голый скелет
        skeleton_JSON = Generator.JSON

        # И наш JSON
        JSON_dict_record = Generator.Generator_JSON_for_Meter_data_POST()

        # Теперь получаем деконструированный JSON

        JSON_deconstruct = DeconstructJSON(JSON=JSON_dict_record).JSON_deconstruct
        # после этого - записываем

        RecordValueToDataBase(JSON_deconstruct=JSON_deconstruct)

        # После чего генерируем JSON запроса
        self.JSON_dict = Generator.Generator_JSON_for_Meter_data_GET(
            count_tags=count_tags,
            select_device_idx=select_device_idx,
            select_meter_id=select_meter_id,
            select_id_all=select_id_all,
            select_last_time=select_last_time,
            out_of_bounds=out_of_bounds,
            serial=serial,
            select_count_ts=select_count_ts,
            select_count_id=select_count_id)

        # print('JSON_dict_record', JSON_dict_record)
        # Теперь получаем данные из БД что записали
        select_for_JSON_to_database = ReceivingDataAccordingToJSON(JSON=self.JSON_dict, Select_all=False).get_result()

        # Теперь Запускаем наш JSON
        AnswerJSON = self.Setup()

        # Обрабатываем ошибки самого JSON
        result = self._error_handler(answer_JSON=AnswerJSON)

        # Если ошибок нет , то запускаем наш сравниватель
        if len(result) == 0:
            # Теперь деконструируем JSON для сравнения с БД
            answer_JSON_deconstruct = ParseAnswerMeterDataJSON(JSON=AnswerJSON).JSON_deconstruct
            # Теперь пихаем это в сравниватель
            result = GETCheckUP(JSON_deconstruct=answer_JSON_deconstruct,
                                DataBase_select=select_for_JSON_to_database).error_collector
            # Логируем
            result = self._write_log(result)
        #
        return result


#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                                                   POST
# -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################

class POST(MeterData):
    """
        Класс для работы с методом POST компонента Meter Data API
    """
    type_connect: str = 'virtualbox'
    API = 'meter_db_data_api'
    JSON = {}
    answer_JSON = {}

    def __init__(self, type_connect: str = 'virtualbox'):
        self.type_connect = type_connect

    # ----------------------------------------------------------------------------------------------
    #                                   Вспомомгательные методы
    # -----------------------------------------------------------------------------------------------

    # ---------------------------   ПРОВЕРКА УСПЕШНОСТИ ОПЕРАЦИИ  -----------------------------------
    def _error_handler(self, answer_JSON):
        if answer_JSON['res'] != 0:
            result = [{'error': 'Ошибка в полученном JSON', 'JSON': self.JSON, 'answer_JSON': answer_JSON}]
        else:
            result = []

        return result

    # -------------------------------   Логирование ОШИБКИ  -----------------------------------------
    def _write_log(self, result):
        if len(result) > 0:
            result = log(API_name='Meter db data API - POST - ' + str(self.list_measure),
                         Error=result,
                         JSON=self.JSON,
                         answer_JSON=self.answer_JSON,
                         JSON_normal={'БД': ''})
        return result

    # -----------------------------------------------------------------------------------------------
    # Еcли мы отправляем массив данных :
    def Сustom_measures(self,
                        # НАШ СПИСОК ТИПОВ ДАННЫХ
                        list_measure: list = ['ElConfig'],
                        # Количество Времени которое мы генерируем
                        count_ts: int = 1,
                        # Количество айдишников которые мы генерируем
                        count_id: int = 3,
                        # Тэги которые надо переопределить
                        tags: dict = {}
                        ):
        """
        Основной метод запуска POST запроса к MeterData
        Работает в один Поток

        :param list_measure:  # НАШ СПИСОК ТИПОВ ДАННЫХ
        :param count_ts:    # Количество Времени которое мы генерируем
        :param count_id:    # Количество айдишников которые мы генерируем
        :param tags:                # Тэги которые надо переопределить
        :return:
        """

        self.list_measure = list_measure
        # Вызываем нужный генератор - Генерирукем данные

        Generator = GeneratorJSON(measure=list_measure,
                                  count_ts=count_ts,
                                  count_id=count_id,
                                  Castrom_Value=tags)
        # Получаем данные - голый скелет
        skeleton_JSON = Generator.JSON

        # И наш JSON
        self.JSON_dict = Generator.Generator_JSON_for_Meter_data_POST()

        # Теперь получаем деконструированный JSON
        JSON_deconstruct = DeconstructJSON(JSON=self.JSON_dict).JSON_deconstruct

        # Селектим БД до записи
        data_base_before_recording = ReceivingDataAccordingToJSON(JSON=self.JSON_dict, Select_all=True).get_result()

        # Теперь Запускаем наш JSON
        AnswerJSON = self.Setup()

        # Обрабатываем ошибки самого JSON
        result = self._error_handler(answer_JSON=AnswerJSON)

        # Если ошибок нет , то запускаем наш сравниватель
        if len(result) == 0:
            # селектим БД после записи
            data_base_after_recording = ReceivingDataAccordingToJSON(JSON=self.JSON_dict, Select_all=True).get_result()

            # И селектим в БД только записи что мы сделали

            data_base_was_recorded = ReceivingDataAccordingToJSON(JSON=self.JSON_dict, Select_all=False).get_result()

            print(result)

            result = POSTCheckUP(DataBase_before=data_base_before_recording,
                                 DataBase_after=data_base_after_recording,
                                 DataBase_was_recording=data_base_was_recorded,
                                 JSON_deconstruct=JSON_deconstruct).error_collector

            result = self._write_log(result)

        return result


#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                                                   МНОГОПОТОЧНЫЙ POST
# -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################

class ThreadingPOST(POST):
    JSON_dict = {}
    JSON_deconstruct = {}
    data_base_before_recording = {}
    data_base_was_recorded = {}
    data_base_after_recording = {}
    JSON = {}
    answer_JSON = {}
    thread = 2
    setup_JSON = False

    # -----------------------------МЕТОД ЗАПУСКА - ЕГО ПЕРЕОПРЕДЕЛЯЕМ ОТ БАЗОВОГО ------------------------------------
    def Setup(self, JSON, index):
        """МЕТОД ЗАПУСКА JSON"""

        while True:
            if self.setup_JSON:
                JSON_Setup = Setup(JSON=JSON, API=self.API, type_connect=self.type_connect)
                answer_JSON = JSON_Setup.answer_JSON
                # Добавляем по индексу - Имени потока
                self.answer_JSON[index] = answer_JSON

                # # ----------ПРИНТУЕМ---------------
                # print('JSON Обрабабатывался:', time_finis - time_start)
                # # Навсякий случай печатаем JSON ответа и что отправляли
                # print('JSON\n', self.JSON)
                # print('answer_JSON\n', self.answer_JSON)
                # # ---------------------------------

                # И сбрамываем
                break

    # -----------------------------МЕТОД для многопоточности - Он свой  ------------------------------------
    def __Setup_JSON(self):

        # Сначала формируем наши JSON
        self.JSON = {}
        for i in range(self.thread):
            self.JSON['thread_' + str(i)] = code_JSON(self.JSON_dict['thread_' + str(i)])
        # для измерения времени работы API ставим таймер
        time_start = time.time()
        # Сделаем запуск ПОТОКОВ
        Thread_dict = {}
        self.answer_JSON = {}
        self.setup_JSON = False
        for i in range(self.thread):
            # Создаем поток
            Thread_dict['thread_' + str(i)] = threading.Thread(target=self.Setup,
                                                               args=(
                                                                   self.JSON['thread_' + str(i)],
                                                                   str('thread_' + str(i)),))
            # Запускаем его
            Thread_dict['thread_' + str(i)].start()
        self.setup_JSON = True

        time.sleep(10)

        for i in range(self.thread):
            # Запускаем его
            Thread_dict['thread_' + str(i)].join()
        # Получаем время
        time_finis = time.time()

        # # ----------ПРИНТУЕМ---------------
        # print('JSON Обрабабатывался:', time_finis - time_start)
        # # Навсякий случай печатаем JSON ответа и что отправляли
        # print('JSON\n', self.JSON)
        # print('answer_JSON\n', self.answer_JSON)
        # # ---------------------------------
        return self.answer_JSON

    # ---------------------------   ПРОВЕРКА УСПЕШНОСТИ ОПЕРАЦИИ - Только для потоков ----------------------------
    def __error_handler_thread(self):

        result = []
        for keys in self.answer_JSON:
            result_thread = self._error_handler(answer_JSON=self.answer_JSON[keys])
            if len(result_thread) > 0:
                result.append(result_thread)

        return result

    # -------------------------------   Логирование ОШИБКИ  -----------------------------------------

    # Сдесь сделаем однавременный запуск нескольких потоков , чоб нет.
    def Сustom_measures(self,
                        # НАШ СПИСОК ТИПОВ ДАННЫХ
                        list_measure: list = ['ElConfig'],
                        # Количество Времени которое мы генерируем
                        count_ts: int = 1,
                        # Количество айдишников которые мы генерируем
                        count_id: int = 3,
                        # Тэги которые надо переопределить
                        tags: dict = {},
                        # Количество потоков - ЭТО ВАЖНО
                        thread: int = 2
                        ):
        """
        Функция для многопоточного запуска


        :param list_measure:
        :param count_ts:
        :param count_id:
        :param tags:
        :param thread:
        :return:
        """
        self.list_measure = list_measure
        self.thread = thread
        # Пункт первый - Генерируем соответсвующие число JSON на запись
        self.JSON_dict = {}
        self.JSON_deconstruct = {}
        self.data_base_before_recording = {}
        self.data_base_was_recorded = {}
        self.data_base_after_recording = {}
        # Вызываем нужный генератор - Генерирукем данные

        for i in range(thread):
            Generator = GeneratorJSON(measure=list_measure,
                                      count_ts=count_ts,
                                      count_id=count_id,
                                      Castrom_Value=tags)
            # Получаем данные - голый скелет
            skeleton_JSON = Generator.JSON

            # И наш JSON
            self.JSON_dict['thread_' + str(i)] = Generator.Generator_JSON_for_Meter_data_POST()
            # Теперь получаем деконструированный JSON
            self.JSON_deconstruct['thread_' + str(i)] = DeconstructJSON(
                JSON=self.JSON_dict['thread_' + str(i)]).JSON_deconstruct
            # Селектим БД до записи
            self.data_base_before_recording['thread_' + str(i)] = ReceivingDataAccordingToJSON(
                JSON=self.JSON_dict['thread_' + str(i)], Select_all=True).get_result()

        # Запускаем
        self.answer_JSON = self.__Setup_JSON()

        print('\n\n=================', self.answer_JSON)

        # Теперь имеем наш ответ - и теперь начинаем его проверять

        # Обрабатываем ошибки самого JSON
        result = self.__error_handler_thread()

        # Если ошибок нет , то запускаем наш сравниватель
        if len(result) == 0:
            # селектим БД после записи

            for i in range(thread):
                self.data_base_after_recording['thread_' + str(i)] = ReceivingDataAccordingToJSON(
                    JSON=self.JSON_dict['thread_' + str(i)], Select_all=True).get_result()

            # И селектим в БД только записи что мы сделали
            for i in range(thread):
                self.data_base_was_recorded['thread_' + str(i)] = ReceivingDataAccordingToJSON(
                    JSON=self.JSON_dict['thread_' + str(i)], Select_all=False).get_result()

            # А Теперь - Сравниваем

            for i in range(thread):
                name_thread = 'thread_' + str(i)

                result_thread = POSTCheckUP(DataBase_before=self.data_base_before_recording[name_thread],
                                            DataBase_after=self.data_base_after_recording[name_thread],
                                            DataBase_was_recording=self.data_base_was_recorded[name_thread],
                                            JSON_deconstruct=self.JSON_deconstruct[name_thread]).error_collector
                if len(result) != 0:
                    result.append({'ОШИБКА В потоке ' + name_thread: result_thread})

            result = self._write_log(result)

        return result


#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                                                МНОГОПОТОЧНЫЙ GET
# -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################
class ThreadingGET(GET):
    JSON_dict = {}
    JSON_deconstruct = {}
    JSON_dict_record = {}
    select_for_JSON_to_database = {}
    answer_JSON_deconstruct = {}
    JSON = {}
    answer_JSON = {}
    thread = 2
    setup_JSON = False

    # ---------------------------   ПРОВЕРКА УСПЕШНОСТИ ОПЕРАЦИИ - Только для потоков ----------------------------
    def __error_handler_thread(self):

        result = []
        for keys in self.answer_JSON:
            result_thread = self._error_handler(answer_JSON=self.answer_JSON[keys])
            if len(result_thread) > 0:
                result.append(result_thread)

        return result

    # -----------------------------МЕТОД ЗАПУСКА - ЕГО ПЕРЕОПРЕДЕЛЯЕМ ОТ БАЗОВОГО ------------------------------------
    def Setup(self, JSON, index):
        """МЕТОД ЗАПУСКА JSON"""

        while True:
            if self.setup_JSON:
                JSON_Setup = Setup(JSON=JSON, API=self.API, type_connect=self.type_connect)
                answer_JSON = JSON_Setup.answer_JSON
                # Добавляем по индексу - Имени потока
                self.answer_JSON[index] = answer_JSON

                # # ----------ПРИНТУЕМ---------------
                # print('JSON Обрабабатывался:', time_finis - time_start)
                # # Навсякий случай печатаем JSON ответа и что отправляли
                # print('JSON\n', self.JSON)
                # print('answer_JSON\n', self.answer_JSON)
                # # ---------------------------------

                # И сбрамываем
                break

    # -----------------------------МЕТОД для многопоточности - Он свой  ------------------------------------
    def __Setup_JSON(self):

        # Сначала формируем наши JSON
        self.JSON = {}
        for i in range(self.thread):
            self.JSON['thread_' + str(i)] = code_JSON(self.JSON_dict['thread_' + str(i)])
        # для измерения времени работы API ставим таймер
        time_start = time.time()
        # Сделаем запуск ПОТОКОВ
        Thread_dict = {}
        self.answer_JSON = {}
        self.setup_JSON = False
        for i in range(self.thread):
            # Создаем поток
            Thread_dict['thread_' + str(i)] = threading.Thread(target=self.Setup,
                                                               args=(
                                                                   self.JSON['thread_' + str(i)],
                                                                   str('thread_' + str(i)),))
            # Запускаем его
            Thread_dict['thread_' + str(i)].start()
        self.setup_JSON = True

        time.sleep(10)

        for i in range(self.thread):
            # Запускаем его
            Thread_dict['thread_' + str(i)].join()
        # Получаем время
        time_finis = time.time()

        return self.answer_JSON

    # ---------------------------   ПРОВЕРКА УСПЕШНОСТИ ОПЕРАЦИИ - Только для потоков ----------------------------

# -----------------------------------------------------------------------------------------------
    # Еcли мы отправляем массив данных :
    def Сustom_measures(self,
                        #
                        list_measure: list = ['ElConfig'],
                        # Количество отрезков времени , которые запрашиваем
                        select_count_ts: int = 1,
                        # Количество Id которые запрашиваем
                        select_count_id: int = 3,
                        # Количество отрезков времени , которые генерируем
                        generate_count_ts: int = 1,
                        # Количество Id которые генерируем
                        generate_count_id: int = 3,
                        # Количество тэгов или список тэгов которые попадут в JSON
                        count_tags: int or list = 2,
                        # Маркер селекта по device_idx - внутрений айдишник
                        select_device_idx: bool = True,
                        # Маркер селекта по meter_id - внешний айдишник
                        select_meter_id: bool = True,
                        # Маркер селекта всего что есть. Взаимоисключающий с select_meter_id, select_device_idx и serial
                        select_id_all: bool = False,
                        # Маркер селекта последнего времени. Взаимоисключающий с select_count_ts и out_of_bounds
                        select_last_time: bool = False,
                        # Маркер выхода за границы существующего времени - Важен для настройки лимита времени
                        out_of_bounds: bool = False,
                        # Маркер селекта по serial - серийный номер в config
                        serial: bool = True,
                        # Тэги которые надо переопределить
                        tags: dict = {},
                        # Количество потоков - ЭТО ВАЖНО
                        thread: int = 2

                        ):
        # Включаем обработчик
        result = []
        self.list_measure = list_measure
        self.thread = thread


        self.JSON_dict_record = {}
        self.select_for_JSON_to_database = {}
        self.AnswerJSON = {}
        self.answer_JSON_deconstruct = {}
        # Вызываем нужный генератор - Генерирукем данные

        for i in range(thread):
            Generator = GeneratorJSON(measure=list_measure,
                                      count_ts=generate_count_ts,
                                      count_id=generate_count_id,
                                      Castrom_Value=tags)
            # Получаем данные - голый скелет
            skeleton_JSON = Generator.JSON

            # И наш JSON
            self.JSON_dict_record['thread_' + str(i)] = Generator.Generator_JSON_for_Meter_data_POST()
            # Теперь получаем деконструированный JSON
            self.JSON_deconstruct['thread_' + str(i)] = DeconstructJSON(
                                                                        JSON=self.JSON_dict_record['thread_' + str(i)]
                                                                        ).JSON_deconstruct

            RecordValueToDataBase(JSON_deconstruct=self.JSON_deconstruct['thread_' + str(i)])

            # После чего генерируем JSON запроса
            self.JSON_dict['thread_' + str(i)] = Generator.Generator_JSON_for_Meter_data_GET(
                count_tags=count_tags,
                select_device_idx=select_device_idx,
                select_meter_id=select_meter_id,
                select_id_all=select_id_all,
                select_last_time=select_last_time,
                out_of_bounds=out_of_bounds,
                serial=serial,
                select_count_ts=select_count_ts,
                select_count_id=select_count_id)


            # Теперь получаем данные из БД что записали
            self.select_for_JSON_to_database['thread_' + str(i)] = ReceivingDataAccordingToJSON(
                                                                       JSON=self.JSON_dict['thread_' + str(i)],
                                                                       Select_all=False).get_result()

        # Теперь Запускаем наш JSON
        self.AnswerJSON = self.__Setup_JSON()



        # Обрабатываем ошибки самого JSON
        result = self.__error_handler_thread()

        # Если ошибок нет , то запускаем наш сравниватель
        if len(result) == 0:
            # Теперь деконструируем JSON для сравнения с БД
            for i in range(thread):
                self.answer_JSON_deconstruct['thread_' + str(i)] = ParseAnswerMeterDataJSON(JSON=self.AnswerJSON['thread_' + str(i)]).JSON_deconstruct

            for i in range(thread):
                name_thread = 'thread_' + str(i)

                result_thread = GETCheckUP(JSON_deconstruct=self.answer_JSON_deconstruct[name_thread],
                                            DataBase_select=self.select_for_JSON_to_database[name_thread]).error_collector
                if len(result_thread) != 0:
                    result.append({'ОШИБКА В потоке ' + name_thread: result_thread})

            result = self._write_log(result)

        return result

# # -------------------------------------------------------------------------------------------------------------------
# Сделаем список из всех возможных ArchType
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes

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
# # -------------------------------------------------------------------------------------------------------------------
import sys
sys.coinit_flags = 0

import pythoncom
        # Сразу перед инициализацией DCOM в run()
pythoncom.CoInitializeEx(0)


# Чистим таблицу
from time import sleep
from working_directory.sqlite import deleteMeterTable

deleteMeterTable()
sleep(2)

# # -------------------------------------------------------------------------------------------------------------------
#
# meterdata = POST(type_connect='ssh').Сustom_measures(
#     list_measure=['PlsMomentPulse'],
#     count_id=1, count_ts=2,
#     tags={'serial':None, 'model':None, 'cArrays':None, 'isDst':None, 'isClock':None, 'isTrf':None,
#             'isAm':None, 'isRm':None, 'isRp':None, 'kI':None, 'kU':None, 'const':None
#          }
# )


ElMomentQuality = {
    'UA': None, 'IA': None, 'PA': None, 'QA': None, 'SA': None, 'kPA': None, 'AngAB': None,
    'UB': None, 'IB': None, 'PB': None, 'QB': None, 'SB': None, 'kPB': None, 'AngBC': None,
    'UC': None, 'IC': None, 'PC': None, 'QC': None, 'SC': None, 'kPC': None, 'AngAC': None,
    'PS': None, 'QS': None, 'SS': None, 'kPS': None, 'Freq': None,
}

ElMomentEnergy = {
    'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
    'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
    'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
    'A+3': None, 'A-3': None, 'R+3': None, 'R-3': None,
    'A+4': None, 'A-4': None, 'R+4': None, 'R-4': None,
}

ElArr1ConsPower = {
    'cTime': None, 'P+': None, 'Q+': None, 'P-': None, 'Q-': None, 'isPart': None, 'isOvfl': None, 'isSummer': None
}

PlsMomentPulse = {'Pls1': None, 'Pls2': None, 'Pls3': None, 'Pls4': None, 'Pls5': None, 'Pls6': None, 'Pls7': None,
                  'Pls8': None, 'Pls9': None, 'Pls10': None, 'Pls11': None, 'Pls12': None,
                  'Pls13': None, 'Pls14': None, 'Pls15': None, 'Pls16': None, 'Pls17': None, 'Pls18': None,
                  'Pls19': None, 'Pls20': None, 'Pls21': None, 'Pls22': None, 'Pls23': None,
                  'Pls24': None, 'Pls25': None, 'Pls26': None, 'Pls27': None, 'Pls28': None, 'Pls29': None,
                  'Pls30': None, 'Pls31': None, 'Pls32': None}

DigMomentState = {'Chnl1': None, 'Chnl2': None, 'Chnl3': None, 'Chnl4': None, 'Chnl5': None, 'Chnl6': None,
                  'Chnl7': None, 'Chnl8': None, 'Chnl9': None,
                  'Chnl10': None,
                  'Chnl11': None, 'Chnl12': None, 'Chnl13': None, 'Chnl14': None, 'Chnl15': None, 'Chnl16': None,
                  'Chnl17': None, 'Chnl18': None,
                  'Chnl19': None, 'Chnl20': None,
                  'Chnl21': None, 'Chnl22': None, 'Chnl23': None, 'Chnl24': None, 'Chnl25': None, 'Chnl26': None,
                  'Chnl27': None, 'Chnl28': None,
                  'Chnl29': None, 'Chnl30': None,
                  'Chnl31': None, 'Chnl32': None, }

ElConfig = {'serial': None, 'model': None, 'cArrays': None, 'isDst': None, 'isClock': None, 'isTrf': None,
            'isAm': None, 'isRm': None, 'isRp': None, 'kI': None, 'kU': None, 'const': None}

Journal = {'event': None, 'eventId': None, }
# print(meterdata)

# -------------------------------------------------------------------------------------------------------------------
# meterdata = GET(type_connect='virtualbox').Сustom_measures(list_measure=['ElArr1ConsPower'],
#                                                            select_count_ts=2,
#                                                            select_count_id=2,
#                                                            generate_count_ts=3,
#                                                            generate_count_id=3,
#                                                            count_tags=0,
#                                                            select_device_idx=False,
#                                                            select_meter_id=True,
#                                                            serial=False,
#                                                            select_id_all=False,
#                                                            select_last_time=True,
#                                                            out_of_bounds=True)
#
# print(meterdata)

# ['PlsConfig'], select_count_ts = 2, select_count_id = 2, generate_count_ts = 3, generate_count_id = 3, count_tags = 0, select_device_idx = False, select_meter_id = True, serial = False
# select_id_all = False, select_last_time = True, out_of_bounds = True
# # -------------------------------------------------------------------------------------------------------------------
#
meterdata = ThreadingPOST(type_connect='ssh').Сustom_measures(
    list_measure=['PlsMomentPulse'],
    count_id=1, count_ts=2,
    tags={'serial': None, 'model': None, 'cArrays': None, 'isDst': None, 'isClock': None, 'isTrf': None,
          'isAm': None, 'isRm': None, 'isRp': None, 'kI': None, 'kU': None, 'const': None
          }, thread=2

)
#
# meterdata = ThreadingGET(type_connect='virtualbox').Сustom_measures(list_measure=['ElArr1ConsPower'],
#                                                            select_count_ts=2,
#                                                            select_count_id=2,
#                                                            generate_count_ts=3,
#                                                            generate_count_id=3,
#                                                            count_tags=0,
#                                                            select_device_idx=False,
#                                                            select_meter_id=True,
#                                                            serial=False,
#                                                            select_id_all=False,
#                                                            select_last_time=True,
#                                                            out_of_bounds=True,
#                                                                     thread=2)
#
# print(meterdata)