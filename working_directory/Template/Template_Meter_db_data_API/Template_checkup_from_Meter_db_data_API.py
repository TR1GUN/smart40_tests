# А здесь расположим обработчик , да да  да
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

class CheckUP:
    """
    Класс для проверки что есть в базе данных и что в итоге мы получили

    """
    dublicate = None
    error_collector = None
    tags = None

    def __init__(self):
        self.error_collector = None
        self.tags = []

    # ---------------------------------Вспомогательные функции - старые ------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    #     Вспомомгательная функция расчета каждого из элементов
    def __checkup_list_element_value_ArchType_Name(self, database_before: list,
                                                   database_after: list,
                                                   database_was_recording: list,
                                                   json_content: list):

        result_total = []
        # Теперь берем расчет по каждому из элементов
        for i in range(len(json_content)):
            # а теперь каждый элемент пихаем в сравниватель
            result = self.__checkup_by_element_ArchType_Name(database_after=database_after[i],
                                                             database_before=database_before[i],
                                                             database_was_recording=database_was_recording[i],
                                                             json_content=json_content[i]
                                                             )

            if len(result) != 0:
                result_total.append(result)

        return result_total

    # ---------------------------------------------------------------------------------------------------------------------
    #     В этой функции сравниваем каждый элемент
    def __checkup_by_element_ArchType_Name(self,
                                           database_before: list,
                                           database_after: list,
                                           database_was_recording: list,
                                           json_content: list):
        result = []
        # Первое что должны сделать - определиться с тэгом что лежит  в Name
        # и исходя из него составляем лист тэгов что содержится в нем
        archtype_name = json_content[0]['Name']

        if archtype_name in Template_list_ArchTypes.ElectricConfig_ArchType_name_list:
            tags_name = Template_list_ArchTypes.ElectricConfig_tag
        elif archtype_name in Template_list_ArchTypes.PulseConfig_ArchType_name_list:
            tags_name = Template_list_ArchTypes.PulseConfig_tag
        elif archtype_name in Template_list_ArchTypes.DigitalConfig_ArchType_name_list:
            tags_name = Template_list_ArchTypes.DigitalConfig_tag
        elif archtype_name in Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list:
            tags_name = Template_list_ArchTypes.ElecticEnergyValues_tag
        elif archtype_name in Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list:
            tags_name = Template_list_ArchTypes.ElectricQualityValues_tag
        elif archtype_name in Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list:
            tags_name = Template_list_ArchTypes.ElectricPowerValues_tag
        elif archtype_name in Template_list_ArchTypes.PulseValues_ArchType_name_list:
            tags_name = Template_list_ArchTypes.PulseValues_tag
        elif archtype_name in Template_list_ArchTypes.DigitalValues_ArchType_name_list:
            tags_name = Template_list_ArchTypes.DigitalValues_tag
        elif archtype_name in Template_list_ArchTypes.JournalValues_ArchType_name_list:
            tags_name = Template_list_ArchTypes.JournalValues_tag

        # Иначе - отбрасываем ошибку
        else:
            result = [{'error': 'Неправильно сформированно archtypes name'}]

        # После этого - проверяем на дубликаты , и отправляем в сравниватель
        if len(result) == 0:
            # Если нет ошибок то Добаввляем нужные тэги
            tags_name = ['id', 'ts'] + tags_name

            #  запускаем нашу функцию сравнивания
            result = self.__function_checkup_line(database_after_list=database_after,
                                                  database_before_list=database_before,
                                                  database_was_recording_list=database_was_recording,
                                                  json_content_list=json_content,
                                                  tags_list=tags_name)

        return result

    # ---------------------------------------------------------------------------------------------------------------------
    #     функция слепливания нужных значений в единый стринг по ключу
    def __concatenation_of_key_values_to_str(self, dict_list: list, name_key: list):

        value_str_set = set()

        for i in range(len(dict_list)):
            # Шаблон слепливания:
            value_dict = ''
            for x in range(len(name_key)):
                value_dict = str(value_dict) + str(' , ') + str(name_key[x]) + str(' : ') + str(
                    dict_list[i][name_key[x]])
            # и добавляем в множество
            value_str_set.add(value_dict)
        return value_str_set

    # ---------------------------------------------------------------------------------------------------------------------
    #    А это самая главная функция сравнивания
    def __function_checkup_line(self,
                                database_before_list: list,
                                database_after_list: list,
                                database_was_recording_list: list,
                                json_content_list: list,
                                tags_list: list):

        # Включаем обработчик ошибок
        error_collector = []
        # В начале все превращаем в сеты:
        database_before_set = self.__concatenation_of_key_values_to_str(dict_list=database_before_list,
                                                                        name_key=tags_list)

        database_after_set = self.__concatenation_of_key_values_to_str(dict_list=database_after_list,
                                                                       name_key=tags_list)

        database_was_recording_set = self.__concatenation_of_key_values_to_str(dict_list=database_was_recording_list,
                                                                               name_key=tags_list)

        json_content_set = self.__concatenation_of_key_values_to_str(dict_list=json_content_list,
                                                                     name_key=tags_list)
        # Теперь проверяем на дубликаты :
        if (len(database_before_set) != len(database_before_list)) and \
                (len(database_after_set) != len(database_after_list)) and \
                (len(database_was_recording_set) != len(database_was_recording_list)) and \
                (len(json_content_set) != len(json_content_list)):
            error_collector.append({"error": 'Записанны дубликаты: '})

        # Теперь начинаем сравнивать эты сеты
        # Получаем разницу сетов

        database_expect_was_recording_set = database_after_set - database_before_set

        # теперь посмотрим - равно ли то что записали JSON что отправили на запись
        if (database_was_recording_set == json_content_set):

            if (database_expect_was_recording_set == database_was_recording_set):

                if len(database_expect_was_recording_set - json_content_set) != 0:
                    result = database_expect_was_recording_set - json_content_set
                    error_collector.append({"error": 'Записанные значения больше чем значения JSON. Лишние значения: ',
                                            'numper': result,
                                            'numper json': json_content_set - database_expect_was_recording_set})
            else:
                result = database_expect_was_recording_set - database_was_recording_set
                error_collector.append({"error": 'Записанные значения не равны запсианным по селекту,значения: ',
                                        'numper': result})
        else:
            result = database_expect_was_recording_set - json_content_set
            error_collector.append({
                "error": 'Данные что отправили на запись не равны тому что записались, неправильно записанные значения',
                'numper': result,
                'numper jSON': json_content_set - database_expect_was_recording_set})
        return error_collector

    # ---------------------------------------------------------------------------------------------------------------------
    # # для начала получим наши данные - нам нужны БД до , БД после , БД что было записанно , и контент джейсона в формате бд
    # def checkup_post_old(self, database_before: list, database_after: list, database_was_recording: list,
    #                      json_content: list):
    #     # Обновим значение сборщика ошибок - теперь это пустой массив
    #     self.error_collector = []
    #     # Теперь надо проверить их длину - их длина должна быть одинакова - потому что нам нужны все archtypes name
    #
    #     if (len(json_content) == len(database_before)) and \
    #             (len(json_content) == len(database_after)) and \
    #             (len(json_content) == len(database_was_recording)):
    #         # Если они одинаковы , то тогда надо проходится по каждому из списка
    #         #     определяем тэги
    #         self.tags = ['Name', 'id', 'ts']
    #
    #         self.error_collector = self.__checkup_list_element_value_ArchType_Name(database_before=database_before,
    #                                                                                database_after=database_after,
    #                                                                                database_was_recording=database_was_recording,
    #                                                                                json_content=json_content)
    #
    #     else:
    #         # Если они не раавны то добавляем ошибку
    #
    #         self.error_collector.append({'error': 'Нет соответсвия archtypes name'})
    #     return self.error_collector

    # ----------------------------------------------------------------------------------------------------------------
    #                             все хуйня миша , давай по новой
    # ----------------------------------------------------------------------------------------------------------------

    def checkup_post(self,
                     database_before: list,
                     database_after: list,
                     database_was_recording: list,
                     json_content: list):
        # Обновим значение сборщика ошибок - теперь это пустой массив
        self.error_collector = []
        # Теперь надо проверить их длину - их длина должна быть одинакова - потому что нам нужны все archtypes name
        if (len(json_content) == len(database_before)) and \
                (len(json_content) == len(database_after)) and \
                (len(json_content) == len(database_was_recording)):
            # Если они одинаковы , то тогда надо проходится по каждому из списка
            #     определяем тэги
            self.tags = ['Name', 'id', 'ts']

            # Если все ок - отправляем в следующую функцию стравнивания
            self.error_collector = self.__measures_iteration_over_each_element(
                database_before=database_before,
                database_after=database_after,
                database_was_recording=database_was_recording,
                json_content=json_content)
        else:
            # Если они не раавны то добавляем ошибку
            self.error_collector.append({'error': 'Нет соответсвия archtypes name'})
        return self.error_collector

    # ---------------------------------------------------------------------------------------------------------------------
    #     вспомомгательная функция - перебор каждого элемента - типов данных приборов учета
    def __measures_iteration_over_each_element(self,
                                               database_before: list,
                                               database_after: list,
                                               database_was_recording: list,
                                               json_content: list):

        result = []
        # Теперь берем расчет по каждому из элементов
        for i in range(len(json_content)):
            # а теперь каждый элемент пихаем в сравниватель
            result.append(self.__measure_checkup_by_element(
                database_before=database_before[i],
                database_after=database_after[i],
                database_was_recording=database_was_recording[i],
                json_content=json_content[i]))

        return result

    # ----------------------------------------------------------------------------------------------------------------
    #     вспомогательная функция сравнивания значений именно определенного measure
    def __measure_checkup_by_element(self,
                                     database_before: list,
                                     database_after: list,
                                     database_was_recording: list,
                                     json_content: list):
        result = []
        # Первое что должны сделать - определиться с тэгом что лежит  в Name
        # и исходя из него составляем лист тэгов что содержится в нем

        archtype_name = json_content[0]['Name']

        if archtype_name in Template_list_ArchTypes.ElectricConfig_ArchType_name_list:
            tags_name = Template_list_ArchTypes.ElectricConfig_tag
        elif archtype_name in Template_list_ArchTypes.PulseConfig_ArchType_name_list:
            tags_name = Template_list_ArchTypes.PulseConfig_tag
        elif archtype_name in Template_list_ArchTypes.DigitalConfig_ArchType_name_list:
            tags_name = Template_list_ArchTypes.DigitalConfig_tag
        elif archtype_name in Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list:
            tags_name = Template_list_ArchTypes.ElecticEnergyValues_tag
        elif archtype_name in Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list:
            tags_name = Template_list_ArchTypes.ElectricQualityValues_tag
        elif archtype_name in Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list:
            tags_name = Template_list_ArchTypes.ElectricPowerValues_tag
        elif archtype_name in Template_list_ArchTypes.PulseValues_ArchType_name_list:
            tags_name = Template_list_ArchTypes.PulseValues_tag
        elif archtype_name in Template_list_ArchTypes.DigitalValues_ArchType_name_list:
            tags_name = Template_list_ArchTypes.DigitalValues_tag
        elif archtype_name in Template_list_ArchTypes.JournalValues_ArchType_name_list:
            tags_name = Template_list_ArchTypes.JournalValues_tag

        # Иначе - отбрасываем ошибку
        else:
            result = [{'error': 'Неправильно сформированно archtypes name'}]

        # После этого - проверяем на дубликаты , и отправляем в сравниватель
        if len(result) == 0:
            # Если нет ошибок то Добаввляем нужные тэги
            tags_name = ['id', 'ts'] + tags_name

            #  запускаем нашу функцию сравнивания
            result = self.__function_checkup_dict(
                database_before=database_before,
                database_after=database_after,
                database_was_recording=database_was_recording,
                json_content=json_content,
                tags_name=tags_name)

        return result

    # ----------------------------------------------------------------------------------------------------------------
    #    А это самая главная функция сравнивания
    def __function_checkup_dict(self,
                                database_before: list,
                                database_after: list,
                                database_was_recording: list,
                                json_content: list,
                                tags_name: list):

        # Включаем обработчик ошибок
        error_collector = []

        # Первое что делаем - проверяем поле VALID
        # проверяем - нужно ли проверять это поле :
        if (json_content[0]['Name'] not in Template_list_ArchTypes.ElectricConfig_ArchType_name_list) and \
                (json_content[0]['Name'] not in Template_list_ArchTypes.PulseConfig_ArchType_name_list) and \
                (json_content[0]['Name'] not in Template_list_ArchTypes.DigitalConfig_ArchType_name_list):
            # Теперь если это нужно - проверяем поле VALID

            database_expect_was_recording = self.__finding_discrepancy(
                from_subtract=database_before,
                subtract=database_after)
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!НАдо ДОПИСАТЬ проверку валидности!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            for i in range(len(database_expect_was_recording)):
                if database_expect_was_recording[i]['Valid'] == 0:
                    tags_name_valid = tags_name[:2]
                    for x in range(tags_name_valid):
                        if (database_expect_was_recording[i][tags_name[x]] is not None) and \
                                (json_content[i][tags_name[x]] is not None):
                            error_collector.append({
                                'error': 'Поле Valid приняло не правильное значение',
                                'Расхождение со стороны того что есть в JSON': json_content[i],
                                'Расхождение со стороны того что есть в БД': database_expect_was_recording[i]
                            })

        # Приводим все имеющиеся у нас словари в нормальное значение

        database_before_list_of_dict = self.__sorted_for_keys(list_dictionaries=database_before,
                                                              list_name_keys=tags_name)

        database_after_list_of_dict = self.__sorted_for_keys(list_dictionaries=database_after,
                                                             list_name_keys=tags_name)

        database_was_recording_list_of_dict = self.__sorted_for_keys(list_dictionaries=database_was_recording,
                                                                     list_name_keys=tags_name)

        json_content_list_of_dict = self.__sorted_for_keys(list_dictionaries=json_content,
                                                           list_name_keys=tags_name)

        # Теперь можно сделать сравнение
        # Первое что делаем -  складываем JSON и БД до записи должен быть равен БД после записи
        # Если нет - то делаем отлов ошибки

        if (database_after_list_of_dict != database_before_list_of_dict + json_content_list_of_dict) and \
                (len(database_after_list_of_dict) != len(database_before_list_of_dict) + len(
                    json_content_list_of_dict)):

            # для начала посмотрим что есть добавленного в БД по факту
            database_expect_was_recording_list_of_dict = self.__finding_discrepancy(
                from_subtract=database_before_list_of_dict,
                subtract=database_after_list_of_dict)

            # Далее проверяем коректность записи jSON в БД
            # И сравниваем добавленного в БД по факту с тем что мы отправили в JSON
            if json_content_list_of_dict != database_expect_was_recording_list_of_dict:
                result1 = self.__finding_discrepancy(from_subtract=database_expect_was_recording_list_of_dict,
                                                     subtract=json_content_list_of_dict)

                result2 = self.__finding_discrepancy(from_subtract=json_content_list_of_dict,
                                                     subtract=database_expect_was_recording_list_of_dict)
                error_collector.append({
                    'error': 'Записанное по факту не совпадает с тем что отправляли в JSON',
                    'Расхождение со стороны того что есть в JSON': result1,
                    'Расхождение со стороны того что есть в БД': result2
                })

            # Далее после того как получили что есть по факту сравниваем с тем что мы заселектили
            if database_was_recording_list_of_dict != database_expect_was_recording_list_of_dict:
                # Находим расхождения
                result1 = self.__finding_discrepancy(from_subtract=database_expect_was_recording_list_of_dict,
                                                     subtract=database_was_recording_list_of_dict)

                result2 = self.__finding_discrepancy(from_subtract=database_was_recording_list_of_dict,
                                                     subtract=database_expect_was_recording_list_of_dict)

                error_collector.append({
                    'error': 'Записалось лишее: Значения что записали не равны значениям что выдало select по id',
                    'Расхождение со стороны того что заселектили': result1,
                    'Расхождение со стороны того что есть в БД': result2
                })
            # Есть поврежденные записи
            database_expect_before_list_of_dict = self.__finding_discrepancy(
                from_subtract=json_content_list_of_dict,
                subtract=database_after_list_of_dict)

            if database_expect_before_list_of_dict != database_before_list_of_dict:
                # Находим расхождения
                result1 = self.__finding_discrepancy(from_subtract=database_before_list_of_dict,
                                                     subtract=database_expect_before_list_of_dict)

                result2 = self.__finding_discrepancy(from_subtract=database_expect_before_list_of_dict,
                                                     subtract=database_before_list_of_dict)

                error_collector.append({
                    'error': 'Повредились старые записи',
                    'Запись что была в БД': result2,
                    'Новое значение записи БД': result1
                })

            if len(database_after_list_of_dict) != len(database_before_list_of_dict) + len(json_content_list_of_dict):
                error_collector.append({
                    'error': 'В БД найдены дубли',
                    'БД до записи': database_before_list_of_dict,
                    'БД после записи': database_after_list_of_dict
                })

            if len(error_collector) == 0:
                error_collector.append({
                    'error': 'Неизвестная ошибка',
                    'БД до записи': database_before,
                    'БД после записи': database_after,
                    'Записи что добавлены в БД': database_was_recording,
                    'JSON': json_content
                })

        return error_collector

    # ----------------------------------------------------------------------------------------------------------------
    # Дополнительная функция которая конструирует нужный нам массив со словорями которые имеют нужные ключи
    def __sorted_for_keys(self, list_dictionaries: list, list_name_keys):
        """
        Это вспомомгательная функция ля того чтоб сформировать новый массив из словарей ,
        которые будут содержать только те значения что сравниваются.
        По сути - это отчищение от не нужных ключей.

        Возвращает список из словарей только с валидными ключами
        :param list_diction:
        :param list_keys:
        :return:
        """
        # Наш валидный список , котоырй будем заполнять
        valid_list_of_dictionaries = []
        for i in range(len(list_dictionaries)):
            # Создаем необходимый словарь
            valid_dict = {}
            for x in range(len(list_name_keys)):
                valid_dict[list_name_keys[x]] = list_dictionaries[i][list_name_keys[x]]
            # после чего добавляем сформированный список в основной массив

            valid_list_of_dictionaries.append(valid_dict)

        return valid_list_of_dictionaries

    # ----------------------------------------------------------------------------------------------------------------
    #     Напишим функцию нахождения разности - это важно!!
    def __finding_discrepancy(self, from_subtract: list, subtract: list):
        result_subtract = []
        for i in range(len(subtract)):
            if subtract[i] not in from_subtract:
                # Если нет - То сравниваем поэлементно по ключам
                print(subtract[i])
                result_subtract.append(subtract[i])

        return result_subtract


# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# -----------------------------Напишем здесь сравниватель для запроса GET----------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

class GETCheckUP:
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

class POSTCheckUP:
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

    def __init__(self, JSON_deconstruct: list,
                 DataBase_before: list,
                 DataBase_after: list,
                 DataBase_was_recording: list):
        # Итак - Переопределяем Поля - ЕТО ВАЖНО
        self.JSON_deconstruct = JSON_deconstruct
        self.DataBase_before = DataBase_before

        self.DataBase_after = DataBase_after
        self.DataBase_was_recording = DataBase_was_recording

        # self.error_collector = self.error_collector + self.__checkup_to_void()
        # self.JSON_deconstruct = self.__checkup_to_void()


        # Првоеряем валидность
        self.error_collector = self.error_collector + self.__checkup_field_valid()

        # после переопределения полей - делаем сравнение
        self.error_collector = self.error_collector + self.__checkup_archtype_name()

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

    # //////
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
        print('\n--------------------------')
        print('JSON_deconstruct', JSON_deconstruct)
        print('DataBase_before', DataBase_before)
        print('DataBase_after', DataBase_after)
        print('DataBase_was_recording', DataBase_was_recording)

        # Теперь первое что делаем - Получаем разницу что записалось по факту
        DataBase_after_the_fact = self.__getting_recording_record_after_fact(DataBase_after=DataBase_after,
                                                                             DataBase_before=DataBase_before)
        print('----------------------')
        # print(DataBase_after_the_fact)
        # print(len(DataBase_after_the_fact))
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
                if JSON_deconstruct[i] not in DataBase_was_recording:
                    # print('ОШИИИИБКА в JSON')
                    # ЕСЛИ У НАС НЕТ НИЧЕГО ХОРОШЕГО - То сравниваем ПОЭЛЕМЕНТНО
                    error = self.__checkup_json_with_database(JSON_Element=JSON_deconstruct[i],
                                                              database=DataBase_was_recording)

                else:
                    error = self.__checkup_json_with_database(JSON_Element=JSON_deconstruct[i],
                                                              database=DataBase_was_recording)

        else:
            error = error + [{
                "ОШИБКА": 'Записанное в БД , Не совпадает с JSON по длине. Что то потерялось',
                'JSON_deconstruct - Наш JSON': JSON_deconstruct,
                'DataBase_was_recording - То что записанно в БД ': DataBase_was_recording
            }]
        return error

    # //////

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

    def __check_up_element_keys(self, answer_element: dict, normal_element: dict):
        """Сравнивание поэлементно """
        error = []
        error_keys = []
        # Сначала проверяем значения ответа
        for keys in answer_element:
            # отбрасываем ключ diff
            if keys not in ['diff', 'Valid']:
                # Теперь сравниваем значения
                answer_value = answer_element.get(keys)
                normal_value = normal_element.get(keys)

                # Теперь проверяем их равнество

                if (type(normal_value) == float) and (type(answer_value) == float):
                    epsilon = 5.96e-08
                    if abs(normal_value / answer_value - 1) > epsilon:
                        error_string = {
                            'Неравенство значений Ключа': str(keys),
                            'Значение ключа в  JSON ответа': answer_value,
                            'Значение ключа в предполагаеммый JSON': normal_value
                        }

                        # Добавляем это в ошибку , и добавляем наш ключ
                        error.append(error_string)
                        error_keys.append(keys)
                else:
                    if answer_value != normal_value:
                        error_string = {
                            'Неравенство значений Ключа': str(keys),
                            'Значение ключа в  JSON ответа': answer_value,
                            'Значение ключа в предполагаеммый JSON': normal_value
                        }
                        # Добавляем это в ошибку , и добавляем наш ключ
                        error.append(error_string)
                        error_keys.append(keys)

        for keys in normal_element:
            # отбрасываем ключ diff
            if keys not in ['diff', 'Valid']:
                if keys not in error_keys:
                    # Теперь сравниваем значения
                    answer_value = answer_element.get(keys)
                    normal_value = normal_element.get(keys)

                    # Теперь проверяем их равнество

                    if (type(normal_value) == float) or (type(answer_value) == float):
                        epsilon = 5.96e-08
                        if abs(normal_value / answer_value - 1) > epsilon:
                            error_string = {
                                'Неравенство значений Ключа': str(keys),
                                'Значение ключа в  JSON ответа': answer_value,
                                'Значение ключа в предполагаеммый JSON': normal_value
                            }

                            # Добавляем это в ошибку , и добавляем наш ключ
                            error.append(error_string)

                    else:
                        if answer_value != normal_value:
                            error_string = {
                                'Неравенство значений Ключа': str(keys),
                                'Значение ключа в  JSON ответа': answer_value,
                                'Значение ключа в предполагаеммый JSON': normal_value
                            }

                            # Добавляем это в ошибку , и добавляем наш ключ
                            error.append(error_string)
        return error

    def __checkup_json_with_database(self, JSON_Element, database):
        '''Итак - Здесь приводим сравнивание JSON по ключаем '''
        # Итак = Перебираем нашу БД
        error = []
        element_id = None
        element_ts = None
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
                error = error + self.__check_up_element_keys(normal_element=database[i], answer_element=JSON_Element)

            if JSON_Element['id'] == database[i]['id']:
                element_id = i

            if JSON_Element['ts'] == database[i]['ts']:
                element_ts = i
            # Если не нашли нужный Элемент
        if element_id is None:
            error = error + [{'Не удалось найти Элемент JSON id ': JSON_Element['id'],
                              'JSON_Element': JSON_Element,
                              'То что записали в БД': database}]
        if element_ts is None:
            error = error + [{'Не удалось найти Элемент JSON ts ': JSON_Element['ts'],
                              'JSON_Element': JSON_Element,
                              'То что записали в БД': database}]

        return error

    def __checkup_field_valid(self):
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!НАдо ДОПИСАТЬ проверку валидности!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        error = []
        database_was_recording = self.DataBase_was_recording

        # print(database_was_recording)
        # if (database_was_recording[0][0]['Name'] not in (Template_list_ArchTypes.ElectricConfig_ArchType_name_list +
        #                                                 Template_list_ArchTypes.DigitalConfig_ArchType_name_list +
        #                                                 Template_list_ArchTypes.PulseConfig_ArchType_name_list)):
        #     for i in range(len(database_was_recording)):
        #         print('ЗДЕСЬ', database_was_recording[i])
        #         for x in range(len(database_was_recording[i])):
        #             if database_was_recording[i][x]['Valid'] != 1:
        #                 error = error + [
        #                     {
        #                         'error': 'Поле Valid приняло не правильное значение',
        #                         'Элемент где записанно не правильно - ': database_was_recording[i]
        #                     }
        #                 ]
        for i in range(len(database_was_recording)):

            for x in range(len(database_was_recording[i])):
                if database_was_recording[i][x].get('Name') not in (
                        Template_list_ArchTypes.ElectricConfig_ArchType_name_list + Template_list_ArchTypes.DigitalConfig_ArchType_name_list + Template_list_ArchTypes.PulseConfig_ArchType_name_list):
                    if database_was_recording[i][x].get('Valid') != 1:
                        error = error + [
                            {
                                'error': 'Поле Valid приняло не правильное значение',
                                'Элемент где записанно не правильно - ': database_was_recording[i]
                            }
                        ]
        return error

    # ----------------------------------------------------------------------------------------------------------------
    def __checkup_to_void(self):
        """Здесб проверяем наш JSON на наличие пустоты"""
        # итак - первое что делаем - берем JSON и определяем - Есть ли что то ТРИ в ряд

        JSON = self.JSON_deconstruct
        # создаем список пустых возможных комбинаций
        # Теперь перебираем JSON на наличие пустоты
        for i in range(len(JSON)):
            for x in range(len(JSON[i])):

                for keys in JSON[i][x]:
                    # Здесь расположим группы тэгов
                    none_dict = {
                        'tarif0': ['A+0', 'A-0', 'R+0', 'R-0'],
                        'tarif1': ['A+1', 'A-1', 'R+1', 'R-1'],
                        'tarif2': ['A+2', 'A-2', 'R+2', 'R-2'],
                        'tarif3': ['A+3', 'A-3', 'R+3', 'R-3'],
                        'tarif4': ['A+4', 'A-4', 'R+4', 'R-4'],
                    }
                    # Здесь их счет ПУТОСТЫ
                    find_void = {
                        'tarif0': 0,
                        'tarif1': 0,
                        'tarif2': 0,
                        'tarif3': 0,
                        'tarif4': 0,
                    }

                    # ТЕПЕРЬ ИЩЕМ ТРИ В РЯД
                    if JSON[i][x][keys] is None:
                        # ЕСли получили пустоту то смотрим ее вхождение в одну из категорий
                        for katigory in none_dict:

                            if keys in none_dict[katigory]:
                                find_void[katigory] = find_void.get(katigory) + 1
                        print(find_void)
                # Если у нас накопилось по итогу больше 3 , то удаляем всю категорию
                for tag in find_void:
                    if find_void[tag] >= 3:
                        tag_to_delete = none_dict[tag]
                        for element in range(len(tag_to_delete)):
                            print('--------eeeeeeeeee-')
                            JSON[i][x].pop(tag_to_delete[element])
                            print(JSON[i][x].pop(tag_to_delete[element]))
        return JSON
