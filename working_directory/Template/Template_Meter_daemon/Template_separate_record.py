# Здесь напишем класс котоырй будет генерировать нужные данные в БД
from working_directory.Template.Template_Meter_db_data_API.Template_list_ArchTypes import \
    ElectricConfig_ArchType_name_list, PulseConfig_ArchType_name_list, DigitalConfig_ArchType_name_list, \
    ElectricQualityValues_ArchType_name_list

from datetime import datetime
import copy


# //-------------------------------------------------------------------------------------------------------------------
#                      РАЗДЕЛИТЕЛЬ JSON METER DEV на два - ЧТО ЗАПИСЫВАЕМ В СЧЕТЧИК и ЧТО в БД
# //-------------------------------------------------------------------------------------------------------------------

class SeparateJSONfromMeterDev:
    """
    В Этом классе разделяем наш сгенерированный JSON
    """
    JSON_record_for_data_base = []

    JSON_for_MeterDev = []

    JSON_original = []

    count_ts_to_record = 12

    def __init__(self, JSON_original, count_ts_to_record: int = 40):
        self.JSON_original = JSON_original
        self.count_ts_to_record = count_ts_to_record
        # Если у нас число записей больше чем 11 , то ставим 11
        # if self.count_ts_torecord > 11:
        #     self.count_ts_torecord = 11

        self.__setarate()

    def __setarate(self):
        JSON_original = self.JSON_original

        for i in range(len(JSON_original)):
            # ИТак - Здесь определяем - какие данные попали - моментные или архивные
            # ЕСЛИ ПОПАЛИ АРХИВНЫЕ ДАННЫЕ
            from working_directory.Template.Template_Meter_devices_API.Template_generator_time import \
                measure_containin_day_list, measure_containin_month_list, \
                measure_containin_half_hour_list, measure_containin_hour_list
            archive_measure = measure_containin_day_list + \
                              measure_containin_month_list + \
                              measure_containin_half_hour_list + \
                              measure_containin_hour_list
            self.type_measure = JSON_original[i]['data']['measures'][0]['type']

            for_MeterDev, record_for_data_base = self.__separate_element(JSON_original[i])
            JSON_record_for_data_base = copy.deepcopy(JSON_original[i])
            JSON_record_for_data_base['data']['measures'][0]['devices'][0]['vals'] = record_for_data_base
            JSON_for_MeterDev = copy.deepcopy(JSON_original[i])
            JSON_for_MeterDev['data']['measures'][0]['devices'][0]['vals'] = for_MeterDev

            self.JSON_record_for_data_base.append(JSON_record_for_data_base)
            self.JSON_for_MeterDev.append(JSON_for_MeterDev)

    def __separate_element(self, element):
        """ЗДЕСЬ ДЕЛАЕМ ОЧЕНЬ ВАЖНЫЙ МОМЕНТ - ОПРЕДЕЛЯЕМ ТИП ДВАННЫХ И ПЛУЧАЕМ НУЖНУЮ ВЕТКУ РАЗВИТИЯ"""

        # ЕСЛИ АРХИВНЫЕ ДАННЫЕ
        from working_directory.Template.Template_Meter_devices_API.Template_generator_time import \
            measure_containin_day_list, measure_containin_month_list, \
            measure_containin_half_hour_list, measure_containin_hour_list
        archive_measure = measure_containin_day_list + \
                          measure_containin_month_list + \
                          measure_containin_half_hour_list + \
                          measure_containin_hour_list
        from working_directory.Template.Template_Meter_db_data_API.Template_list_ArchTypes import \
            ElectricConfig_ArchType_name_list, DigitalConfig_ArchType_name_list, PulseConfig_ArchType_name_list

        config = ElectricConfig_ArchType_name_list + DigitalConfig_ArchType_name_list + PulseConfig_ArchType_name_list

        if self.type_measure in archive_measure:

            for_MeterDev, record_for_data_base = self.__separate_element_archive(element)

        # ЕСЛИ ЭТО КОНФИГ

        elif self.type_measure in config:

            for_MeterDev, record_for_data_base = self.__separate_element_config(element)

        # ИНАЧЕ - ЭТО ПРСОТО МОМЕНТНЫЕ ПОКАЗАТЕЛИ
        else:
            for_MeterDev, record_for_data_base = self.__separate_element_moment(element)

        return for_MeterDev, record_for_data_base

    def __separate_element_config(self, element):
        """Здесь разделяем только КОНФИГИ"""
        # ЗДЕСЬ ВСЕ ПРОСТО _ КОНФИГОВ ДО ЗАПРАШИВАЕМОГО НЕ МОЖЖЕТ БЫТЬ
        # Теперь ищем наш список с таймштампами - и сортируем его
        element_list = sorted(element['data']['measures'][0]['devices'][0]['vals'], key=lambda x: x['time'])

        for_MeterDev = copy.deepcopy(element_list)
        record_for_data_base = []

        return for_MeterDev, record_for_data_base

    def __separate_element_moment(self, element):
        """Здесь разделяем только МОМЕНТНЫЕ ДАННЫе"""
        # ЕСЛИ У НАС ПО ЗАДАНИЮ ТРЕБУЕТСЯ ЗАПИСАТЬ БОЛЬШЕ НУЛЯ
        # Теперь ищем наш список с таймштампами - и сортируем его
        element_list = sorted(element['data']['measures'][0]['devices'][0]['vals'], key=lambda x: x['time'])

        if self.count_ts_to_record > 0:
            for_MeterDev = copy.deepcopy(element_list)
            record_for_data_base = copy.deepcopy(element_list)
            import time
            record_for_data_base[0]['time'] = int(time.mktime(datetime.now().timetuple()))

        # ИАНЧЕ _ ОСТАВЛЯЕМ ПУСТЫМ
        else:
            for_MeterDev = copy.deepcopy(element_list)
            record_for_data_base = []

        if self.type_measure in ElectricQualityValues_ArchType_name_list:
            for i in range(len(for_MeterDev)):
                for x in range(len(for_MeterDev[i]['tags'])):
                    if for_MeterDev[i]['tags'][x]['tag'] in ['SA', 'SB', 'SC', 'SS']:
                        # JSON_meter_value[i]['tags'][x]['val'] = None
                        print(for_MeterDev[i]['tags'][x])
                for i in range(len(record_for_data_base)):
                    for x in range(len(record_for_data_base[i]['tags'])):
                        if record_for_data_base[i]['tags'][x]['tag'] in ['SA', 'SB', 'SC', 'SS']:
                            # JSON_meter_value[i]['tags'][x]['val'] = None
                            print(record_for_data_base[i]['tags'][x])

        return for_MeterDev, record_for_data_base

    def __separate_element_archive(self, element):
        """Теперь пойдет жаришка - Сюда попали только архивные записи"""
        # Теперь ищем наш список с таймштампами - и сортируем его
        element_list = sorted(element['data']['measures'][0]['devices'][0]['vals'], key=lambda x: x['time'])
        # Теперь что делаем - В зависимости от того сколько должно остаться - столько и оставляем

        if self.count_ts_to_record < len(element_list):

            # ЕСЛИ ЭТО МГНОВЕНЫЕ ПОКАЗАТЕЛИ!!!
            record_for_data_base = []
            for_MeterDev = []
            element_list_copy = copy.deepcopy(element_list)

            for i in range(len(element_list)):
                if i < self.count_ts_to_record:
                    record_for_data_base.append(element_list_copy[i])
                else:
                    for_MeterDev.append(element_list_copy[i])

        elif self.count_ts_to_record == len(element_list):

            for_MeterDev = []
            record_for_data_base = copy.deepcopy(element_list)

        else:
            # Так Берем максимальный Таймшитамп
            element_list_copy = copy.deepcopy(element_list)
            for_MeterDev = [element_list_copy.pop(-1)]
            record_for_data_base = element_list_copy

        # ТЕПЕРЬ НАМ НАДО ПЕРЕЗАПИСАТЬ ВСЕ НЕКОТОРЫЕ ЗНАЧЕНИЯ

        return for_MeterDev, record_for_data_base
