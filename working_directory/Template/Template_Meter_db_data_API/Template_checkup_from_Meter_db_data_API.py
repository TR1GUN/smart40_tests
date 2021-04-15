# А здесь расположим обработчик , да да  да
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from copy import deepcopy


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
class CheckUp:

    # //////
    def _checkup_element_certain_measure(self,
                                         # Наш JSON
                                         JSON_deconstruct,
                                         # Наша БД что записалось согласно JSON
                                         DataBase_was_recording
                                         ):
        """Стадия проверки конкретного типа данных"""
        error_list = []

        # Делаем коприю бд для проверки на нулевые значения
        self.database_for_checkup_NULL = deepcopy(DataBase_was_recording)
        for i in range(len(JSON_deconstruct)):
            # сравниваем ПОЭЛЕМЕНТНО
            error = self._checkup_json_with_database(JSON_Element=JSON_deconstruct[i],
                                                     database=DataBase_was_recording)
            error_list = error_list + error
        if len(error_list) == 0:
            # После чего очищаем нашу скоророванную БД от значений которые проверили

            error = self._check_up_null_values(database=self.database_for_checkup_NULL)
            error_list = error_list + error
        return error_list

    # ///--------------------------         ПОНИЖАЕМ УРОВЕНЬ АБСТРАКЦИИ     -------------------------------------------
    # ///--------------------------         ИЩЕМ ЭЛЕМЕНТ JSON ВО ВСЕЙ БД    -------------------------------------------
    def _checkup_json_with_database(self, JSON_Element, database):
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
                error = self._check_up_element_keys(data_base_element=database[i], JSON_element=JSON_Element)

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

    def _check_up_element_keys(self, data_base_element: dict, JSON_element: dict):
        """Сравнивание поэлементно """
        error = []
        error_keys = []
        # Сначала проверяем значения ответа
        for keys in data_base_element:
            # отбрасываем ключ diff
            if keys not in ['diff', 'Valid']:
                # Теперь сравниваем значения
                if keys in JSON_element:
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
                else:
                    error_string = {
                        'Ключа нет в БД': str(keys),
                        'Значение БД': data_base_element,
                        'Значение JSON': JSON_element,
                    }

                    # Добавляем это в ошибку , и добавляем наш ключ
                    error.append(error_string)

        for keys in JSON_element:
            # отбрасываем ключ diff
            if keys not in ['diff', 'Valid']:
                if keys not in error_keys:
                    # Теперь смотрим вхождения в нужный диапазон
                    if keys in data_base_element:
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
                    # Иначе отбрасываем ошибку - Не вхождения в нужный диапазон
                    else:
                        error_string = {
                            'Ключа нет в БД': str(keys),
                            'Значение БД': data_base_element,
                            'Значение JSON': JSON_element,
                        }

                        # Добавляем это в ошибку , и добавляем наш ключ
                        error.append(error_string)

        return error

    # ///--------------------------         ПОНИЖАЕМ УРОВЕНЬ АБСТРАКЦИИ     -------------------------------------------
    # ///--------------------------      СРАВНИВАЕМ ЭЛЕМЕННТ JSON и ЭЛЕМЕНТ БД    -------------------------------------
    def _check_up_null_values(self, database):
        """Здесь должны остаться только значения НУЛЕВЫЕ , ПОЭТОМУ ЕСЛИ ИНАЧЕ - ВЫБРАСЫВАЕМ ОШИБКУ"""
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


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# -------------------------------- Служебный класс для переопределения ТЭГОВ JSON -------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

