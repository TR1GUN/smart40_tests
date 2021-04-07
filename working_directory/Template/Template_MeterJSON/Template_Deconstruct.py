# //-------------------------------------------------------------------------------------------------------------------
#                                   Деконструтор JSON для JSON
# //-------------------------------------------------------------------------------------------------------------------
# Итак . Здесь расположим Деконструктор JSON котоырый наследуем от одного


class DeconstructJSON:
    JSON = {}
    JSON_deconstruct = []

    def __init__(self, JSON):
        self.JSON_deconstruct = []
        # Итак - Получаем JSON
        self.JSON = JSON
        # Итак в самом начале определяем ЧТо это за JSON
        # ЕСЛИ ЭТО ОТ METERDATA ответ на GET, то можно сразу ебашить
        if JSON.get("res") == 0:
            self.JSON_deconstruct = self.__parse_measures()
        elif JSON.get("method") == 'post':
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
            for x in range(len(measures_list)):
                # Переопределяем наше поле measure
                measures_list[x]["Name"] = measures[i]["measure"]
            if len(measures_list) > 0:
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

                # серийник
                if 'serial' in devices[i]:
                    devices_dict["serials"] = devices[i]["serial"]

                # Внешний айдишник
                if "meter" in devices[i]:
                    devices_dict["meter"] = devices[i]["meter"]

                # # айдишник
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
            tags_list_full = [{"vals": None}]
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
