# Итак - начнем сразу с большого . Генератора measures
from working_directory import sqlite
from random import randint
from working_directory.Template.Template_Meter_db_data_API.Template_generator_measures_id import GeneratorIdDevices, \
    GeneratorDeviceIdx
from working_directory.Template.Template_Meter_db_data_API.Template_generator_measures_ts import GeneratorTimestamp
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes


class GeneratorMeasures:
    json = {}
    json_deconstruct = []
    json_deconstruct_dict = []

    def __init__(self):
        """

        """
        # Переопределяем поля
        self.json = {}
        self.json_deconstruct = []
        self.json_deconstruct_dict = []

    # ------------------------------------------------------------------------------------------------------------------
    # Теперь здесь мы пропишем все нужные методы для выброски наружу!!

    # первый метод формирует JSON рандомом!!!
    def get_all_measure(self,
                        # Количество measure
                        count_measure: int = 3,
                        # Количество timestamp
                        count_ts: int = 1,
                        # Количество id
                        count_id: 3 = 3,
                        # Маркер генерации одних и тех же ts для всех
                        generate_unicale_ts: bool = True,
                        # Маркер генерации одних и тех же id для всех
                        generate_unicale_id: bool = True):
        """
        Метод генератора JSON для post запроса
        генерирует JSON c рандомно выбранными archtype Name

        :param count_measure:   Количество конфигов -  Количество measure которое будет сгенерированно
        :param count_ts: Количество timestamp - Количество ts которое будет у каждого id
        :param count_id: Количество id - Количество id которое будет у каждого measure
        :param generate_unicale_ts: Маркер генерации одних и тех же ts для всех - по умолчанию true.
                                    Если выставить false, то у всех ненерируемых значений будет один и тот же набор ts
        :param generate_unicale_id: Маркер генерации одних и тех же id для всех - по умолчанию true.
                                    Если выставить false, то у всех ненерируемых значений будет один и тот же набор id
        :return: Возвращает сгенерированный по задданым параметрам JSON

        """
        self.json_deconstruct = []

        # Первым делом опредеялем поля measure - их должно быть меньше чем есть весго записей !!!!
        if count_measure < 60:
            # получаем список сгенерирвоанных значений конфигов !!

            measure = self.__generator_measure(count_measure=count_measure)
            # Теперь формируем джейсон

            measures = []
            # Определяемся со временем, если у нас оно не уникально, то генерим его здесь и спускаем дальше:
            if not generate_unicale_ts:
                generate_unicale_ts = self.__control_unical_ts(count=count_ts)
            # Определяемся со id, если у нас оно не уникально, то генерим его здесь и спускаем дальше:
            if not generate_unicale_id:
                generate_unicale_id = self.__control_unical_idx(count=count_id)

            for i in range(count_measure):

                # Важный момент - проверяем на конфиг наш атрибут
                checkup_config = self.__limitation_in_quantity_ts_for_config(measure[i])
                if checkup_config:
                    # Если это конфиг то нам надо по одному ts
                    if type(generate_unicale_ts) != bool:
                        count_ts = 1
                        generate_unicale_ts = [generate_unicale_ts[0]]
                    else:
                        count_ts = 1

                generate_json = {}
                # Сюда пихаем из сгенерирвоанных моментов
                generate_json['measure'] = measure[i]

                devices = GeneratorIdDevices(
                                                count_id=count_id,
                                                count_ts=count_ts,
                                                measure=measure[i],
                                                generate_unicale_id=generate_unicale_id,
                                                generate_unicale_ts=generate_unicale_ts
                                                                                        )
                generate_json['devices'] = devices.get_devices()
                deconstruct_vals = devices.get_devices_deconstruct()
                deconstruct = self.__generate_deconstruct(list_vals=deconstruct_vals,
                                                          measures=measure[i])
                self.json_deconstruct = self.json_deconstruct + deconstruct

                # ---------------------------деконструктор-------------------------------
                deconstruct_vals = devices.get_devices_deconstruct()
                deconstruct = self.__generate_deconstruct(list_vals=deconstruct_vals,
                                                          measures=measure[i])
                self.json_deconstruct = self.json_deconstruct + deconstruct
                # ---------------------деконструктор словарем для БД----------------------
                deconstruct_vals_dict = devices.get_devices_deconstruct_dict()
                deconstruct_dict = self.__generate_deconstruct_dict(list_vals=deconstruct_vals_dict,
                                                                    measures=measure[i])
                # self.deconstruct_dict = self.deconstruct_dict + deconstruct_dict
                self.json_deconstruct_dict.append(deconstruct_dict)
                # ---------------------------------------------------------------------------------

                measures.append(generate_json)


        else:
            measures = None
        return measures

    # Второй метод формирует JSON исходя из массива конфигов которые мы ему передали
    def get_parametrize_measure(self,
                                # Массив конфигов
                                list_measure: list = ['ElConfig'],
                                # Количество timestamp
                                count_ts: int = 1,
                                # Количество id
                                count_id: 3 = 3,
                                # Маркер генерации одних и тех же ts для всех
                                generate_unicale_ts: bool = True,
                                # Маркер генерации одних и тех же id для всех
                                generate_unicale_id: bool = True):
        """
        Метод генератора JSON для post запроса
        генерирует JSON исходя из массива конфигов которые мы ему передали

        :param list_measure:   Массив конфигов - Сюда пихать archtype Name
        :param count_ts: Количество timestamp - Количество ts которое будет у каждого id
        :param count_id: Количество id - Количество id которое будет у каждого measure
        :param generate_unicale_ts: Маркер генерации одних и тех же ts для всех - по умолчанию true.
                                    Если выставить false, то у всех ненерируемых значений будет один и тот же набор ts
        :param generate_unicale_id: Маркер генерации одних и тех же id для всех - по умолчанию true.
                                    Если выставить false, то у всех ненерируемых значений будет один и тот же набор id
        :return: Возвращает сгенерированный по задданым параметрам JSON
        """
        # для начала проверяем наш массив , что он не содержит ничего лишнего !!1
        measures = []
        self.json_deconstruct = []

        # Определяемся со временем, если у нас оно не уникально, то генерим его здесь и спускаем дальше:
        if not generate_unicale_ts:
            generate_unicale_ts = self.__control_unical_ts(count=count_ts)
        # Определяемся со id, если у нас оно не уникально, то генерим его здесь и спускаем дальше:
        if not generate_unicale_id:
            generate_unicale_id = self.__control_unical_idx(count=count_id)

        element_list_measure_string = True
        # Если у нас длина элементов больше нуля , то продолжаем
        if len(list_measure) > 0:
            # После чего проходимся по каждому элементу массива и проверяем - стринг ли он
            for i in range(len(list_measure)):
                if type(list_measure[i]) == str:
                    # Важный момент - проверяем на конфиг наш атрибут
                    checkup_config = self.__limitation_in_quantity_ts_for_config(list_measure[i])
                    if checkup_config:
                        # Если это конфиг то нам надо по одному ts
                        if type(generate_unicale_ts) != bool:
                            count_ts = 1
                            generate_unicale_ts = [generate_unicale_ts[0]]
                        else:
                            count_ts = 1

                    # Если это стринг то что мы делаем - формируем элемент массива из словаря
                    measures_dict = {}
                    # дергаем наш конфиг
                    measures_dict['measure'] = list_measure[i]
                    # генерируем данные для него
                    devices = GeneratorIdDevices(count_id=count_id,
                                                 count_ts=count_ts,
                                                 measure=list_measure[i],
                                                 generate_unicale_id=generate_unicale_id,
                                                 generate_unicale_ts=generate_unicale_ts)
                    measures_dict['devices'] = devices.get_devices()

                    # ---------------------------деконструктор-------------------------------
                    deconstruct_vals = devices.get_devices_deconstruct()
                    deconstruct = self.__generate_deconstruct(list_vals=deconstruct_vals,
                                                              measures=list_measure[i])
                    self.json_deconstruct = self.json_deconstruct + deconstruct
                    # ---------------------деконструктор словарем для БД----------------------
                    deconstruct_vals_dict = devices.get_devices_deconstruct_dict()
                    deconstruct_dict = self.__generate_deconstruct_dict(list_vals=deconstruct_vals_dict,
                                                                        measures=list_measure[i])
                    # self.deconstruct_dict = self.deconstruct_dict + deconstruct_dict
                    self.json_deconstruct_dict.append(deconstruct_dict)

                    measures.append(measures_dict)
                else:
                    # иначе - ставим пометочку
                    element_list_measure_string = False

        else:
            measures = None

        # Делаем дополнительную проверку в случае если что то пошло не так - возвращаем пустоту
        if (element_list_measure_string == False) or (measures is None):
            return None
        else:
            return measures

        #     Контроль уникальных значений времени:

    # ------------------------------------------------------------------------------------------------------------------
    # -----------------Здесь расположим генераторы для НЕ УНИКАЛЬНЫХ ЗНАЧЕНИЙ-------------------------------------------
    # -----------------------------------------Пока готовы: ------------------------------------------------------------
    # ----------------------------------Генератор timestamp ------------------------------------------------------------

    def __control_unical_ts(self, count):
        """
        Если у нас выствлен тэг , который ограничивает уникальность времени, то во всех элементах -
        меняем их по первлому значению - т.е по первому айдишнику
        :param count:
        :return:
        """

        return GeneratorTimestamp(count_ts=count).Timestamp

    # ----------------------------------Генератор device Idx------------------------------------------------------------
    def __control_unical_idx(self, count):
        """
        Если у нас выствлен тэг , который ограничивает уникальность айдишников , надо запускать эту функцию

        :param count:
        :return:
        """
        return GeneratorDeviceIdx(count_id=count).id

    # ------------------------------------------------------------------------------------------------------------------
    # вспомогательная функция для ограничения ts для конфигов

    def __limitation_in_quantity_ts_for_config(self, measure: str):
        if (measure in Template_list_ArchTypes.ElectricConfig_ArchType_name_list) or \
                (measure in Template_list_ArchTypes.PulseConfig_ArchType_name_list) or \
                (measure in Template_list_ArchTypes.DigitalConfig_ArchType_name_list):
            return True
        else:
            return False

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # генератор для типа данных - получаем список из возможных - выбираем из них указанное число
    def __generator_measure(self, count_measure: int):
        # Получаем возможное число возможных типов данных
        # count_measure = self.count_measure
        # Получаем все возможные значения
        ArchTypesName_dict = sqlite.readtable_return_dict(table_name='ArchTypes', collum='Name')
        for i in range(len(ArchTypesName_dict)):
            # Пихаем это все в массив
            ArchTypesName_dict[i] = ArchTypesName_dict[i]['Name']
        # теперь создает сет уникальных записей имен
        ArchTypesName_set = set()
        # в зависимости от нашей запрашиваемой длины формируем сет значений
        for i in range(count_measure):
            # берем максимальное число элементов
            max_len = len(ArchTypesName_dict) - 1
            # выбираем рандомно элемент по всей длине массива
            element = ArchTypesName_dict.pop(randint(0, max_len))
            # пихаем в сет
            ArchTypesName_set.add(element)
        return list(ArchTypesName_set)

    # --------------------------------------ДЕКОНСТРУКТОР---------------------------------------------------------------
    def __generate_deconstruct(self, list_vals: list, measures):
        list_vals_deconstruct = []
        for i in range(len(list_vals)):
            deconstruct = [measures] + list_vals[i]
            list_vals_deconstruct.append(deconstruct)
        return list_vals_deconstruct

    # --------------------------------------ДЕКОНСТРУКТОР для словаря---------------------------------------------------
    def __generate_deconstruct_dict(self, list_vals: list, measures):
        list_vals_deconstruct = []
        for i in range(len(list_vals)):
            dict_vals_deconstruct = {}
            dict_vals_deconstruct['Name'] = measures
            dict_vals_deconstruct.update(list_vals[i])
            # deconstruct = [measures] + list_vals[i]
            list_vals_deconstruct.append(dict_vals_deconstruct)
        return list_vals_deconstruct

    def get_deconstruct_json(self):
        return self.json_deconstruct

    def get_deconstruct_json_dict(self):
        return self.json_deconstruct_dict