class RedefinitionValuesTags:
    """
    В Этом классе переопределяем наши некоторые значения тэгов привендя их к тому значению как обычно записываюся

    """
    JSON_deconstruct_original = []
    JSON_deconstruct_redefinition = []

    def __init__(self, JSON_deconstruct):
        self.JSON_deconstruct_original = JSON_deconstruct
        self.JSON_deconstruct_redefinition = self.__Redefinition_values()

    def __Redefinition_values(self):
        from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes

        JSON_deconstruct_original = deepcopy(self.JSON_deconstruct_original)
        for i in range(len(JSON_deconstruct_original)):
            for x in range(len(JSON_deconstruct_original[i])):
                # Если это профиль мощности , то нулл значения переводим в нужный вид
                if JSON_deconstruct_original[i][x]['Name'] in Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list:
                    redefinition_tags = ['cTime', 'isPart', 'isOvfl', 'isSummer']
                    for tags in redefinition_tags:
                        # Если какое нибудь из этих значений в None то ставим 0
                        if JSON_deconstruct_original[i][x][tags] is None:
                            JSON_deconstruct_original[i][x][tags] = 0
                elif JSON_deconstruct_original[i][x]['Name'] in Template_list_ArchTypes.ElectricConfig_ArchType_name_list:
                    redefinition_tags_None = [ 'cArrays', 'isDst', 'isClock', 'isTrf',
                                            'isAm', 'isRm', 'isRp',]
                    for tags in redefinition_tags_None:
                        # Если какое нибудь из этих значений в None то ставим 0
                        if JSON_deconstruct_original[i][x][tags] is None:
                            JSON_deconstruct_original[i][x][tags] = 0
                    redefinition_tags_Void = ['serial', 'model',]
                    for tags in redefinition_tags_Void:
                        # Если какое нибудь из этих значений в None то ставим 0
                        if JSON_deconstruct_original[i][x][tags] is None:
                            JSON_deconstruct_original[i][x][tags] = ''
                elif JSON_deconstruct_original[i][x]['Name'] in Template_list_ArchTypes.PulseConfig_ArchType_name_list:
                    redefinition_tags_None = [ 'chnl', 'isDst']
                    for tags in redefinition_tags_None:
                        # Если какое нибудь из этих значений в None то ставим 0
                        if JSON_deconstruct_original[i][x][tags] is None:
                            JSON_deconstruct_original[i][x][tags] = 0
                    redefinition_tags_Void = ['serial', 'model',]
                    for tags in redefinition_tags_Void:
                        # Если какое нибудь из этих значений в None то ставим 0
                        if JSON_deconstruct_original[i][x][tags] is None:
                            JSON_deconstruct_original[i][x][tags] = ''

                elif JSON_deconstruct_original[i][x]['Name'] in Template_list_ArchTypes.DigitalConfig_ArchType_name_list:
                    redefinition_tags_None = [ 'chnlOut', 'chnlIn' ,  'isDst']
                    for tags in redefinition_tags_None:
                        # Если какое нибудь из этих значений в None то ставим 0
                        if JSON_deconstruct_original[i][x][tags] is None:
                            JSON_deconstruct_original[i][x][tags] = 0
                    redefinition_tags_Void = ['serial', 'model',]
                    for tags in redefinition_tags_Void:
                        # Если какое нибудь из этих значений в None то ставим 0
                        if JSON_deconstruct_original[i][x][tags] is None:
                            JSON_deconstruct_original[i][x][tags] = ''

                elif JSON_deconstruct_original[i][x]['Name'] in Template_list_ArchTypes.JournalValues_ArchType_name_list:
                    redefinition_tags = ['event', 'eventId']
                    for tags in redefinition_tags:
                        # Если какое нибудь из этих значений в None то ставим 0
                        if JSON_deconstruct_original[i][x][tags] is None:
                            JSON_deconstruct_original[i][x][tags] = 0

        return JSON_deconstruct_original


# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# -----------------------------Напишем здесь сравниватель для запроса GET----------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

