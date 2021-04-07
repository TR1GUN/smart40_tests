# Здесь расположены тесты для нашей апишеки meter_db_data_api

from working_directory.Template.Template_Meter_db_data_API.Template_checkup_from_Meter_db_data_API import CheckUP, \
    GETCheckUP, POSTCheckUP
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
import time
from working_directory.log import log


#
# # ----------------------------------------------------------------------------------------------------------------------
# #                                                   GET
# # ----------------------------------------------------------------------------------------------------------------------
# class GET:
#     """
#             Класс для работы с методом GET
#     """
#
#     type_connect: str = 'virtualbox'
#
#     def __init__(self, type_connect: str = 'virtualbox'):
#         name_table = ""
#         self.type_connect = type_connect
#
#     # Еcли мы отправляем массив данных :
#     def Сustom_measures(self,
#                         #
#                         list_measure: list = ['ElConfig'],
#                         # Количество отрезков времени , которые запрашиваем
#                         select_count_ts: int = 1,
#                         # Количество Id которые запрашиваем
#                         select_count_id: int = 3,
#                         # Количество отрезков времени , которые генерируем
#                         generate_count_ts: int = 1,
#                         # Количество Id которые генерируем
#                         generate_count_id: int = 3,
#                         # Количество тэгов или список тэгов которые попадут в JSON
#                         count_tags: int or list = 2,
#                         # Маркер селекта по device_idx - внутрений айдишник
#                         select_device_idx: bool = True,
#                         # Маркер селекта по meter_id - внешний айдишник
#                         select_meter_id: bool = True,
#                         # Маркер селекта всего что есть. Взаимоисключающий с select_meter_id, select_device_idx и serial
#                         select_id_all: bool = False,
#                         # Маркер селекта последнего времени. Взаимоисключающий с select_count_ts и out_of_bounds
#                         select_last_time: bool = False,
#                         # Маркер выхода за границы существующего времени - Важен для настройки лимита времени
#                         out_of_bounds: bool = False,
#                         # Маркер селекта по serial - серийный номер в config
#                         serial: bool = True):
#         # Включаем обработчик
#         result = []
#         self.list_measure = list_measure
#
#         # Проверяем что количество генераций не есть меньше колличества селектов  - в этом случае у насм все хорошо
#         if select_count_id > generate_count_id:
#             result.append({'error': 'Не правильно задано количество генераций'})
#
#         # теперь очень важный момент - если мы селектим по серийнику , то  генерируем и серийник для них
#         added_config = False
#         if serial:
#
#             # Проверяем - задан ли конфиг, если не задан , то все хорошо
#
#             if (Template_list_ArchTypes.ElectricConfig_ArchType_name_list[0] not in list_measure) and \
#                     (Template_list_ArchTypes.PulseConfig_ArchType_name_list[0] not in list_measure) and \
#                     (Template_list_ArchTypes.DigitalConfig_ArchType_name_list[0] not in list_measure):
#                 # Теперь надо приписать нужный конфиг и сделаем и сделаем это через множества
#                 # Теперь формируем на всякий случай лист из всех электрических конфигов
#                 full_elconfig = Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list + Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list + \
#                                 Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list + Template_list_ArchTypes.JournalValues_ArchType_name_list
#                 # Если есть импульсные значения - то добавляем конфиг
#
#                 # Поскольку тут все грустно - ставим заглушку на El config
#                 if len(set(list_measure) & set(Template_list_ArchTypes.PulseValues_ArchType_name_list)) > 0:
#                     # list_measure = list_measure + PulseConfig_ArchType_name_list
#                     list_measure = list_measure + Template_list_ArchTypes.ElectricConfig_ArchType_name_list
#                 # Если есть диджитал значения - то добавляем конфиг
#                 if len(set(list_measure) & set(Template_list_ArchTypes.DigitalValues_ArchType_name_list)) > 0:
#                     # list_measure = list_measure + DigitalConfig_ArchType_name_list
#                     list_measure = list_measure + Template_list_ArchTypes.ElectricConfig_ArchType_name_list
#                 # Если есть электрик значения - то добавляем конфиг
#                 if len(set(list_measure) & set(full_elconfig)) > 0:
#                     list_measure = list_measure + Template_list_ArchTypes.ElectricConfig_ArchType_name_list
#                 added_config = True
#
#         if len(result) == 0:
#             # Теперь надо сформировать тестовые данные
#             generate = GeneratorMeasures()
#             generate_measures = generate.get_parametrize_measure(list_measure=list_measure,
#                                                                  count_ts=generate_count_ts,
#                                                                  count_id=generate_count_id,
#                                                                  generate_unicale_id=False,
#                                                                  generate_unicale_ts=True
#                                                                  )
#
#             # первое что делаем - добавляем необходимые данные в БД все это в нашу БД:
#             # сначала получаем их
#             generate_measures_list_for_write_in_database = generate.get_deconstruct_json_dict()
#
#             # после этого - записываем
#             RecordDataToDB(data=generate_measures_list_for_write_in_database)
#
#             # Отправляем все это в общий обработчик
#             return self.__Meter_db_data_GET_execution_control(result=result,
#                                                               JSON_generate=generate_measures,
#                                                               select_count_ts=select_count_ts,
#                                                               select_count_id=select_count_id,
#                                                               count_tags=count_tags,
#                                                               select_device_idx=select_device_idx,
#                                                               select_meter_id=select_meter_id,
#                                                               select_id_all=select_id_all,
#                                                               select_last_time=select_last_time,
#                                                               out_of_bounds=out_of_bounds,
#                                                               serial=serial,
#                                                               added_config=added_config)
#
#     def __Meter_db_data_GET_execution_control(self,
#                                               result: list,
#                                               #
#                                               JSON_generate,
#                                               # Количество отрезков времени , которые запрашиваем
#                                               select_count_ts: int = 1,
#                                               # Количество Id которые запрашиваем
#                                               select_count_id: int = 3,
#                                               # Количество тэгов или список тэгов которые попадут в JSON
#                                               count_tags: int or list = 2,
#                                               # Маркер селекта по device_idx - внутрений айдишник
#                                               select_device_idx: bool = True,
#                                               # Маркер селекта по meter_id - внешний айдишник
#                                               select_meter_id: bool = True,
#                                               # Маркер селекта всего что есть. Взаимоисключающий с select_meter_id,
#                                               # select_device_idx и serial
#                                               select_id_all: bool = False,
#                                               # Маркер селекта последнего времени. Взаимоисключающий с
#                                               # select_count_ts и out_of_bounds
#                                               select_last_time: bool = False,
#                                               # Маркер выхода за границы существующего времени - Важен для настройки
#                                               # лимита времени
#                                               out_of_bounds: bool = False,
#                                               # Маркер селекта по serial - серийный номер в config
#                                               serial: bool = False,
#                                               added_config: bool = False):
#
#         # основная функция которая будет все что надо делать
#
#         # Удаляем лишние конфиги , пока не поздно
#         JSON_generate = DeleteAddedConfig(JSON=JSON_generate, added_config=added_config).JSON
#
#         # После чего генерируем JSON запроса
#         JSON_generate = GeneratorGetRequest(JSON=JSON_generate,
#                                             count_tags=count_tags,
#                                             select_device_idx=select_device_idx,
#                                             select_meter_id=select_meter_id,
#                                             select_id_all=select_id_all,
#                                             select_last_time=select_last_time,
#                                             out_of_bounds=out_of_bounds,
#                                             serial=serial,
#                                             select_count_ts=select_count_ts,
#                                             select_count_id=select_count_id).JSON
#
#         JSON_collector = JSON_for_Meter_db_data_API.GET(measures=JSON_generate)
#         JSON = JSON_collector.JSON
#
#         # Теперь получаем данные из БД
#         JSON_dict = JSON_collector.JSON_dict
#         select_db = ReceivingDataAccordingToJSON(JSON=JSON_dict, Select_all=False)
#         select_for_JSON_to_database = select_db.get_result()
#         # Замереем время
#         time_start = time.time()
#         # Теперь его отправляем на нужную нам в космос
#
#         # Сделаем запуск
#         JSON_Setup = Setup(JSON=JSON, API='meter_db_data_api', type_connect=self.type_connect)
#         answer_JSON = JSON_Setup.answer_JSON
#
#         print('JSON', JSON)
#         print('answer_JSON', answer_JSON)
#         # Получаем время
#         time_finis = time.time()
#
#         print('JSON Обрабабатывался:', time_finis - time_start)
#
#         # Навсякий случай печатаем JSON ответа и что отправляли
#         # print('JSON\n', JSON)
#         print('answer_JSON\n', answer_JSON)
#         # Теперь пихаем это все в обработчик ошибок
#         if answer_JSON['res'] != 0:
#             result.append({'error': 'Ошибка в полученном JSON', 'JSON': JSON, 'answer_JSON': answer_JSON})
#         else:
#
#             # Теперь деконструируем JSON для сравнения с БД
#             answer_JSON_deconstruct = ParseAnswerMeterDataJSON(JSON=answer_JSON).JSON_deconstruct
#
#             # Теперь пихаем это в сравниватель
#             result = GETCheckUP(JSON_deconstruct=answer_JSON_deconstruct,
#                                 DataBase_select=select_for_JSON_to_database).error_collector
#
#             # Если ошибка найдена , то лучше записываем это все в файл
#             if len(result) > 0:
#                 result = log(API_name='Meter db data API - GET - ' + str(self.list_measure),
#                              Error=result,
#                              JSON=JSON,
#                              answer_JSON=answer_JSON,
#                              JSON_normal=None)
#
#         return result


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
    def __error_handler(self, answer_JSON):
        if answer_JSON['res'] != 0:
            result = [{'error': 'Ошибка в полученном JSON', 'JSON': self.JSON, 'answer_JSON': answer_JSON}]
        else:
            result = []

        return result

    # -------------------------------   Логирование ОШИБКИ  -----------------------------------------
    def __write_log(self, result):
        if len(result) > 0:
            result = log(API_name='Meter db data API - POST - ' + str(self.list_measure),
                         Error=result,
                         JSON=self.JSON,
                         answer_JSON=self.answer_JSON,
                         JSON_normal={'БД': ''})
        return result

    # -----------------------------------------------------------------------------------------------

    # -------------------------------- ПРОВЕРКА Количества генераций --------------------------------
    def __define_count_generation(self):
        pass
        # Проверяем что количество генераций не есть меньше колличества селектов  - в этом случае у насм все хорошо
        # if self.select_count_id > self.generate_count_id:
        # result.append({'error': 'Не правильно задано количество генераций'})

    # --------------------------- ПРОВЕРКА УСПЕШНОСТИ Здания параметров -----------------------------
    # def __added_config(self, serial):
    #     '''# Проверяем - задан ли конфиг, если не задан , то все хорошо'''
    #     list_measure = self.list_measure
    #
    #     added_config = False
    #
    #     if serial:
    #         # Проверяем - задан ли конфиг, если не задан , то все хорошо
    #
    #         if (Template_list_ArchTypes.ElectricConfig_ArchType_name_list[0] not in list_measure) and \
    #                 (Template_list_ArchTypes.PulseConfig_ArchType_name_list[0] not in list_measure) and \
    #                 (Template_list_ArchTypes.DigitalConfig_ArchType_name_list[0] not in list_measure):
    #             # Теперь надо приписать нужный конфиг и сделаем и сделаем это через множества
    #             # Теперь формируем на всякий случай лист из всех электрических конфигов
    #             full_elconfig = Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list + Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list + \
    #                             Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list + Template_list_ArchTypes.JournalValues_ArchType_name_list
    #             # Если есть импульсные значения - то добавляем конфиг
    #
    #             # Поскольку тут все грустно - ставим заглушку на El config
    #             if len(set(list_measure) & set(Template_list_ArchTypes.PulseValues_ArchType_name_list)) > 0:
    #                 # list_measure = list_measure + PulseConfig_ArchType_name_list
    #                 list_measure = list_measure + Template_list_ArchTypes.ElectricConfig_ArchType_name_list
    #             # Если есть диджитал значения - то добавляем конфиг
    #             if len(set(list_measure) & set(Template_list_ArchTypes.DigitalValues_ArchType_name_list)) > 0:
    #                 # list_measure = list_measure + DigitalConfig_ArchType_name_list
    #                 list_measure = list_measure + Template_list_ArchTypes.ElectricConfig_ArchType_name_list
    #             # Если есть электрик значения - то добавляем конфиг
    #             if len(set(list_measure) & set(full_elconfig)) > 0:
    #                 list_measure = list_measure + Template_list_ArchTypes.ElectricConfig_ArchType_name_list
    #             added_config = True

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

        print('JSON_dict_record', JSON_dict_record)
        # Теперь получаем данные из БД что записали
        select_for_JSON_to_database = ReceivingDataAccordingToJSON(JSON=self.JSON_dict, Select_all=False).get_result()

        # Теперь Запускаем наш JSON
        AnswerJSON = self.Setup()

        # Обрабатываем ошибки самого JSON
        result = self.__error_handler(answer_JSON=AnswerJSON)

        # Если ошибок нет , то запускаем наш сравниватель
        if len(result) == 0:
            # Теперь деконструируем JSON для сравнения с БД
            answer_JSON_deconstruct = ParseAnswerMeterDataJSON(JSON=AnswerJSON).JSON_deconstruct
            # Теперь пихаем это в сравниватель
            result = GETCheckUP(JSON_deconstruct=answer_JSON_deconstruct,
                                DataBase_select=select_for_JSON_to_database).error_collector
            # Логируем
            result = self.__write_log(result)
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
    def __error_handler(self, answer_JSON):
        if answer_JSON['res'] != 0:
            result = [{'error': 'Ошибка в полученном JSON', 'JSON': self.JSON, 'answer_JSON': answer_JSON}]
        else:
            result = []

        return result

    # -------------------------------   Логирование ОШИБКИ  -----------------------------------------
    def __write_log(self, result):
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
        result = self.__error_handler(answer_JSON=AnswerJSON)

        # Если ошибок нет , то запускаем наш сравниватель
        if len(result) == 0:
            # селектим БД после записи
            data_base_after_recording = ReceivingDataAccordingToJSON(JSON=self.JSON_dict, Select_all=True).get_result()


            # И селектим в БД только записи что мы сделали

            data_base_was_recorded = ReceivingDataAccordingToJSON(JSON=self.JSON_dict, Select_all=False).get_result()



            result = POSTCheckUP(DataBase_before=data_base_before_recording,
                                 DataBase_after=data_base_after_recording,
                                 DataBase_was_recording=data_base_was_recorded,
                                 JSON_deconstruct=JSON_deconstruct).error_collector

            result = self.__write_log(result)

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
#
# Чистим таблицу
from time import sleep
from working_directory.sqlite import deleteMeterTable

deleteMeterTable()
sleep(2)
# # -------------------------------------------------------------------------------------------------------------------

meterdata = POST(type_connect='virtualbox').Сustom_measures(
                                                            list_measure=['ElDayEnergy'],
                                                            count_id=1, count_ts=2,
                                                            tags={
                                                                  'A-0':None,'R+0':None,'R-0':None,'A+0':None,
                                                                  'A+1':None, 'A+2':None, 'A+3':None, 'A+4':None}
                                                            )

print(meterdata)

# -------------------------------------------------------------------------------------------------------------------
# meterdata = GET(type_connect='virtualbox').Сustom_measures(list_measure=['ElArr1ConsPower'],
#                                                            select_count_ts=4,
#                                                            select_count_id=4,
#                                                            generate_count_ts=4,
#                                                            generate_count_id=5,
#                                                            count_tags=3,
#                                                            select_device_idx=True,
#                                                            select_meter_id=False,
#                                                            serial=False,
#                                                            select_id_all=False,
#                                                            select_last_time=False,
#                                                            out_of_bounds=False)
#
# print(meterdata)
