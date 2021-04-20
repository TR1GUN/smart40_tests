# Здесь расположим тест для проверки поля records  и других проверок дял компонента базы данных
from working_directory.Template.Template_Meter_db_data_API.Template_checkup_from_Meter_db_data_API import POSTCheckUP
# Либа для формирования JSON запроса
from working_directory.Template.Template_MeterJSON.Template_generate_meter_data_JSON import GeneratorJSON
from working_directory.Template.Template_MeterJSON.Template_Deconstruct import DeconstructJSON
from working_directory.Template.Template_Meter_db_data_API.Template_record_value_to_database import \
    RecordValueToDataBase

from working_directory.Template.Template_Setup import Setup

from working_directory.Template.Template_Meter_db_data_API.Template_read_handler_table import \
    ReceivingDataAccordingToJSON
from working_directory.Connect.JSON_format_coding_decoding import code_JSON

import time
from working_directory.log import log
from time import sleep
from working_directory.sqlite import deleteMeterTable
from working_directory.Template.Template_Meter_daemon.Daemon_settings import ArchInfo_settings


# from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
# ArchTypes_full_list = \
#     Template_list_ArchTypes.JournalValues_ArchType_name_list + \
#     Template_list_ArchTypes.DigitalValues_ArchType_name_list + \
#     Template_list_ArchTypes.PulseValues_ArchType_name_list + \
#     Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list + \
#     Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list + \
#     Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list + \
#     Template_list_ArchTypes.DigitalConfig_ArchType_name_list + \
#     Template_list_ArchTypes.PulseConfig_ArchType_name_list + \
#     Template_list_ArchTypes.ElectricConfig_ArchType_name_list
#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                              Основной класс от которого наследуемся
# -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################

