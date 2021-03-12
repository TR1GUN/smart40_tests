# Здесь расположены тесты для нашей апишеки meter_db_data_api

from working_directory.Template.Template_Meter_db_data_API.Template_checkup_from_Meter_db_data_API import CheckUP, \
    GETCheckUP

# Либа для формирования JSON запроса

from working_directory.Template.Template_Setup import Setup
from working_directory.Template.Template_Meter_db_data_API.Template_generator_measures import GeneratorMeasures
from working_directory.Template.Template_Meter_db_data_API import JSON_for_Meter_db_data_API, Template_list_ArchTypes
from working_directory.Template.Template_Meter_db_data_API.Template_read_handler_table import \
    ReceivingDataAccordingToJSON, RecordDataToDB
from working_directory.Connect.JSON_format_coding_decoding import decode_JSON, code_JSON
from working_directory.Template.Template_Meter_db_data_API.Template_generator_get_by_meansures import \
    GeneratorGetRequest, DeleteAddedConfig

from working_directory.Template.Template_Meter_db_data_API.Template_parse_answer_JSON import ParseAnswerMeterDataJSON
import time, write_file
from working_directory.log import log

# ----------------------------------------------------------------------------------------------------------------------
#                                                   GET
# ----------------------------------------------------------------------------------------------------------------------
class GET:
    """
            Класс для работы с методом GET
    """

    type_connect: str = 'virtualbox'

    def __init__(self, type_connect: str = 'virtualbox'):
        name_table = ""
        self.type_connect = type_connect

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
                        serial: bool = True):
        # Включаем обработчик
        result = []
        self.list_measure = list_measure

        # Проверяем что количество генераций не есть меньше колличества селектов  - в этом случае у насм все хорошо
        if select_count_id > generate_count_id:
            result.append({'error': 'Не правильно задано количество генераций'})

        # теперь очень важный момент - если мы селектим по серийнику , то  генерируем и серийник для них
        added_config = False
        if serial:

            # Проверяем - задан ли конфиг, если не задан , то все хорошо

            if (Template_list_ArchTypes.ElectricConfig_ArchType_name_list[0] not in list_measure) and \
                    (Template_list_ArchTypes.PulseConfig_ArchType_name_list[0] not in list_measure) and \
                    (Template_list_ArchTypes.DigitalConfig_ArchType_name_list[0] not in list_measure):
                # Теперь надо приписать нужный конфиг и сделаем и сделаем это через множества
                # Теперь формируем на всякий случай лист из всех электрических конфигов
                full_elconfig = Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list + Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list + \
                                Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list + Template_list_ArchTypes.JournalValues_ArchType_name_list
                # Если есть импульсные значения - то добавляем конфиг

                # Поскольку тут все грустно - ставим заглушку на El config
                if len(set(list_measure) & set(Template_list_ArchTypes.PulseValues_ArchType_name_list)) > 0:
                    # list_measure = list_measure + PulseConfig_ArchType_name_list
                    list_measure = list_measure + Template_list_ArchTypes.ElectricConfig_ArchType_name_list
                # Если есть диджитал значения - то добавляем конфиг
                if len(set(list_measure) & set(Template_list_ArchTypes.DigitalValues_ArchType_name_list)) > 0:
                    # list_measure = list_measure + DigitalConfig_ArchType_name_list
                    list_measure = list_measure + Template_list_ArchTypes.ElectricConfig_ArchType_name_list
                # Если есть электрик значения - то добавляем конфиг
                if len(set(list_measure) & set(full_elconfig)) > 0:
                    list_measure = list_measure + Template_list_ArchTypes.ElectricConfig_ArchType_name_list
                added_config = True

        if len(result) == 0:
            # Теперь надо сформировать тестовые данные
            generate = GeneratorMeasures()
            generate_measures = generate.get_parametrize_measure(list_measure=list_measure,
                                                                 count_ts=generate_count_ts,
                                                                 count_id=generate_count_id,
                                                                 generate_unicale_id=False,
                                                                 generate_unicale_ts=True
                                                                 )

            # первое что делаем - добавляем необходимые данные в БД все это в нашу БД:
            # сначала получаем их
            generate_measures_list_for_write_in_database = generate.get_deconstruct_json_dict()



            # после этого - записываем
            RecordDataToDB(data=generate_measures_list_for_write_in_database)

            # Отправляем все это в общий обработчик
            return self.__Meter_db_data_GET_execution_control(result=result,
                                                              JSON_generate=generate_measures,
                                                              select_count_ts=select_count_ts,
                                                              select_count_id=select_count_id,
                                                              count_tags=count_tags,
                                                              select_device_idx=select_device_idx,
                                                              select_meter_id=select_meter_id,
                                                              select_id_all=select_id_all,
                                                              select_last_time=select_last_time,
                                                              out_of_bounds=out_of_bounds,
                                                              serial=serial,
                                                              added_config=added_config)

    def __Meter_db_data_GET_execution_control(self,
                                              result: list,
                                              #
                                              JSON_generate,
                                              # Количество отрезков времени , которые запрашиваем
                                              select_count_ts: int = 1,
                                              # Количество Id которые запрашиваем
                                              select_count_id: int = 3,
                                              # Количество тэгов или список тэгов которые попадут в JSON
                                              count_tags: int or list = 2,
                                              # Маркер селекта по device_idx - внутрений айдишник
                                              select_device_idx: bool = True,
                                              # Маркер селекта по meter_id - внешний айдишник
                                              select_meter_id: bool = True,
                                              # Маркер селекта всего что есть. Взаимоисключающий с select_meter_id,
                                              # select_device_idx и serial
                                              select_id_all: bool = False,
                                              # Маркер селекта последнего времени. Взаимоисключающий с
                                              # select_count_ts и out_of_bounds
                                              select_last_time: bool = False,
                                              # Маркер выхода за границы существующего времени - Важен для настройки
                                              # лимита времени
                                              out_of_bounds: bool = False,
                                              # Маркер селекта по serial - серийный номер в config
                                              serial: bool = False,
                                              added_config: bool = False):

        # основная функция которая будет все что надо делать

        # Удаляем лишние конфиги , пока не поздно
        JSON_generate = DeleteAddedConfig(JSON=JSON_generate, added_config=added_config).JSON

        # После чего генерируем JSON запроса
        JSON_generate = GeneratorGetRequest(JSON=JSON_generate,
                                            count_tags=count_tags,
                                            select_device_idx=select_device_idx,
                                            select_meter_id=select_meter_id,
                                            select_id_all=select_id_all,
                                            select_last_time=select_last_time,
                                            out_of_bounds=out_of_bounds,
                                            serial=serial,
                                            select_count_ts=select_count_ts,
                                            select_count_id=select_count_id).JSON

        JSON_collector = JSON_for_Meter_db_data_API.GET(measures=JSON_generate)
        JSON = JSON_collector.JSON

        # Теперь получаем данные из БД
        JSON_dict = JSON_collector.JSON_dict
        select_db = ReceivingDataAccordingToJSON(JSON=JSON_dict, Select_all=False)
        select_for_JSON_to_database = select_db.get_result()
        # Замереем время
        time_start = time.time()
        # Теперь его отправляем на нужную нам в космос

        # Сделаем запуск
        JSON_Setup = Setup(JSON=JSON, API='meter_db_data_api', type_connect= self.type_connect)
        answer_JSON = JSON_Setup.answer_JSON


        print('JSON' , JSON)
        print('answer_JSON', answer_JSON)
        # Получаем время
        time_finis = time.time()

        print('JSON Обрабабатывался:', time_finis - time_start)


        # Навсякий случай печатаем JSON ответа и что отправляли
        # print('JSON\n', JSON)
        print('answer_JSON\n', answer_JSON)
        # Теперь пихаем это все в обработчик ошибок
        if answer_JSON['res'] != 0:
            result.append({'error': 'Ошибка в полученном JSON', 'JSON': JSON, 'answer_JSON': answer_JSON})
        else:

            # Теперь деконструируем JSON для сравнения с БД
            answer_JSON_deconstruct = ParseAnswerMeterDataJSON(JSON=answer_JSON).JSON_deconstruct

            # Теперь пихаем это в сравниватель
            result = GETCheckUP(JSON_deconstruct=answer_JSON_deconstruct,
                                DataBase_select=select_for_JSON_to_database).error_collector

            # Если ошибка найдена , то лучше записываем это все в файл
            if len(result) > 0:

                result = log(API_name='Meter db data API - GET - ' + str(self.list_measure),
                             Error=result,
                             JSON=JSON,
                             answer_JSON=answer_JSON,
                             JSON_normal=None)

        return result