class GETCheckUP(CheckUp):
    """
        Класс для проверки для GET запроса

    """
    dublicate = None
    error_collector = None

    def __init__(self, JSON_deconstruct, DataBase_select):
        """

        Класс для проверки для GET запроса

        :param JSON_deconstruct: Наш деконструированный JSON
        :param DataBase_select:  Что заселектили в Базе данных

        """

        # Переопределяем поля
        self.error_collector = []

        self.JSON_deconstruct = JSON_deconstruct

        self.DataBase_select = DataBase_select

        # Проверяем количество элементов

        # print('self.JSON_deconstruct',self.JSON_deconstruct)
        # print('self.DataBase_select', self.DataBase_select)

        self.__checkUP_len()

        # Если не нашли ошибок , продолжаем дальше
        if len(self.error_collector) == 0:
            result = self.__checkUP_element()

    def __checkUP_len(self):
        """
        сначла проверяем по длине
        :return:
        """
        # Если у нас они не равны по длине - Добавляем ошибку

        if len(self.JSON_deconstruct) != len(self.DataBase_select):
            if len(self.JSON_deconstruct) > len(self.DataBase_select):
                result = len(self.JSON_deconstruct) - len(self.DataBase_select)
                self.error_collector.append({
                    'error': 'Данных в полученном JSON больше, чем чем в получили из БД на ' + str(result),
                    'JSON': self.JSON_deconstruct,
                    'DataBase': self.DataBase_select
                })

        if len(self.JSON_deconstruct) < len(self.DataBase_select):
            result = len(self.DataBase_select) - len(self.JSON_deconstruct)
            self.error_collector.append({
                'error': 'Данных в полученном JSON меньше, чем чем в получили из БД на ' + str(result),
                'JSON': self.JSON_deconstruct,
                'DataBase': self.DataBase_select

            })

        # Теперь проверяем по элементно

    def __checkUP_element(self):

        # Делаем копии для манипуляций
        JSON_deconstruct = []
        for i in range(len(self.JSON_deconstruct)):
            JSON_deconstruct.append(self.JSON_deconstruct[i])
        DataBase_select = []
        for i in range(len(self.DataBase_select)):
            DataBase_select.append(self.DataBase_select[i])
        # Теперь по элементно перебираем массив
        for i in range(len(JSON_deconstruct)):
            if JSON_deconstruct[i] not in DataBase_select:
                self.error_collector.append({
                    'error': 'Элемента JSON нет в полученом массиве из БД ',
                    'JSON_element': str(JSON_deconstruct[i]),
                    'DataBase_select': str(DataBase_select)
                })
            # Если он находится, то сравниваем по элементно
            else:
                # получаем индекс элмента вхождения
                x = DataBase_select.index(JSON_deconstruct[i])
                # теперь по ключам сравниваем их

                error_collector = self.__checkUP_element_key(JSON_dict=DataBase_select[x],
                                                             DataBase_select_dict=JSON_deconstruct[i])

                # Если у нас все нормально - Удаляем этот элемент
                if len(error_collector) == 0:
                    delete = DataBase_select.pop(x)
        return self.error_collector

    def __checkUP_element_key(self, JSON_dict, DataBase_select_dict):
        """
        Сравниваем по ключам все что есть

        :param JSON_dict: словарь JSON
        :param DataBase_select_dict:  словарь из БД
        :return:
        """
        for key in JSON_dict:
            if JSON_dict[key] != DataBase_select_dict[key]:
                self.error_collector.append({

                    'error': 'Значение элемента JSON не совпадает со значением из БД',
                    'JSON_dict': str(JSON_dict),
                    'DataBase_select_dict': str(DataBase_select_dict)

                })

        return self.error_collector


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# -----------------------------Напишем здесь сравниватель для запроса POST---------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

