from random import randint
from working_directory.Template.Template_Meter_db_data_API.Template_generator_measures_tags import \
    GeneratorTagsByDevices
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes


# --------------------------------------------------------------------------------------------------------------------
#                                 Генератор времени
# --------------------------------------------------------------------------------------------------------------------
# Выведем отдельным классом генерацию времени
class GeneratorTimestamp:
    Timestamp = []
    "Генератор времени"

    def __init__(self, count_ts):

        self.Timestamp = self.__generate_ts(count=count_ts)

    #     Сам генератор времени:
    def __generate_ts(self, count: int):
        """
        Функция для генерации рандомного времени в Unix-time от Jul 14 2017 05:40:00 до Nov 15 2023 01:13:20

        :return:  Возвращает рандомное время в заданом диапазоне
        """
        unixtime_set = set()
        # генерируем нужное колличество :
        for i in range(count):
            # генерим нужное число
            unixtime = randint(1500000000, 1609459200)
            # если оно есть - то генерим до тех пор пока не получим нужное
            if unixtime in unixtime_set:
                while unixtime not in unixtime_set:
                    unixtime = randint(1500000000, 1609459200)
            unixtime_set.add(unixtime)

        return list(unixtime_set)

    def get_Timestamp(self):
        return self.Timestamp


# --------------------------------------------------------------------------------------------------------------------
# Конструктор для времени - добавляет время

class GeneratorValsByDevices:
    vals = []
    deconstruct = []
    deconstruct_dict = []

    # Конструктор для генерации тэгов - очень важно - принимает строковые значения
    def __init__(self, generate_unicale, measure: str, count_ts: int = 1):
        self.deconstruct = []
        self.deconstruct_dict = []
        self.vals = []
        # Первое что делаем - смотрим - если это конфиг - то всегда время будет одно !!!
        if (measure in Template_list_ArchTypes.ElectricConfig_ArchType_name_list) or \
                (measure in Template_list_ArchTypes.PulseConfig_ArchType_name_list) or \
                (measure in Template_list_ArchTypes.DigitalConfig_ArchType_name_list):
            count_ts = 1

        self.vals = self.__form_json_list_vals(measure=measure, count_ts=count_ts, generate_unicale=generate_unicale)

    # Конструктор JSON Массива с временем
    def __form_json_list_vals(self, measure: str, count_ts: int, generate_unicale):
        # забираем колличество генераций

        count = count_ts
        # Делаем шаблон массива
        vals_list = []
        deconstruct_all = []

        # А теперь факус - В зависимости от того какая нам нужна генерация - делаем разные ветвления.
        # ветка false:
        if type(generate_unicale) != bool:
            # генерируем нужное количество УНИКАЛЬНОГО времени для нас
            unixtime_list = generate_unicale
            # После чего мы берем и формируем Отрывок JSON
            for i in range(count):
                deconstruct = []
                vals_dict = {}
                # Наш Unix-time
                vals_dict['ts'] = unixtime_list[i]
                # А сюда генерим нам массив тэгов что записываем
                generate_tags = GeneratorTagsByDevices(measure=measure)

                # теперь делаем следующее возвращаем массив значений что сгенерировали
                generate = generate_tags.get_tags()

                # ----------------------Деконструктор ------------------------------------------
                # # Теперь конструируем наш список возврата -
                # Возвращаем список
                deconstruct_dict = {}
                deconstruct_dict = generate_tags.get_tags_deconstruct_dict()
                # добавляем значение времени и его имя
                deconstruct_dict['ts'] = str(vals_dict['ts'])
                # Сначала берем и добавляем в массив ts
                self.deconstruct_dict.append(deconstruct_dict)
                # ----------------------------------------------------------------------------------
                deconstruct = generate_tags.get_tags_deconstruct()
                deconstruct.reverse()
                deconstruct.append(unixtime_list[i])
                deconstruct.reverse()
                self.deconstruct.append(deconstruct)

                vals_dict['tags'] = generate  # self.__generate_list_tags_by_devices(measure=measure)
                vals_list.append(vals_dict)

        else:
            # После чего мы берем и формируем Отрывок JSON
            for i in range(count):
                # генерируем нужное количество УНИКАЛЬНОГО времени для нас
                unixtime_list = GeneratorTimestamp(count_ts=count).Timestamp
                deconstruct = []
                vals_dict = {}
                # Наш Unix-time
                vals_dict['ts'] = unixtime_list[i]
                # А сюда генерим нам массив тэгов что записываем
                generate_tags = GeneratorTagsByDevices(measure=measure)

                # теперь делаем следующее возвращаем массив значений что сгенерировали
                generate = generate_tags.get_tags()

                # ----------------------пока не используем------------------------------------------
                # # Теперь конструируем наш список возврата -
                # Возвращаем список
                deconstruct_dict = {}
                deconstruct_dict = generate_tags.get_tags_deconstruct_dict()
                # добавляем значение времени и его имя
                deconstruct_dict['ts'] = str(vals_dict['ts'])
                # Сначала берем и добавляем в массив ts
                self.deconstruct_dict.append(deconstruct_dict)

                # ----------------------------------------------------------------------------------
                deconstruct = generate_tags.get_tags_deconstruct()
                deconstruct.reverse()
                deconstruct.append(unixtime_list[i])
                deconstruct.reverse()
                self.deconstruct.append(deconstruct)

                vals_dict['tags'] = generate  # self.__generate_list_tags_by_devices(measure=measure)
                vals_list.append(vals_dict)
        return vals_list

    # Теперь отдаем то что нужно было отдавать

    def get_vals(self):
        """
        Функция которая возвращает результат генерации

        :return:
        """
        return self.vals

    def get_deconstruct(self):
        return self.deconstruct

    def get_deconstruct_dict(self):
        return self.deconstruct_dict


