# Сдесь сделаем наш алгоритм сравнения для Meter Daemon
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from copy import deepcopy


# ---------------------------------------------------------------------------------------------------------------------
#                         Здесь расположем главный класс сравнивания - Это важно !!!
# ---------------------------------------------------------------------------------------------------------------------


class CheckUP:
    """
        Класс для проверки для Meter Daemon
    """
    dublicate = []
    error_collector = []
    JSON_deconstruct = []
    database_before = []
    database_after = []
    DataBase_was_recording = []
    DataBase_after_the_fact = []
    tags = ['Name', 'id', 'ts']

    def __init__(self, JSON_deconstruct: list,
                 DataBase_was_recording: list,
                 # database_before: list,
                 # database_after: list,
                 ):

        # Итак - Переопределяем Поля - ЕТО ВАЖНО
        self.JSON_deconstruct = self.__Normalise_data(JSON_deconstruct)
        # self.DataBase_was_recording = self.__Normalise_data(DataBase_was_recording)
        # self.database_before = self.__Normalise_data(database_before)
        # self.database_after = self.__Normalise_data(database_after)
        self.DataBase_after_the_fact = self.__Normalise_data(DataBase_was_recording)

        if len(self.JSON_deconstruct) > 0:
            # self.DataBase_after_the_fact = self.__getting_recording_record_after_fact(
            #     DataBase_after=self.database_after,
            #     DataBase_before=self.database_before)

            # Теперь достраиваем JSON
            self.JSON_deconstruct = self.__Rewrite_JSON()
            # Првоеряем валидность
            self.error_collector = self.error_collector + self.__checkup_field_valid()

            # после переопределения полей - делаем сравнение
            self.error_collector = self.error_collector + self.__checkup_archtype_name()

    def __checkup_archtype_name(self):
        '''Стадия проверки - 1  - проверяем что мы получили все типы данных в наборах'''
        error_collector = []

        # Теперь надо проверить их длину - их длина должна быть одинакова - потому что нам нужны все archtypes name
        if (len(self.JSON_deconstruct) == len(self.DataBase_after_the_fact)):
            # Если все ок - отправляем в следующую функцию стравнивания

            error_collector = self.__checkup_element_brute_measures()
        else:
            error_collector.append({'error': 'Нет соответсвия archtypes name'})

        return error_collector

    def __checkup_element_brute_measures(self):
        """Стадия проверки 2 - Перебираем все типы данных """
        error_collector = []

        for i in range(len(self.JSON_deconstruct)):
            # Теперь сюда пихаем ошибки на конкретный тип данных
            error_collector = error_collector + self.__checkup_element_certain_measure(
                JSON_deconstruct=self.JSON_deconstruct[i],
                DataBase_was_recording=self.DataBase_after_the_fact[i]
            )

        return error_collector

    # //////
    def __checkup_element_certain_measure(self,
                                          # Наш JSON Ответа
                                          JSON_deconstruct,
                                          # Наша БД что записалось согласно JSON
                                          DataBase_was_recording
                                          ):
        """Стадия проверки конкретного типа данных"""
        error_list = []

        # print('JSON_deconstruct', JSON_deconstruct)
        # print('DataBase_was_recording', DataBase_was_recording)
        # Сравниваем по длине того что получили

        # НАЧИНАЕМ СРАВНЕНИЕ
        # Пункт Первый - Сравнение Того что записано по факту и тем что записали по Селекиту

        # ТЕПЕРЬ _ СРАВНИВАЕМ НАШ JSON и с тем что заселектили по факту.
        # Делаем коприю бд для проверки на нулевые значения
        self.database_for_checkup_NULL = deepcopy(DataBase_was_recording)
        for i in range(len(JSON_deconstruct)):
            # сравниваем ПОЭЛЕМЕНТНО
            error = self.__checkup_json_with_database(JSON_Element=JSON_deconstruct[i],
                                                      database=DataBase_was_recording)
            error_list = error_list + error
        if len(error_list) == 0:
            # После чего очищаем нашу скоророванную БД от значений которые проверили

            error = self.__check_up_null_values(database=self.database_for_checkup_NULL)
            error_list = error_list + error
        return error_list

    # ///--------------------------         ПОНИЖАЕМ УРОВЕНЬ АБСТРАКЦИИ     -------------------------------------------
    # ///--------------------------         ИЩЕМ ЭЛЕМЕНТ JSON ВО ВСЕЙ БД    -------------------------------------------
    def __checkup_json_with_database(self, JSON_Element, database):
        '''Итак - Здесь приводим сравнивание JSON по ключаем '''
        # Итак = Перебираем нашу БД
        error_list = []
        element_id = None
        element_ts = None

        # Делаем коприю бд для проверки на нулевые значения


        for i in range(len(database)):
            # Ищем здесь две связки - таймштамп и айди
            JSON_Element['id'] = int(JSON_Element['id'])
            database[i]['id'] = int(database[i]['id'])
            JSON_Element['ts'] = int(JSON_Element['ts'])
            database[i]['ts'] = int(database[i]['ts'])

            if (int(JSON_Element['id']) == int(database[i]['id'])) and (
                    int(JSON_Element['ts']) == int(database[i]['ts'])):
                # Если мы нашли нужный таймштамп нужного айдишника - Продолжаем

                # здесь сравниваем уже конкретные значения нашего полученного JSON c Записью
                error = self.__check_up_element_keys(data_base_element=database[i], JSON_element=JSON_Element)

                self.database_for_checkup_NULL.remove(database[i])
                error_list = error_list + error

            if JSON_Element['id'] == database[i]['id']:
                element_id = i

            if JSON_Element['ts'] == database[i]['ts']:
                element_ts = i

            # Если не нашли нужный Элемент
        if element_id is None:
            error_list = error_list + [{'Не удалось найти Элемент JSON id ': JSON_Element['id'],
                                        'JSON_Element': JSON_Element,
                                        'То что записали в БД': database}]
        if element_ts is None:
            error_list = error_list + [{'Не удалось найти Элемент JSON ts ': JSON_Element['ts'],
                                        'JSON_Element': JSON_Element,
                                        'То что записали в БД': database}]
        # Теперь првоеряем что все показатели стоят в null

        return error_list

    # ///--------------------------         ПОНИЖАЕМ УРОВЕНЬ АБСТРАКЦИИ     -------------------------------------------
    # ///--------------------------      СРАВНИВАЕМ ЭЛЕМЕННТ JSON и ЭЛЕМЕНТ БД    -------------------------------------

    def __check_up_element_keys(self, data_base_element: dict, JSON_element: dict):
        """Сравнивание поэлементно """
        error = []
        error_keys = []
        # Сначала проверяем значения ответа
        for keys in data_base_element:
            # отбрасываем ключ diff
            if keys not in ['diff', 'Valid']:
                # Теперь сравниваем значения
                data_base_value = data_base_element.get(keys)
                JSON_value = JSON_element.get(keys)

                # Теперь проверяем их равнество

                if (type(JSON_value) == float) and (type(data_base_value) == float):

                    epsilon = 5.96e-08

                    # if abs(normal_value / answer_value - 1) > epsilon:
                    if abs(JSON_value - data_base_value) > epsilon:
                        error_string = {
                            'Неравенство значений Ключа': str(keys),
                            'Значение ключа в БД': data_base_value,
                            'Значение ключа в   JSON ': JSON_value
                        }

                        # Добавляем это в ошибку , и добавляем наш ключ
                        error.append(error_string)
                        error_keys.append(keys)
                else:
                    if data_base_value != JSON_value:
                        error_string = {
                            'Неравенство значений Ключа': str(keys),
                            'Значение ключа JSON ': JSON_value,
                            'Значение ключа в БД': data_base_value
                        }
                        # Добавляем это в ошибку , и добавляем наш ключ
                        error.append(error_string)
                        error_keys.append(keys)

        for keys in JSON_element:
            # отбрасываем ключ diff
            if keys not in ['diff', 'Valid']:
                if keys not in error_keys:
                    # Теперь сравниваем значения
                    data_base_value = data_base_element.get(keys)
                    JSON_value = JSON_element.get(keys)

                    # Теперь проверяем их равнество

                    if (type(JSON_value) == float) or (type(data_base_value) == float):
                        epsilon = 5.96e-08
                        # if abs(normal_value / answer_value - 1) > epsilon:
                        if abs(JSON_value - data_base_value) > epsilon:
                            error_string = {
                                'Неравенство значений Ключа': str(keys),
                                'Значение ключа в JSON ': JSON_value,
                                'Значение ключа в БД': data_base_value
                            }

                            # Добавляем это в ошибку , и добавляем наш ключ
                            error.append(error_string)

                    else:
                        if data_base_value != JSON_value:
                            error_string = {
                                'Неравенство значений Ключа': str(keys),
                                'Значение ключа в JSON ': JSON_value,
                                'Значение ключа в БД': data_base_value
                            }

                            # Добавляем это в ошибку , и добавляем наш ключ
                            error.append(error_string)
        return error

    # ///--------------------------         ПОНИЖАЕМ УРОВЕНЬ АБСТРАКЦИИ     -------------------------------------------
    # ///--------------------------      СРАВНИВАЕМ ЭЛЕМЕННТ JSON и ЭЛЕМЕНТ БД    -------------------------------------
    def __check_up_null_values(self, database):
        """Здесь должны остаться только зеначения НУЛЕВЫЕ , ПОЭТОМУ ЕСЛИ ИНАЧЕ - ВЫБРАСЫВАЕМ ОШИБКУ"""
        error_list = []
        for i in range(len(database)):
            for key in database[i].keys():
                if key not in ['Name', 'id', 'ts', 'Valid']:
                    # ЕСЛИ ЗНАЧЕНИЕ НЕ НУЛЕВОЕ _ ВЫБРАСЫВАЕМ ОШИБКУ
                    if database[i][key] is not None:
                        error = [{'Не None ЗНАЧЕНИЯ КЛЮЧА ' + key: database[i][key], 'Элемент БД - ': database[i],
                                  "ЭЛЕМЕНТ Time": database['ts']}]
                        error_list = error_list + error
        return error_list

    def __checkup_field_valid(self):
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Нaдо ДОПИСАТЬ проверку валидности!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        error = []
        database_was_recording = self.DataBase_after_the_fact
        for element in range(len(database_was_recording)):
            if len(database_was_recording[element]) > 0:

                if (database_was_recording[0][0].get('Name') not in (
                        Template_list_ArchTypes.ElectricConfig_ArchType_name_list +
                        Template_list_ArchTypes.DigitalConfig_ArchType_name_list +
                        Template_list_ArchTypes.PulseConfig_ArchType_name_list)):
                    for i in range(len(database_was_recording)):
                        for x in range(len(database_was_recording[i])):
                            if database_was_recording[i][x]['Valid'] != 1:
                                error = error + [
                                    {
                                        'error': 'Поле Valid приняло не правильное значение',
                                        'Элемент где записанно не правильно - ': database_was_recording[i]
                                    }
                                ]
            else:
                error = error + [
                    {
                        'error': 'НИЧЕГО НЕ ЗАПИСАНО БД ПУСТАЯ'
                    }
                ]

        return error

    # ----------------------------------------------------------------------------------------------------------------
    def __Normalise_data(self, element):
        """
        Метод ждя нормализции данных - Перевод в инт айдишников и таймштампов
        """
        for i in range(len(element)):
            for x in range(len(element[i])):
                element[i][x]['id'] = int(element[i][x]['id'])
                element[i][x]['ts'] = int(element[i][x]['ts'])

        return element

    # ----------------------------------------------------------------------------------------------------------------
    def __Rewrite_JSON(self):

        """
        Здесь перезаписываем наши Значения JSON
        :return:
        """
        from Emulator.Counters.Config_settings import get_time
        # Теперь определяем что это за тип данных - Архивный или Моментный
        from working_directory.Template.Template_Meter_devices_API.Template_generator_time import \
            measure_containin_day_list, measure_containin_month_list, \
            measure_containin_half_hour_list, measure_containin_hour_list
        archive_measure = measure_containin_day_list + \
                          measure_containin_month_list + \
                          measure_containin_half_hour_list + \
                          measure_containin_hour_list

        JSON = self.JSON_deconstruct

        for i in range(len(JSON)):
            # Если это моментный показатель , то перезаписываем
            if JSON[i][0]['Name'] not in archive_measure:
                # Перезаписываем таймштамп
                # Берем таймштамп
                timestamp = get_time()
                for x in range(len(JSON[i])):
                    JSON[i][x]['ts'] = timestamp

        return JSON
