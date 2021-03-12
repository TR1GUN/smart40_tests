# Итак - я не придумал ничего умного кроме как
# дособирать JSON из meter dev до вида который представляет из себя POST запрос к meter data
from working_directory.Connect.JSON_format_coding_decoding import code_JSON, decode_JSON
import time, write_file


class AssemblyDictLikeMeterData:
    """тут собираем дособирать JSON из meter dev до вида который представляет из себя POST запрос к meter data """

    JSON = {
        'method': 'post',
        'res': 0,
        'measures': None
    }
    JSON_list = []
    ids_meter = []

    def __init__(self, JSON_list: list, ids_meter):
        # Теперь берем наш Дособиратель и разбираем написианное тут
        self.ids_meter = ids_meter
        self.JSON_list = JSON_list
        JSON_measures_list = []
        for i in range(len(self.JSON_list)):
            JSON_measures_list.append(self.__purifyd_service_tag(self.JSON_list[i]['data']['measures'][0]))

        # ПОСЛЕ ЧЕГО :
        self.JSON['measures'] = JSON_measures_list

    def __purifyd_service_tag(self, JSON):
        "здесь отчищаем от лишних ТЭГОВ НАЩ JSON"
        # Переименовываем ключ тайп

        print(JSON['type'])
        JSON['measure'] = JSON.pop('type')
        for i in range(len(JSON['devices'])):
            JSON['devices'][i]['id'] = self.ids_meter[i]
            # Теперь переопрелеляем тайм
            for x in range(len(JSON['devices'][i]['vals'])):
                JSON['devices'][i]['vals'][x]['ts'] = JSON['devices'][i]['vals'][x].pop('time')

        return JSON


class RecordFromEmulatorMeter:
    '''Класс который Переводит наш JSON формат котоырй кушает наш эмулятор счетчика'''

    def __init__(self, JSON_list):

        self.JSON_record = {"vals": []}
        # Итак - что мы делаем - Мы составляем огромный JSON о всеми возможными значениями -
        # если значение моментое - делаем на это скидку

        for i in range(len(JSON_list)):
            JSON = JSON_list[i]

            vals = JSON['data']['measures'][0]['devices'][0]['vals']
            for x in range(len(vals)):
                self.JSON_record["vals"].append(vals[x])

            # А Теперь берем и перезаписываем все наши значения

        JSON_meter_value = self.JSON_record
        # Теперь все это упаковываем в JSON и сохраняем
        JSON_meter_value = code_JSON(JSON_meter_value)

        write_file.write_file_JSON_on_Emulator(writen_text=JSON_meter_value)



# ---------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------
# Итак . Здесь расположим Деконструктор JSON котоырый наследуем от одного


class DecostructMeterDataJSONForDaemon:
    JSON = {}
    JSON_deconstruct = []

    def __init__(self, JSON):
        self.JSON_deconstruct = []
        # Итак - Получаем JSON
        self.JSON = JSON
        if JSON["res"] == 0:
            self.JSON_deconstruct = self.__parse_measures()

    def __parse_measures(self):
        # проходимся по каждому элементу массива
        measures = self.JSON["measures"]
        measures_list_full = []
        for i in range(len(measures)):
            # Определяем что спускается ниже
            self.devices = measures[i]["devices"]
            # Спасукаем элемент ниже по цепочке
            measures_list = self.__parse_devices()
            print('GOOOOOVNOOOOOOOO')
            for x in range(len(measures_list)):
                measures_list[x]["Name"] = measures[i]["measure"]
            measures_list_full.append(measures_list)

        return measures_list_full

    def __parse_devices(self):
        # Парсер поля devices
        devices = self.devices
        if devices is None:
            devices_list_full = []

        elif len(devices) > 0:
            devices_list_full = []
            for i in range(len(devices)):
                devices_list = []
                devices_dict = {}
                # внутрений айдишник
                if "id" in devices[i]:
                    devices_dict["id"] = devices[i]["id"]

                # # серийник
                # if 'serial' in devices[i]:
                #     devices_dict["serials"] = devices[i]["serial"]
                #
                # # Внешний айдишник
                # if "meter" in devices[i]:
                #     devices_dict["meter"] = devices[i]["meter"]

                # айдишник
                # try:
                #     element["id"] = devices[i]["id"]
                # except:
                #     pass

                # После того как определились с этими Элементами - спускаем готовый элемент ниже
                # Получаем с предыдущей функции массив

                if "vals" in devices[i]:
                    # Определяем поле - получаем все что есть ниже
                    self.vals = devices[i]["vals"]
                    devices_list = self.__parse_vals()
                    for x in range(len(devices_list)):
                        devices_list[x].update(devices_dict)
                else:
                    devices_dict["vals"] = None
                    devices_list.append(devices_dict)
                devices_list_full = devices_list_full + devices_list


        else:
            devices_list_full = []

        return devices_list_full

    def __parse_vals(self):
        # Парсер поля vals
        vals = self.vals
        if vals is None:
            tags_list_full = [{"vals":None}]
        elif len(vals) > 0:
            tags_list_full = []
            for i in range(len(vals)):
                element_ts = {}

                if "ts" in vals[i]:
                    element_ts["ts"] = vals[i]["ts"]

                if "tags" in vals[i]:
                    self.tags = vals[i]["tags"]
                    element = self.__parse_tags()
                    element.update(element_ts)
                else:
                    element_ts["tags"] = None
                    element.update(element_ts)

                tags_list_full.append(element)
        else:
            tags_list_full = []

        return tags_list_full

    def __parse_tags(self):
        # Парсер поля tags
        tags = self.tags
        if tags is None:
            element = {}

        elif len(tags) > 0:
            element = {}
            for i in range(len(tags)):
                if type(tags[i]["val"]) == bool:
                    # Переводим в стрингу
                    tags[i]["val"] = str(tags[i]["val"])

                    # Меняем
                    if tags[i]["val"] == 'True':
                        tags[i]["val"] = 1

                    if tags[i]["val"] == 'False':
                        tags[i]["val"] = 0


                # Записываем
                element[tags[i]["tag"]] = tags[i]["val"]

        else:
            element = {}

        return element