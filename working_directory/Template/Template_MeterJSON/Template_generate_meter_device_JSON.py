from working_directory.Template.Template_Meter_devices_API.Template_json_archtype_name import ArchTypesNameJSON
from working_directory.Template.Template_Meter_devices_API.Template_generate_Timestamp_list import GenerateTimestamp
from working_directory.Template.Template_Meter_devices_API.Template_generator_time import GeneratorTime


# # -----------------------------------------------------------------------------------------------------
#                             Наш великий и ужасный Генератор JSON
#                                       Теперь для Meter DEV
# # -----------------------------------------------------------------------------------------------------


class GeneratorJSON:
    '''
    Великий и Ужасный генератор JSON для всех возможных комбинаций METER DEV
    '''

    JSON = {}
    measure = ''
    count_timestamp_ElArr1ConsPower = 48 * 35

    def __init__(self, measure, count_timestamp=None):
        # ПЕРЕОПРЕДЕЛЯЕМ
        self.measure = measure

        # Первое - Генерируем рандомный отрезок времени по правилам
        # Сначала генерим отрезок времени который будем юзать -
        timestamp_of_request = GeneratorTime(measure=self.measure).time

        print('ONE -------->', timestamp_of_request)
        # Генерируем нужные ts лоя него
        Generate_Time = GenerateTimestamp(measure=self.measure, Time=timestamp_of_request, Count_timestamp=count_timestamp)
        # ДЕЛАЕМ НЕОБХОДИМЫЕ ПРАВКИ ДЛЯ ДЕМОНА
        # ЗДЕСЬ - ПОЛУЧАСОВКИ - НА 35 СУТОК
        Generate_Time.cTime = 30
        # ТЕПЕРЬ ЕСЛИ У НАС НЕ НУЛЕВОЕ
        Generate_Time.delta_half_hour = self.count_timestamp_ElArr1ConsPower
        # Generate_Time.delta_day = delta_day
        # Generate_Time.delta_month = delta_month
        # Generate_Time.delta_half_hour = delta_half_hour
        # Generate_Time.delta_hour = delta_hour
        # Generate_Time.delta_moment = delta_moment
        # Generate_Time.delta_Journal = delta_Journal

        timestamp_list = Generate_Time.Generate_Timestamp_list()
        print('TWO -------->', timestamp_list)
        # Делаем заготовку -

        # Генерируем JSON
        JSON_data = ArchTypesNameJSON(measure=self.measure, count_ts=timestamp_list).JSON

        # отдаем взад
        self.JSON = {
            'data': JSON_data,
            'res': 0
        }
