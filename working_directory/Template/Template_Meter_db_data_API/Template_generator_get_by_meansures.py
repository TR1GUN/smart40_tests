# Здесь класс который будет генерировать JSON get Запроса исходя из тех данных которые мы сгенерировали в классе выше
from working_directory.Template.Template_Meter_db_data_API.Template_generator_measures_tags import DefineTagsByMeasure
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from working_directory import sqlite
from random import randint


class GeneratorGetRequest:
    processed_JSON = {}
    JSON = {}

    """
    Из поля JSON можно считать все что нужно
    """

    def __init__(self,

                 JSON,

                 count_tags: int or list,

                 select_device_idx: bool = True,

                 select_meter_id: bool = True,

                 select_id_all: bool = False,

                 select_last_time: bool = False,

                 out_of_bounds: bool = False,

                 serial: bool = False,

                 select_count_ts: int = 1,

                 select_count_id: int = 1

                 ):

        """
        Генератор для get запроса

        :param JSON: - JSON с помощью которого вставили данные в БД
        :param count_tags: -int, list  Количество тэгов или список тэгов которые попадут в JSON
        :param select_device_idx: -bool Маркер селекта по device_idx - внутрений айдишник -
        :param select_meter_id: -bool Маркер селекта по meter_id - внешний айдишник
        :param select_id_all: -bool Маркер селекта всего что есть.
                                    Взаимоисключающий с select_meter_id, select_device_idx и serial
        :param select_last_time: -bool Маркер селекта последнего времени.
                                        Взаимоисключающий с select_count_ts и out_of_bounds
        :param out_of_bounds: -bool Маркер выхода за границы существующего времени - Важен для настройки лимита времени
        :param serial: -bool Маркер селекта по serial - серийный номер в config
        :param select_count_ts: -int Количество отрезков времени , которые запрашиваем
        :param select_count_id: -int Количество Id которые запрашиваем
        """

        self.JSON = {}
        # ща чо сделаем - переопределяем JSON что получили в поле класса
        self.processed_JSON = JSON

        # окей - теперь важный момент - обрабатываем его  получаем его основные характеристики
        self.select_count_ts = select_count_ts
        self.select_count_id = select_count_id

        # Для начала подготавливаем тестовые данные
        self.__leadUpData_list = LeadUpDataForGetRequest(JSON_measures=JSON,
                                                         select_count_id=select_count_id).leadUpData_list

        # После того как получили необходимые данные , начинаем собирать JSON
        # обьявляем переменую флагов - она нам понадобится чуть позже
        flags = []
        # Добавляем девайсы
        self.JSON["measures"] = self.__added_measure()

        # Добавляем айдишники - в противном случае - селектим все
        if not select_id_all:
            if select_device_idx:
                self.JSON["devices"] = self.__added_device_idx('device_idx')

            if select_meter_id:
                self.JSON["ids"] = self.__added_device_idx('meter_id')


            if serial:
                self.JSON["serials"] = self.__added_device_idx("serial")

        else:
            flags.append("allMeters")

        # добавляем тэги
        # Если мы задали число -
        if type(count_tags) == int:
            # берем все тэги в сэт
            self.all_tags = self.__added_device_idx("tags")
            # проверяем больше ли оно того что у нас есть
            if len(self.all_tags) < count_tags:
                # Если больше - то просто ставим ноль - при нуле селектим все что есть
                count_tags = 0
            # После чего вставляем нужное колличетво тэгов
            self.JSON["tags"] = self.__added_needed_count_tags(count_tags)

        # Иначе - добавляем контректные тэги
        else:
            self.JSON["tags"] = count_tags

        # Добавляем срез времени
        # Если этот тэг в неправде - то мы можем нормально добавлять нужный нам срез времени
        if not select_last_time:
            # обрабатываем все время что у нас есть
            self.all_time = self.__added_ts()
            # Дальше работаем с select_count_ts - Если он больше чем у нас есть в массиве - обнуляем
            if len(self.all_time) < select_count_ts:
                select_count_ts = 0

            # итак проверяем выход за границы - это важно

            # мы не выходим за границы
            if not out_of_bounds:
                # Если количество - 0 - делает старт и конец один и тот же ts
                if select_count_ts == 0:
                    # берем рандомный таймштамп
                    i = randint(0, (len(self.all_time) - 1))

                    self.JSON["time"] = [{"start": self.all_time[i],
                                          "end": self.all_time[i]
                                          }]
                # Если количество - 1 - старт это минимальное значение , а конец это максимальное
                elif select_count_ts == 1:
                    self.JSON["time"] = [{
                        "start": max(self.all_time),
                        "end": min(self.all_time)
                    }]
                # Если количество - 2 и больше - нарезаем внутри отрезка
                else:
                    self.JSON["time"] = self.__generate_segment_time(count=select_count_ts,
                                                                     out_of_bounds=out_of_bounds)

            # Если мы выходим за границы -  то тут все куда интереснее
            else:
                # Если количество - 0 - то мы просто берем и селектим все время что у нас есть
                if select_count_ts == 0:
                    self.JSON["time"] = []
                # Если количество - 1 - то мы просто берем все что вне границ
                elif select_count_ts == 1:

                    self.JSON["time"] = [
                        {
                            "start": 0,
                            "end": min(self.all_time)
                        },
                        {
                            "start": max(self.all_time),
                            "end": 1800000000
                        }
                    ]
                    # Если количество - 2 и больше - нарезаем по всему отрезку
                else:
                    self.JSON["time"] = self.__generate_segment_time(count=select_count_ts,
                                                                     out_of_bounds=out_of_bounds)
        else:
            flags.append("lastTime")
            # -------------------------------------
            # обрабатываем все время что у нас есть
            self.all_time = self.__added_ts()
            # Дальше работаем с select_count_ts - Если он больше чем у нас есть в массиве - обнуляем
            if len(self.all_time) < select_count_ts:
                select_count_ts = 0

            # итак проверяем выход за границы - это важно

            # мы не выходим за границы
            if not out_of_bounds:
                # Если количество - 0 - делает старт и конец один и тот же ts
                if select_count_ts == 0:
                    # берем рандомный таймштамп
                    i = randint(0, (len(self.all_time) - 1))

                    self.JSON["time"] = [{"start": self.all_time[i],
                                          "end": self.all_time[i]
                                          }]
                # Если количество - 1 - старт это минимальное значение , а конец это максимальное
                elif select_count_ts == 1:
                    self.JSON["time"] = [{
                        "start": max(self.all_time),
                        "end": min(self.all_time)
                    }]
                # Если количество - 2 и больше - нарезаем внутри отрезка
                else:
                    self.JSON["time"] = self.__generate_segment_time(count=select_count_ts,
                                                                     out_of_bounds=out_of_bounds)

            # Если мы выходим за границы -  то тут все куда интереснее
            else:
                # Если количество - 0 - то мы просто берем и селектим все время что у нас есть
                if select_count_ts == 0:
                    self.JSON["time"] = []
                # Если количество - 1 - то мы просто берем все что вне границ
                elif select_count_ts == 1:

                    self.JSON["time"] = [
                        {
                            "start": 0,
                            "end": min(self.all_time)
                        },
                        {
                            "start": max(self.all_time),
                            "end": 1800000000
                        }
                    ]
                    # Если количество - 2 и больше - нарезаем по всему отрезку
                else:
                    self.JSON["time"] = self.__generate_segment_time(count=select_count_ts,
                                                                     out_of_bounds=out_of_bounds)
        # ---------------------------------------
        # в конце добавляем флаги
        self.JSON["flags"] = flags

    def get_JSON(self):
        return self.JSON

        # Добавление в финальный JSON списка measure

    def __added_measure(self):
        data_list = self.__leadUpData_list

        measure_list = []
        for i in range(len(data_list)):
            measure_list.append(data_list[i]["measure"])


        return measure_list

    def __added_device_idx(self, name_key):
        data_list = self.__leadUpData_list
        device_idx_full_set = set()
        for i in range(len(data_list)):
            device_idx_set = data_list[i][name_key]
            device_idx_set = set(device_idx_set)
            # обьеденяем эти множества
            device_idx_full_set = device_idx_full_set | device_idx_set

        return list(device_idx_full_set)

    def __added_ts(self):
        data_list = self.__leadUpData_list
        device_idx_full_set = set()
        for i in range(len(data_list)):
            device_idx_ts_full_set = set()
            for x in range(len(data_list[i]['ts'])):
                device_idx_set = data_list[i]['ts'][x]['ts']
                device_idx_set = set(device_idx_set)
                # обьеденяем эти множества
                device_idx_ts_full_set = device_idx_ts_full_set | device_idx_set
            device_idx_full_set = device_idx_full_set | device_idx_ts_full_set

        return list(device_idx_full_set)

    # здесь из всего сэта выбираем рандомное колличество тэгов
    def __added_needed_count_tags(self, count):
        # Получаем все тэги
        full_tag_list = self.all_tags
        tag_list = []
        for i in range(count):
            tag = randint(0, (len(full_tag_list) - 1))
            tag_list.append(full_tag_list.pop(tag))
        return tag_list

    def __generate_segment_time(self, count: int, out_of_bounds: bool):
        time_list = []

        if out_of_bounds:
            max_limited = 1800000000
            min_limited = 1000000000
        else:
            max_limited = max(self.all_time)
            min_limited = min(self.all_time)

        for i in range(count):
            # Генерируем два значения
            value1 = randint(min_limited, max_limited)
            value2 = randint(min_limited, max_limited)
            # Выясняем какое из них больше, какое меньше
            start = min([value1, value2])
            end = max([value1, value2])
            # Делаем из этого список
            time_dict = {
                "start": start,
                "end": end

            }
            time_list.append(time_dict)
        return time_list