class Service:
    """Основной класс наследуясь от которого реализуем наши дополнительные проверки"""
    type_connect: str = 'virtualbox'
    API = ''
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
#                           КЛАСС ДЛЯ ПРОВЕРКИ РАБОТЫ ПОЛЯ РЕКОРДС
# -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################
class ArchInfo(Service):
    """
    Класс для Проверки работы поля Records в таблице ArchInfo
    """

    type_connect: str = 'virtualbox'
    API = 'meter_db_data_api'
    JSON = {}
    answer_JSON = {}
    ArchType_Name = ''

    def __init__(self, type_connect: str = 'virtualbox'):
        self.type_connect = type_connect

    # ----------------------------------------------------------------------------------------------
    #                                   Вспомомгательные методы
    # -----------------------------------------------------------------------------------------------
    # ---------------------------   ПРОВЕРКА УСПЕШНОСТИ ОПЕРАЦИИ  -----------------------------------
    def __error_handler(self, answer_JSON):
        if answer_JSON['res'] != 0:
            result = [{'error': 'Ошибка в полученном JSON', 'JSON': self.JSON, 'answer_JSON': answer_JSON}]
        else:
            result = []

        return result

    # -------------------------------   Логирование ОШИБКИ  -----------------------------------------
    def __write_log(self, result):
        if len(result) > 0:
            result = log(API_name=' ArchInfo - Records ' + str(self.ArchType_Name),
                         Error=result,
                         JSON=self.JSON,
                         answer_JSON=self.answer_JSON,
                         JSON_normal={'БД': ''})
        return result

    # ------------------ Генерируем заведомо Плохие таймштампы  -------------------------------------

    def __generate_incorrect_timestamp(self, Count_records):
        """Здесь генерируем не коректные таймштампы для заведомо плохой записи"""
        from working_directory.Template.Template_MeterJSON.Template_generator_random_timestamp import GeneratorTimestamp

        class GeneratorTime(GeneratorTimestamp):
            finis = 1400000000
            start = 1300000000
        Generator = GeneratorTime
        Timestamp = Generator(count_ts=Count_records).Timestamp
        return Timestamp

    # -----------------------------------------------------------------------------------------------
    # ----------------------- Редактор наших полей  ArchInfo Под стоковое значение --------------------
    def _rewrite_ArchInfo(self, count):
        '''
        Редактор наших полей  ArchInfo Под нужное значение
        :return:
        '''

        from working_directory.Template.Template_Meter_daemon.Template_ReWrite_field_Records import ReWriteFieldRecords

        record = ReWriteFieldRecords(measure=self.ArchType_Name,
                                     count_records=count)

        return record

    # ---------------------------- Получение Нашего локального айпишника ---------------------------------------------

    def RecordsCheckUp(self, ArchType_Name: str, Count_records: int):
        """
        Этот Метод нужен для проверки Коректности обработки значений в поле  Records
        :param ArchType_Name:
        :return:
        """

        # Переопределяем Методы
        self.ArchType_Name = ArchType_Name

        # Первое что делаем - Чистим всю БД
        deleteMeterTable()

        sleep(2)
        # После мы берем и редачим нашу Талицу ЗНАЧЕНИЯМИ ПО УМОЛЧАНИЮ
        record = self._rewrite_ArchInfo(count=ArchInfo_settings.get(ArchType_Name))

        # ТЕПЕРЬ МЕНЯЕМ НА НУЖНОЕ ЗНАЧЕНИЕ
        record = self._rewrite_ArchInfo(count=Count_records)

        # ГЕНЕРИРУЕМ НАШИ ДАННЫЕ , которые запишем в таблицу
        Generator = GeneratorJSON(measure=[ArchType_Name],
                                  count_ts=self.__generate_incorrect_timestamp(Count_records=Count_records),
                                  count_id=1,
                                  Castrom_Value={})
        # Получаем данные - голый скелет
        skeleton_JSON = Generator.JSON

        # И наш JSON
        JSON_dict_record = Generator.Generator_JSON_for_Meter_data_POST()

        # Теперь получаем деконструированный JSON

        JSON_deconstruct = DeconstructJSON(JSON=JSON_dict_record).JSON_deconstruct

        # print('То что записали', JSON_deconstruct)

        # после этого - записываем
        RecordValueToDataBase(JSON_deconstruct=JSON_deconstruct)

        # Вытаскиваем айдишник
        DeviceIdx = [JSON_deconstruct[0][0]['id']]

        # Вызываем нужный генератор - Генерирукем данные

        Generator = GeneratorJSON(measure=[ArchType_Name],
                                  count_ts=Count_records,
                                  count_id=DeviceIdx,
                                  Castrom_Value={})
        # Получаем данные - голый скелет
        skeleton_JSON = Generator.JSON

        # И наш JSON
        self.JSON_dict = Generator.Generator_JSON_for_Meter_data_POST()

        # Теперь получаем деконструированный JSON
        JSON_deconstruct = DeconstructJSON(JSON=self.JSON_dict).JSON_deconstruct

        # Селектим БД до записи
        data_base_before_recording = ReceivingDataAccordingToJSON(JSON=self.JSON_dict, Select_all=True).get_result()


        # print('БД до отправки' ,data_base_before_recording )
        # Теперь Запускаем наш JSON
        AnswerJSON = self.Setup()

        # Обрабатываем ошибки самого JSON
        result = self.__error_handler(answer_JSON=AnswerJSON)


        # Если ошибок нет , то запускаем наш сравниватель
        if len(result) == 0:
            # селектим БД после записи


            data_base_after_recording = ReceivingDataAccordingToJSON(JSON=self.JSON_dict, Select_all=True).get_result()

            # И селектим в БД только записи что мы сделали

            data_base_was_recorded = ReceivingDataAccordingToJSON(JSON=self.JSON_dict, Select_all=False).get_result()

            # print('data_base_was_recorded', data_base_was_recorded)
            # print('data_base_after_recording', data_base_after_recording)
            # print('JSON_deconstruct', JSON_deconstruct)
            result = POSTCheckUP(DataBase_before=data_base_before_recording,
                                 DataBase_after=data_base_after_recording,
                                 DataBase_was_recording=data_base_was_recorded,
                                 JSON_deconstruct=JSON_deconstruct).error_collector

            result = self.__write_log(result)

        # возвращаем в наше исходное ссотояние
        record = self._rewrite_ArchInfo(count=ArchInfo_settings.get(ArchType_Name))

        return result

#####################################################################################################################
# -------------------------------------------------------------------------------------------------------------------
#                                               Тестовые Запуски
# -------------------------------------------------------------------------------------------------------------------
#####################################################################################################################


# -----------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------
# #
# lol = ArchInfo().RecordsCheckUp(ArchType_Name='ElArr1ConsPower', Count_records=3)
# #
# print(lol)
