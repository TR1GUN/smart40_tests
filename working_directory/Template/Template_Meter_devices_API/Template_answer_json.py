# Итак - здесь попытаемся генерировать JSON ответа
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from working_directory.Template.Template_Meter_devices_API import Template_list_job
from working_directory.Template.Template_Meter_devices_API.Template_json_archtype_name import ArchTypesNameJSON
from working_directory.Template.Template_Meter_devices_API.Template_generator_time import GeneratorTime


class GenerateAnswer:
    """
    Генервтор ответа JSON для апи
    """
    JSON = {}
    type_job = ''
    timestamp_of_request = None

    def __init__(self, job: str):
        # переопределяем переменные
        self.type_job = job

        # Сначала генерим отрезок времени который будем юзать -
        self.timestamp_of_request = GeneratorTime(measure=job).time[0]

        # Теперь смотрим - какой тип ответа будем генерировать
        self.JSON = self.__definition_type_answer()

    def __definition_type_answer(self):
        # Берем список всех типов переменных которые уже умеем генерировать
        full_archtype_name_list = \
            Template_list_ArchTypes.JournalValues_ArchType_name_list + \
            Template_list_ArchTypes.DigitalValues_ArchType_name_list + \
            Template_list_ArchTypes.PulseValues_ArchType_name_list + \
            Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list + \
            Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list + \
            Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list + \
            Template_list_ArchTypes.DigitalConfig_ArchType_name_list + \
            Template_list_ArchTypes.PulseConfig_ArchType_name_list + \
            Template_list_ArchTypes.ElectricConfig_ArchType_name_list
            # и добавляем запрос серийника
        full_archtype_name_list = full_archtype_name_list + Template_list_job.GetSerial_list

        # Берем список список всех типов переменых которые нужно реализовыывавть в этой апи
        full_set_job_list = \
            Template_list_job.SetRelay_list + \
            Template_list_job.SyncTime_list + \
            Template_list_job.SetTime_list

        type_measure = self.type_job
        # Ветка ветвления для full_archtype_name_list
        if type_measure in full_archtype_name_list:

            JSON_data = self.__generate_for_archtype_name()

        # Ветка ветвления для full_set_job_list
        elif type_measure in full_set_job_list:

            if type_measure == '':
                JSON_data = None
            else:
                JSON_data = None

        else:
            JSON_data = 'Unknown error code'

        JSON = self.wrapping_JSON(JSON_data=JSON_data)

        return JSON

    def wrapping_JSON(self, JSON_data):
        """
        Функция для оборачивания

        :param JSON_data: наш JSON который получаем на выходе
        :return: Возвращает нормальный JSON
        """
        JSON = {
            'data': JSON_data,
            'res': 0
        }

        return JSON

    def __generate_for_archtype_name(self):
        """
        Генерируем JSON для типов переменных которые есть в  archtype.name
        :return:
        """
        # Переопределяем переменые
        measure = self.type_job
        # Определяеем количество таймштампов для конкретного коллинечтва времени

        count_ts = self.timestamp_of_request
        # Делаем заготовку -

        # Генерируем JSON
        JSON_data = ArchTypesNameJSON(measure=measure, count_ts=count_ts).JSON

        return JSON_data