# Класс который подготавливает данные для формирования нужного гет запроса
class LeadUpDataForGetRequest:
    leadUpData_list = []
    select_count_id = None

    def __init__(self, JSON_measures: list,

                 select_count_id: int):
        self.select_count_id = None
        self.leadUpData_list = []


        self.select_count_id = select_count_id
        self.leadUpData_list = self.__added_measures(JSON_measures)

    def __added_measures(self, JSON_measures: list):
        # Проходимся по каждому из конфигов
        measures_list = []
        # для начала надо взять и получить все idx
        device_idx = []
        for i in range(len(JSON_measures)):
            device_idx_element = self.__added_device_idx(JSON_measures[i]["devices"])
            device_idx = device_idx + device_idx_element
        # После чего пихаем в сэт и выбираем из него нужный нам элемент
        device_idx = self.__get_the_right_amount_id(device_idx)

        for i in range(len(JSON_measures)):
            # Добавляем в словарь :
            measure_dict = {"measure": JSON_measures[i]["measure"]}
            # Сам тип данных
            # его выбранные рандомом внутрение ид

            measure_dict["device_idx"] = device_idx
            # его внешние ид исходя из внутрених
            measure_dict["meter_id"] = self.__added_meter_id_from_meter_table(device_idx=device_idx)
            # таймстампы выбранных внутрених ид
            measure_dict["ts"] = self.__added_all_timestamp_by_id(device_idx=device_idx,
                                                                  devices=JSON_measures[i]["devices"])
            # Теперь добавляем все тагс
            measure_dict["tags"] = self.__added_all_tags(measure=JSON_measures[i]["measure"])

            # Добавляем серийники
            measure_dict["serial"] = self.__added_serial(device_idx=device_idx)

            measures_list.append(measure_dict)

        return measures_list

    def __get_the_right_amount_id(self, idx: list):
        # делаем из него сэт чтоб избавиться от дублей
        idx = set(idx)
        # после этого выбираем нужное количество
        idx = list(idx)
        # Теперь рандомно выбираем нужное колличество
        ids_for_get_json = []
        for i in range(self.select_count_id):
            x = randint(0, (len(idx) - 1))
            element = idx.pop(x)
            ids_for_get_json.append(element)
        # Теперь  имеем список id для выборки, теперь по ним получаем ts
        return ids_for_get_json

    def __added_device_idx(self, devices):
        # для начала получаем список колличества id для выборки
        # сначала получаем рандомно выбранные id
        all_id_list = []
        for i in range(len(devices)):
            # формируем лист из всех Id
            all_id_list.append(devices[i]["id"])
        # Теперь рандомно выбираем нужное колличество
        ids_for_get_json = []
        for i in range(self.select_count_id):
            x = randint(0, (len(all_id_list) - 1))
            element = all_id_list.pop(x)
            ids_for_get_json.append(element)
        # Теперь  имеем список id для выборки, теперь по ним получаем ts
        return ids_for_get_json

    # Получаем все ids Из Metertable
    def __added_meter_id_from_meter_table(self, device_idx: list):

        sql_command = ' MeterTable WHERE DeviceIdx IN (' + str(device_idx)[1:-1] + ")"
        result = sqlite.readtable_return_dict(collum=' MeterId ', table_name=sql_command)
        # а теперь очищаем все это
        meter_id_list = []
        for i in range(len(result)):
            meter_id_list.append(result[i]['MeterId'])

        return meter_id_list

        # Теперь получаем все ts

    def __added_all_timestamp_by_id(self, device_idx: list, devices: list):
        # Получаем все ts по выбранным айдишникам
        all_timestamp_list = []
        for i in range(len(devices)):
            if devices[i]["id"] in device_idx:
                timestamp_dict = {'id': devices[i]["id"]}
                timestamp_list = []
                for x in range(len(devices[i]["vals"])):
                    timestamp_list.append(devices[i]["vals"][x]["ts"])
                timestamp_dict["ts"] = timestamp_list
                all_timestamp_list.append(timestamp_dict)

        return all_timestamp_list

    # Здесь получаем все доступные тэги для этого measures
    def __added_all_tags(self, measure):
        tags = DefineTagsByMeasure(measure).tag
        return tags

    def __added_serial(self, device_idx: list):
        meter_id_list = []
        sql_command = ' ElectricConfig WHERE DeviceIdx IN ' + '(' + str(device_idx)[1:-1] + ")"
        result = sqlite.readtable_return_dict(collum='Serial', table_name=sql_command)
        # а теперь очищаем все это

        for i in range(len(result)):
            meter_id_list.append(result[i]['Serial'])

        sql_command = ' DigitalConfig WHERE DeviceIdx IN ' + '(' + str(device_idx)[1:-1] + ")"
        result = sqlite.readtable_return_dict(collum='Serial', table_name=sql_command)
        # а теперь очищаем все это

        for i in range(len(result)):
            meter_id_list.append(result[i]['Serial'])

        sql_command = ' PulseConfig WHERE DeviceIdx IN ' + '(' + str(device_idx)[1:-1] + ")"
        result = sqlite.readtable_return_dict(collum='Serial', table_name=sql_command)
        # а теперь очищаем все это

        for i in range(len(result)):
            meter_id_list.append(result[i]['Serial'])

        return meter_id_list


class DeleteAddedConfig:
    """
    Класс Который обрезает добавленные конфиги

    """


    JSON = None
    added_config = None

    def __init__(self, JSON, added_config: bool = False):

        self.added_config = added_config

        # Теперь что делаем - берем список measure_list и Прогоняем его
        self.JSON = self.__delete_added_config(measure_list=JSON)

    # -------------------------------------------------------------Добавленно-----------------------------------------------
    def __delete_added_config(self, measure_list):
        # Смотрим - добавляли или нет мы конфиг
        if self.added_config:
            # Берем JSON что нам нужен
            for i in range(len(measure_list)):
                if (measure_list[i]['measure'] in Template_list_ArchTypes.ElectricConfig_ArchType_name_list) or \
                        (measure_list[i]['measure'] in Template_list_ArchTypes.PulseConfig_ArchType_name_list) or \
                        (measure_list[i]['measure'] in Template_list_ArchTypes.DigitalConfig_ArchType_name_list):
                    # Если да - то удаляем его из общего списка
                    measure_list.pop(i)
        return measure_list
    # -------------------------------------------------------------