# ----------------------------------------------------------------------------------------------------------------------
#                                                   POST
# ----------------------------------------------------------------------------------------------------------------------
class POST:
    """
        Класс для работы с методом POST
    """
    type_connect: str = 'virtualbox'

    def __init__(self, type_connect: str = 'virtualbox'):
        self.type_connect = type_connect

    # Делаем общий обработчик что дальше делать с JSON
    def __Meter_db_data_POST_execution_control(self, measures, JSON_for_compare_to_data_base: list):
        # Теперь что делаем - формируем окончательный JSON
        JSON = JSON_for_Meter_db_data_API.POST().collector(measures=measures)

        JSON_dict = decode_JSON(JSON)
        # Селектим БД до записи
        select_db = ReceivingDataAccordingToJSON(JSON=JSON_dict, Select_all=True)

        data_base_before_recording = select_db.get_result()
        # Замереем время
        time_start = time.time()
        # # Теперь его отправляем на нужную нам в космос
        # JSON_Setup = Setup(JSON)
        # answer_JSON = JSON_Setup.answer_JSON

        # Сделаем запуск через ДОКЕР
        JSON_Setup = Setup(JSON=JSON, API='meter_db_data_api', type_connect=self.type_connect)
        answer_JSON = JSON_Setup.answer_JSON

        # Получаем время
        time_finis = time.time()
        print('JSON Обрабабатывался:', time_finis - time_start)
        # Навсякий случай печатаем JSON ответа и что отправляли
        print('JSON\n', JSON)
        print('answer_JSON\n', answer_JSON)

        # Теперь пихаем это все в обработчик ошибок
        if answer_JSON['res'] != 0:
            result = [{'error': 'Ошибка в полученном JSON', 'JSON': JSON, 'answer_JSON': answer_JSON}]
        else:

            # Теперь селектим БД после записи
            select_db = ReceivingDataAccordingToJSON(JSON=JSON_dict, Select_all=True)
            data_base_after_recording = select_db.get_result()

            # И селектим в БД только записи что мы сделали

            print('JSON_dict' , JSON_dict)

            select_db = ReceivingDataAccordingToJSON(JSON=JSON_dict, Select_all=False)
            data_base_was_recorded = select_db.get_result()


            print('JSON_for_compare_to_data_base' , JSON_for_compare_to_data_base)
            # Теперь пихаем это все в обработчик
            result = CheckUP().checkup_post(database_before=data_base_before_recording,
                                            database_after=data_base_after_recording,
                                            database_was_recording=data_base_was_recorded,
                                            json_content=JSON_for_compare_to_data_base)

            if len(result) > 0:
                result = log(API_name='Meter db data API - POST - ' + str(self.list_measure),
                             Error=result,
                             JSON=JSON,
                             answer_JSON=answer_JSON,
                             JSON_normal=None)
        return result

    # Еcли мы отправляем массив данных :
    def Сustom_measures(self, list_measure: list = ['ElConfig'], count_ts: int = 1, count_id: int = 3,
                        generate_unicale_id: bool = True, generate_unicale_ts: bool = True):
        self.list_measure = list_measure
        # Вызываем нужный генератор -
        generate = GeneratorMeasures()
        generate_measures = generate.get_parametrize_measure(list_measure=list_measure,
                                                             count_ts=count_ts,
                                                             count_id=count_id,
                                                             generate_unicale_id=generate_unicale_id,
                                                             generate_unicale_ts=generate_unicale_ts
                                                             )
        # Получаем наш JSON Который будет с кушать обработчик
        JSON_for_compare_to_data_base = generate.get_deconstruct_json_dict()

        result = self.__Meter_db_data_POST_execution_control(measures=generate_measures,
                                                             JSON_for_compare_to_data_base=JSON_for_compare_to_data_base)
        # После того как все это произошло вызываем общую функцию, которая следит что да как


        return result

    # Генирируемый случайно :
    def Random_generate_measures(self, count_measure: int = 59, count_ts: int = 1, count_id: int = 1,
                                 generate_unicale_id: bool = True, generate_unicale_ts: bool = True):

        self.list_measure = 'random'
        # Вызываем нужный генератор -
        generate = GeneratorMeasures()
        generate_measures = generate.get_all_measure(count_measure=count_measure,
                                                     count_ts=count_ts,
                                                     count_id=count_id,
                                                     generate_unicale_id=generate_unicale_id,
                                                     generate_unicale_ts=generate_unicale_ts
                                                     )

        # Получаем наш JSON Который будет с кушать обработчик
        JSON_for_compare_to_data_base = generate.get_deconstruct_json_dict()

        result = self.__Meter_db_data_POST_execution_control(measures=generate_measures,
                                                             JSON_for_compare_to_data_base=JSON_for_compare_to_data_base)
        # После того как все это произошло вызываем общую функцию, которая следит что да как

        return result

# -------------------------------------------------------------------------------------------------------------------

meterdata = POST(type_connect='virtualbox').Сustom_measures(list_measure=['ElConfig','ElMomentEnergy', 'ElMomentQuality'] , count_id=2,count_ts=3 )

print(meterdata)