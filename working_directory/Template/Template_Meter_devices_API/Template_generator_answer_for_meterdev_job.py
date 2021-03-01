# Здесь расположим класс генератор для генерации нужных данных ответа , и соответственно - счетчик сам будет их считывать
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from working_directory.Template.Template_Meter_devices_API import Template_list_job
from Emulator.Counters.Config_settings import get_time


class CompletionSupposedAnswer:
    """
    Генератор для достройки ПРЕДПОЛОГАЕМОГО JSON ответа для виртуального счетчика
    """
    measure = None
    JSON_supposed = None

    JSON_answer = None

    JSON_normal = None

    def __init__(self, measure, JSON_supposed: dict, JSON_answer: dict):
        # Переоопределяем поля
        self.measure = measure
        # Список данных с однним таймштампов - моментные показания
        self.measure_moment_list = \
            [
                Template_list_ArchTypes.ElectricConfig_ArchType_name_list[0],
                Template_list_ArchTypes.PulseConfig_ArchType_name_list[0],
                Template_list_ArchTypes.DigitalConfig_ArchType_name_list[0],
                Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list[0],
                Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list[0],
                Template_list_ArchTypes.PulseValues_ArchType_name_list[0],
                Template_list_ArchTypes.DigitalValues_ArchType_name_list[0],
            ]

        self.JSON_supposed = JSON_supposed
        self.JSON_answer = JSON_answer
        # Читаем мгновенное время Из JSON !!!

        self.instant_time = get_time()

        # После вызываем наш заменитель
        self.JSON_normal = self.__completion_json()

    def __completion_json(self):
        # Итак, для начала мы делаем определение - надо или нет на генерировать значения для Нужных
        # Если у нас серийник
        if self.measure in Template_list_job.GetSerial_list:
            # Если у нас серийник , то исправляем серийник -
            self.JSON_supposed['data']['measures'][0]['devices'][0]['model'] = ''
        # Если у нас archtype
        # Достраиваем для Конфигов и моментных показателей
        if self.measure in self.measure_moment_list:
            # Достраиваем тайм штамп
            self.JSON_supposed['data']['measures'][0]['devices'][0]['vals'][0]['time'] = self.instant_time
        # текущие ПКЭ электросчетчика Достраиваем до нужного значения
        if self.measure in Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list:

            vals = self.JSON_supposed['data']['measures'][0]['devices'][0]['vals']
            for i in range(len(vals)):
                tags = vals[i]["tags"]
                # Переопределяем значения :
                for x in range(len(tags)):
                    # Для начала переопределяем знак угла - Это важно
                    if self.JSON_supposed['data']['measures'][0]['devices'][0]['vals'][i]["tags"][x]["tag"] == 'AngAC':
                        self.JSON_supposed['data']['measures'][0]['devices'][0]['vals'][i]["tags"][x]["val"] =\
                            self.JSON_supposed['data']['measures'][0]['devices'][0]['vals'][i]["tags"][x]["val"] * -1

                    # # Далее заменяем значения полной мощности на нон
                    # if self.JSON_supposed['data']['measures'][0]['devices'][0]['vals'][i]["tags"][x]["tag"] in ['SA', 'SB', 'SC', 'SS']:
                    #     self.JSON_supposed['data']['measures'][0]['devices'][0]['vals'][i]["tags"][x]["val"] = None
        return self.JSON_supposed