class POSTCheckUP(CheckUp):
    """
        Класс для проверки для POST запроса
    """
    dublicate = []
    error_collector = []
    JSON_deconstruct = []
    DataBase_before = []
    DataBase_after = []
    DataBase_was_recording = []
    tags = ['Name', 'id', 'ts']

    def __init__(self,
                 JSON_deconstruct: list,
                 DataBase_before: list,
                 DataBase_after: list,
                 DataBase_was_recording: list):
        # Итак - Переопределяем Поля - ЕТО ВАЖНО

        self.JSON_deconstruct = deepcopy(RedefinitionValuesTags(JSON_deconstruct).JSON_deconstruct_redefinition)
        self.DataBase_before = DataBase_before

        self.DataBase_after = DataBase_after
        self.DataBase_was_recording = DataBase_was_recording

        # Пункт Первый - Удаляем из JSON все то что не должног было записаться
        self.JSON_deconstruct = self.__checkup_to_void()

        # Проверяем валидность
        self.error_collector = self.error_collector + self.__checkup_field_valid()

        # после переопределения полей - делаем сравнение
        self.error_collector = self.error_collector + self.__checkup_archtype_name()

    # ---------------------------------- УРОВЕНЬ АБСТРАЦИИ 1 - Проверка всех типов данных ----------------------
    def __checkup_archtype_name(self):
        '''Стадия проверки - 1  - проверяем что мы получили все типы данных в наборах'''
        error_collector = []

        # Теперь надо проверить их длину - их длина должна быть одинакова - потому что нам нужны все archtypes name
        if (len(self.JSON_deconstruct) == len(self.DataBase_before)) and \
                (len(self.JSON_deconstruct) == len(self.DataBase_after)) and \
                (len(self.JSON_deconstruct) == len(self.DataBase_was_recording)):
            # Если все ок - отправляем в следующую функцию стравнивания

            error_collector = self.__checkup_element_brute_measures()
        else:
            error_collector.append({'error': 'Нет соответсвия archtypes name'})

        return error_collector

    # ---------------------------------Понимажаем уровень абстрацкции -----------------------------------------------------
    # ---------------------------------- УРОВЕНЬ АБСТРАЦИИ 2 - Проверка конкретного типа данных ----------------------
    def __checkup_element_brute_measures(self):
        """Стадия проверки 2 - Перебираем все типы данных """
        error_collector = []

        for i in range(len(self.JSON_deconstruct)):
            # Теперь сюда пихаем ошибки на конкретный тип данных
            error_collector = error_collector + self.__checkup_element_certain_measure(
                JSON_deconstruct=self.JSON_deconstruct[i],
                DataBase_before=self.DataBase_before[i],
                DataBase_after=self.DataBase_after[i],
                DataBase_was_recording=self.DataBase_was_recording[i]
            )

        return error_collector

    # ---------------------------------Понимажаем уровень абстрацкции -----------------------------------------------------
    # ---------------------------------- УРОВЕНЬ АБСТРАЦИИ 3 - Проверка массива конкретного типа данных -------------------
    def __checkup_element_certain_measure(self,
                                          # Наш jSON Ответа
                                          JSON_deconstruct,
                                          # Наша БД до записи
                                          DataBase_before,
                                          # Наша БД После Записи
                                          DataBase_after,
                                          # Наша БД что записалось согласно JSON
                                          DataBase_was_recording):
        """Стадия проверки конкретного типа данных"""
        error = []
        # print('\n--------------------------')
        # print('JSON_deconstruct', JSON_deconstruct)
        # print('DataBase_before', DataBase_before)
        # print('DataBase_after', DataBase_after)
        # print('DataBase_was_recording', DataBase_was_recording)

        # Теперь первое что делаем - Получаем разницу что записалось по факту
        DataBase_after_the_fact = self.__getting_recording_record_after_fact(DataBase_after=DataBase_after,
                                                                             DataBase_before=DataBase_before)
        # print('----------------------')
        # print(DataBase_after_the_fact)

        # Делаем коприю бд для проверки на нулевые значения
        self.database_for_checkup_NULL = deepcopy(DataBase_after_the_fact)

        # Сравниваем по длине того что получили

        # НАЧИНАЕМ СРАВНЕНИЕ
        # Пункт Первый - Сравнение Того что записано по факту и тем что записали по Селекиту

        if len(DataBase_was_recording) == len(DataBase_after_the_fact):
            for i in range(len(DataBase_after_the_fact)):
                if DataBase_after_the_fact[i] not in DataBase_was_recording:
                    error = error + \
                            [{
                                "ОШИБКА": 'Нет Элемента В селекте по айдишникам в Наборе элементов записанных по факту',
                                'DataBase_was_recording - о что Взяли ИЗ Бд и должно было быть записанное': DataBase_was_recording,
                                'DataBase_after_the_fact - Что записано по факту - Разница между БД До и После записи': DataBase_after_the_fact
                            }]

        else:
            error = error + [{
                "ОШИБКА": 'Записанное по факту , не совпадает взяли из БД по ID',
                'DataBase_was_recording - о что Взяли ИЗ Бд и должно было быть записанное': DataBase_was_recording,
                'DataBase_after_the_fact - Что записано по факту - Разница между БД До и После записи': DataBase_after_the_fact
            }]

        # ТЕПЕРЬ _ СРАВНИВАЕМ НАШ JSON и с тем что заселектили по факту.
        if len(JSON_deconstruct) == len(DataBase_was_recording):
            for i in range(len(JSON_deconstruct)):
                error = self._checkup_json_with_database(JSON_Element=JSON_deconstruct[i],
                                                         database=DataBase_was_recording)

            if len(error) == 0:
                # После чего очищаем нашу скоророванную БД от значений которые проверили
                error = error + self._check_up_null_values(database=self.database_for_checkup_NULL)
        else:
            error = error + [{
                "ОШИБКА": 'Записанное в БД , Не совпадает с JSON по длине. Что то потерялось',
                'JSON_deconstruct - Наш JSON': JSON_deconstruct,
                'DataBase_was_recording - То что записанно в БД ': DataBase_was_recording
            }]

        return error

    # //------------------СЛУЖЕБНАЯ ФУНКЦИЯ _ ЧТО ЗАПСИАЛОАСЬ ПО ФАКТУ---------------------------------------------------

    def __getting_recording_record_after_fact(self, DataBase_after, DataBase_before):
        """Здесь получаем то, что записали по факту в ТАблицу"""
        DataBase_after_the_fact = []
        for i in range(len(DataBase_after)):
            DataBase_after_the_fact.append(DataBase_after[i])

        # Теперь удаляем все то что было записанно
        for i in range(len(DataBase_after)):
            if DataBase_after[i] in DataBase_before:
                DataBase_after_the_fact.remove(DataBase_after[i])
        return DataBase_after_the_fact

    # ---------------------------------------------------------------------------------------------------------------------
    #                             Итак - Здесь идет проверка валидности
    # ---------------------------------------------------------------------------------------------------------------------
    def __checkup_field_valid(self):
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!НАдо ДОПИСАТЬ проверку валидности!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        error = []
        database_was_recording = self.DataBase_was_recording

        for i in range(len(database_was_recording)):

            for x in range(len(database_was_recording[i])):
                if database_was_recording[i][x].get('Name') not in (
                        Template_list_ArchTypes.ElectricConfig_ArchType_name_list +
                        Template_list_ArchTypes.DigitalConfig_ArchType_name_list +
                        Template_list_ArchTypes.PulseConfig_ArchType_name_list
                ):

                    # Сначала Обрабатываем вариант , если валид равен 1 или 0 :
                    if database_was_recording[i][x].get('Valid') in [1, 0]:
                        # Так - Поле Валид не равно 1 , то проверяем  что у нас в JSON
                        for keys in database_was_recording[i][x]:
                            if keys not in ['Name', 'id', 'Valid', 'ts']:
                                # Если у нас есть лишний ключ
                                if database_was_recording[i][x].get('Valid') != 1:
                                    error = error + [
                                        {
                                            'error': 'Поле Valid приняло не правильное значение',
                                            'Элемент где записанно не правильно - ': database_was_recording[i][x],
                                        }
                                    ]
                    else:
                        error = error + [
                            {
                                'error': 'Поле Valid приняло не правильное значение',
                                'Элемент где записанно не правильно - ': database_was_recording[i][x],
                                'Само поле Valid': database_was_recording[i][x].get('Valid')
                            }
                        ]
        return error

    # ----------------------------------------------------------------------------------------------------------------
    def __checkup_to_void(self):
        """Здесб проверяем наш JSON на наличие пустоты - и удаляем то что не должно было записываться"""
        # Определяем Тэги категорий
        none_dict_etalon = {
            'tarif0': ['A+0', 'A-0', 'R+0', 'R-0'],
            'tarif1': ['A+1', 'A-1', 'R+1', 'R-1'],
            'tarif2': ['A+2', 'A-2', 'R+2', 'R-2'],
            'tarif3': ['A+3', 'A-3', 'R+3', 'R-3'],
            'tarif4': ['A+4', 'A-4', 'R+4', 'R-4'],

            'phaseA': ['UA', 'IA', 'PA', 'QA', 'SA', 'kPA', 'AngAB'],
            'phaseB': ['UB', 'IB', 'PB', 'QB', 'SB', 'kPB', 'AngBC'],
            'phaseC': ['UC', 'IC', 'PC', 'QC', 'SC', 'kPC', 'AngAC'],
            'phaseSum': ['PS', 'QS', 'SS', 'kPS', 'Freq'],
            'ConsPower': ['P+', 'Q+', 'P-', 'Q-'],
            'Pulse' : ['Pls1', 'Pls2', 'Pls3', 'Pls4', 'Pls5', 'Pls6', 'Pls7', 'Pls8', 'Pls9', 'Pls10', 'Pls11', 'Pls12',
                    'Pls13', 'Pls14', 'Pls15', 'Pls16', 'Pls17', 'Pls18', 'Pls19', 'Pls20', 'Pls21', 'Pls22', 'Pls23',
                    'Pls24', 'Pls25', 'Pls26', 'Pls27', 'Pls28', 'Pls29', 'Pls30', 'Pls31', 'Pls32'],
            'Digital': ['Chnl1', 'Chnl2', 'Chnl3', 'Chnl4', 'Chnl5', 'Chnl6', 'Chnl7', 'Chnl8', 'Chnl9',
                                 'Chnl10',
                                 'Chnl11', 'Chnl12', 'Chnl13', 'Chnl14', 'Chnl15', 'Chnl16', 'Chnl17', 'Chnl18',
                                 'Chnl19', 'Chnl20',
                                 'Chnl21', 'Chnl22', 'Chnl23', 'Chnl24', 'Chnl25', 'Chnl26', 'Chnl27', 'Chnl28',
                                 'Chnl29', 'Chnl30',
                                 'Chnl31', 'Chnl32'],

            # 'Journal' : ['event', 'eventId',]
        }

        # Теперь перебираем все возможные комбинации по типам данных
        for i in range(len(self.JSON_deconstruct)):
            # Перебираем по айдишникам и их таймштампам
            for x in range(len(self.JSON_deconstruct[i])):
                # Теперь перебираем нащи КЛЮЧИ ОПРЕДЕЛЕННОГО СЛОВАРЯ

                none_dict = deepcopy(none_dict_etalon)
                for keys_for_tag in self.JSON_deconstruct[i][x]:

                    # Игнорируем наши тэги по умолчанию
                    if keys_for_tag not in ['Name', 'id', 'Valid', 'ts']:

                        # Теперь Ищем НУЛЛ значения в нашем тэге
                        if self.JSON_deconstruct[i][x][keys_for_tag] is None:
                            # Если он пустой - то ищем его в нашей копии
                            for category in none_dict:
                                if keys_for_tag in none_dict[category]:
                                    # Удаляем его
                                    none_dict[category].pop(none_dict[category].index(keys_for_tag))
                # ТЕПЕРЬ - смотрим - какие из категорий остались пустые
                for category in none_dict:
                    # Если категория пуста - то получаем все тэги категории
                    if len(none_dict[category]) == 0:
                        tags_list = deepcopy(none_dict_etalon)
                        # Обновляем чтоб удалить все что есть
                        tags_list.update(
                            {'ConsPower': ['cTime', 'P+', 'Q+', 'P-', 'Q-', 'isPart', 'isOvfl', 'isSummer']}
                        )
                        tags_list = tags_list[category]
                        # Теперь проходимся по листу - и удаляем все эти тэги из элемента JSON
                        for name_tag in tags_list:
                            self.JSON_deconstruct[i][x].pop(name_tag)
        return self.JSON_deconstruct
# ---------------------------------------------------------------------------------------------------------------------
