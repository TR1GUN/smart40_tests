# Итак - я не придумал ничего умного кроме как
# дособирать JSON из meter dev до вида который представляет из себя POST запрос к meter data
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from Emulator.Counters.Config_settings import get_time
from copy import deepcopy


# //-----------------------------------------------------------------------------------------------------------------
#                         Класс для перестройки JSON формата MeterDEV в формат Meter DATA
# //-----------------------------------------------------------------------------------------------------------------
class AssemblyDictLikeMeterData:
    """тут собираем дособирать JSON из meter dev до вида который представляет из себя POST запрос к meter data """

    JSON = {
        'method': 'post',
        'res': 0,
        'measures': None
    }
    JSON_list = []
    ids_meter = []
    measure_list = []
    JSON_GET = {}
    serial = None

    def __init__(self, JSON_list: list, ids_meter, serial=None):

        self.JSON = {
            'method': 'post',
            'res': 0,
            'measures': None
        }
        # Теперь берем наш Дособиратель и разбираем написанное тут
        self.ids_meter = ids_meter
        self.JSON_list = JSON_list
        self.serial = serial

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

        # Читаем мгновенное время Из JSON !!!

        self.instant_time = get_time()

        JSON_measures_list = []
        for i in range(len(self.JSON_list)):
            JSON_measures_list.append(self.__purifyd_service_tag(self.JSON_list[i]['data']['measures'][0]))

        # ПОСЛЕ ЧЕГО :
        self.JSON['measures'] = JSON_measures_list

        self.JSON_GET = self.__GET_meter_data()

    def __purifyd_service_tag(self, JSON):
        "здесь отчищаем от лишних ТЭГОВ НАЩ JSON"
        # Переименовываем ключ тайп
        self.measure_list.append(deepcopy(JSON['type']))

        JSON['measure'] = JSON.pop('type')
        # ------------------------ИСПРАВЛЕННО----------------------------
        self.measure = JSON['measure']
        # КОПИРУЕМ СНОВНОЙ ЭЛЕМЕНТ

        fild_devices = deepcopy(JSON['devices'].pop(0))
        for i in range(len(self.ids_meter)):
            JSON['devices'].append(deepcopy(fild_devices))

            # print(JSON['devices'])
            # print(fild_devices)
            # for i in range(len(JSON['devices'])):
            JSON['devices'][i]['id'] = self.ids_meter[i]

            # Теперь переопрелеляем тайм
            # Здесь - Удаляем серийник
            if JSON['devices'][i].get('serial') is not None:
                JSON['devices'][i].pop('serial')
            if JSON['devices'][i].get('model') is not None:
                JSON['devices'][i].pop('model')

            for x in range(len(JSON['devices'][i]['vals'])):
                JSON['devices'][i]['vals'][x]['ts'] = JSON['devices'][i]['vals'][x].pop('time')

                # !!!!!!!!!!!!!!!!!!!!!!!!!!ЗАГЛУШКА
                # !!!!!!!!!!!!!!!!!!!!!!!!!! Переводим 0 в нужные нам значения
                # !!!!!!!!!!!!!!!!!!!!!!!!!!

                # Если у нас мгновенный показатель , меняем время что содержится в счетчике
                # if self.measure in self.measure_moment_list:
                #     JSON['devices'][i]['vals'][x]['ts'] = self.instant_time

                if self.measure in self.measure_moment_list:
                    JSON['devices'][i]['vals'][x]['ts'] = 0

                # !!!!!!!!!!!!!!!!!!!!!!!!!!ЗАГЛУШКА
                # !!!!!!!!!!!!!!!!!!!!!!!!!! Переводим 0 в нужные нам значения
                # !!!!!!!!!!!!!!!!!!!!!!!!!!

                if JSON['devices'][i]['vals'][x].get('diff') is not None:
                    JSON['devices'][i]['vals'][x].pop('diff')

                # текущие ПКЭ электросчетчика Достраиваем до нужного значения
                # if self.measure in Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list:
                #     for z in range(len(JSON['devices'][i]['vals'][x]["tags"])):
                #         # Для начала переопределяем знак угла - Это важно
                #         if JSON['devices'][i]['vals'][x]["tags"][z]["tag"] == 'AngAC':
                #             JSON['devices'][i]['vals'][x]["tags"][z]["val"] = JSON['devices'][i]['vals'][x]["tags"][z][
                #                                                                   "val"] * -1

                # if JSON['devices'][i]['vals'][x]["tags"][z]["tag"] in ['SA', 'SB', 'SC', 'SS']:
                #     JSON['devices'][i]['vals'][x]["tags"][z]['val'] = None
                # Теперь смотрим тоже самое для конфигов
                if self.measure in Template_list_ArchTypes.ElectricConfig_ArchType_name_list:
                    delete_index_list = []
                    for z in range(len(JSON['devices'][i]['vals'][x]["tags"])):
                        # Перезаписываем серийник - Если у нас спускается
                        if JSON['devices'][i]['vals'][x]["tags"][z]["tag"] in ["serial"]:
                            if self.serial is not None:
                                JSON['devices'][i]['vals'][x]["tags"][z]["val"] = str(self.serial)

                        if JSON['devices'][i]['vals'][x]["tags"][z]["tag"] in ["VarConsDepth", "MonDepth",
                                                                               "MonConsDepth", "DayDepth",
                                                                               "DayConsDepth", "cTime", "isCons"]:
                            delete_index_list.append(z)

                    # Теперь - удаляем лишнее -
                    delete_index_list.reverse()
                    for z in delete_index_list:
                        JSON['devices'][i]['vals'][x]["tags"].pop(z)

                # ПРОФИЛЬ МОЩНОСТИ
                if self.measure in Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list:
                    delete_index_list = []
                    for z in range(len(JSON['devices'][i]['vals'][x]["tags"])):
                        if JSON['devices'][i]['vals'][x]["tags"][z]["tag"] in ["isMeas"]:
                            delete_index_list.append(z)

                    # Теперь - удаляем лишнее -
                    delete_index_list.reverse()
                    for z in delete_index_list:
                        JSON['devices'][i]['vals'][x]["tags"].pop(z)
                # ЖУРНАЛЫ
                if self.measure in Template_list_ArchTypes.JournalValues_ArchType_name_list:
                    delete_index_list = []
                    for z in range(len(JSON['devices'][i]['vals'][x]["tags"])):
                        if JSON['devices'][i]['vals'][x]["tags"][z]["tag"] in ["journalId"]:
                            delete_index_list.append(z)

                    # Теперь - удаляем лишнее -
                    delete_index_list.reverse()
                    for z in delete_index_list:
                        JSON['devices'][i]['vals'][x]["tags"].pop(z)

        return JSON

    def __GET_meter_data(self):

        # ТЕПЕРЬ ДЕЛАЕМ POST ЗАПРОС для нашей БД

        JSON_GET = {"measures": self.measure_list,
                    "devices": self.ids_meter,
                    "tags": [],
                    "time": [],
                    "flags": [],
                    "method": "get"}

        return JSON_GET
