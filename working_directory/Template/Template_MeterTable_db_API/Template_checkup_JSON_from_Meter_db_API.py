# Здесь описан класс проверки JSON от различных таблиц Meter db API

class CheckUP():
    """
    Класс для проверки что есть в базе данных и что в итоге мы получили

    """
    dublicate = None

    def __init__(self):
        self.dublicate = None
        Data_Base_settings = None
        JSON_settings = None

# ------------------------------------------------------------------------------------------------------------
#                     Вспомомгательные Функции для анализа корректности ключей
# ------------------------------------------------------------------------------------------------------------
# Функция обработчик пустого значения
    def __function_processing_emptiness(self, value):
        """
        Вспомогательная функция обработчик на пустое значение
        ЕСли у нас попадается пустое значение - возврщаем пустой массив
        :param value: Сюда отправлять переменную которую надо проверить на None
        :return: здесь получаем пустой массив если проверка на None успешна
        """
        if value == None:
            value = []
        return value

# Функция сравнения массивов
    def __function_checkup(self,JSON_settings:list, Data_Base_settings:list,json_field:list ,database_field:list):
        """
        Наша основная функция сравнивания

        :param JSON_settings: -Сюда передаем settings из JSON
        :param Data_Base_settings: -Сюда передаем что у нас есть в БД
        :param json_field: - Сюда передаем массив из названий ключей JSON
        :param database_field: - Сюда передаем массив из названий ключей полей таблицы
        :return: Возвращает результат сравниввания - Если успешно то пустой массив
        """

        # Проверяем наши данные на пустоту
        JSON_settings =  self.__function_processing_emptiness(JSON_settings)
        Data_Base_settings = self.__function_processing_emptiness(Data_Base_settings)
        # Работаем над dict который мы вытащили из базы данных
        # Создаем список для поиска ошибок
        dublicate = []
        # берем каждый словарь и его значения слепливаем в единый str и пихаем это в сет
        value_settings_str_set = set()
        for i in range(len(Data_Base_settings)):
            # Шаблон слепливания:
            value_dict = ''
            for x in range(len(database_field)):
                value_dict = str(value_dict) + str(Data_Base_settings[i][database_field[x]])
            # и добавляем в множество
            value_settings_str_set.add(value_dict)

            # Проверяем на наличие дубликатов в самой базе данных
        if len(value_settings_str_set) == len(Data_Base_settings):
            # после проверяем очень важную вещь - соответствие длины двух массивов - что мы получили от JSON и БД
            if len(Data_Base_settings) == len(JSON_settings):
                # Если дубликатов нет , то сравниваем это все с полученным JSON
                value_settings_str_set_copy = value_settings_str_set.copy()

                #делаем копию нашегос сета - понадобится чуть позже
                for i in range(len(JSON_settings)):
                    # проверяем коректность ключей
                    json_field_sort = json_field.copy()
                    json_field_sort.sort()
                    JSON_settings_list = list(JSON_settings[i].keys()).copy()
                    JSON_settings_list.sort()
                    if (JSON_settings_list == json_field_sort ):
                            # ("records" in JSON_settings[i]) and
                            # ("type" in JSON_settings[i])):
                        # Если успешно - сделаем из них сет для проверки на дубликат
                        element = ''
                        for x in range(len(json_field)):
                            element = str(element) + str(JSON_settings[i][json_field[x]])
                        # element = (
                        #         str(JSON_settings[i]["records"]) +
                        #         str(JSON_settings[i]["type"])
                        #             )
                        if element in value_settings_str_set:
                        # Если успешно - то удаляем этот результат из сета
                            value_settings_str_set.remove(element)
                        # Здесь проверяем - дубликат или не правильно сформированный JSON
                        else:
                            if element in value_settings_str_set_copy:
                                # ЕСли попадает в исходный - Добавляем в наш сет дубликатов
                                dublicate.append({"numper": i, "json_answer": JSON_settings[i], "error": "Дубликат уже существующей записи в JSON"})
                            else:
                                # Иначе - не правильно сформирвоаны значения ключей
                                dublicate.append(
                                    {"numper": i, "json_answer": JSON_settings[i],"error": "Таких значений ключей JSON нет в БД"})
                    else:
                        dublicate.append({"numper":i,"json_answer": JSON_settings[i],"error":'Не корректный ключ'})
            else:
                dublicate.append({"error": "Длина JSON ответа не равна колличеству записей в БД","numper": [
                    {'database': Data_Base_settings,
                    'json_answer': JSON_settings
                     }]})
        else:
            dublicate.append({"error":"Есть дубликаты в БД"})
        return dublicate

# ------------------------------------------------------------------------------------------------------------
    def __function_checkup_list(self,JSON_settings:list, Data_Base_settings:list ,database_field:list):
        """
        Функция сравнивания если у нас в settings просто набор символов , а не набор словарей

        :param JSON_settings: -Сюда передаем settings из JSON
        :param Data_Base_settings: -Сюда передаем что у нас есть в БД
        :param json_field: - Сюда передаем массив из названий ключей JSON
        :param database_field: - Сюда передаем массив из названий ключей полей таблицы
        :return: Возвращает результат сравниввания - Если успешно то пустой массив
        """
        # Проверяем наши данные на пустоту
        JSON_settings = self.__function_processing_emptiness(JSON_settings)
        Data_Base_settings = self.__function_processing_emptiness(Data_Base_settings)
        # Работаем над dict который мы вытащили из базы данных
        # Создаем список для поиска ошибок
        dublicate = []
        # берем каждый словарь и его значения слепливаем в единый str и пихаем это в сет
        value_settings_str_set = set()
        for i in range(len(Data_Base_settings)):
            # Шаблон слепливания:
            value_dict = ''
            for x in range(len(database_field)):
                value_dict = str(value_dict) + str(Data_Base_settings[i][database_field[x]])
            # и добавляем в множество
            value_settings_str_set.add(value_dict)
            # Проверяем на наличие дубликатов в самой базе данных
        if len(value_settings_str_set) == len(Data_Base_settings):
            # после проверяем очень важную вещь - соответствие длины двух массивов - что мы получили от JSON и БД
            if len(Data_Base_settings) == len(JSON_settings):
                # Если дубликатов нет , то сравниваем это все с полученным JSON
                value_settings_str_set_copy = value_settings_str_set.copy()
                # делаем копию нашегос сета - понадобится чуть позже
                for i in range(len(JSON_settings)):
                    # Если успешно - сделаем из них сет для проверки на дубликат
                    element = str(JSON_settings[i])
                    # Проверяем - входит ли элемент
                    if element in value_settings_str_set:
                            # Если успешно - то удаляем этот результат из сета
                            value_settings_str_set.remove(element)
                        # Здесь проверяем - дубликат или не правильно сформированный JSON
                    else:
                        if element in value_settings_str_set_copy:
                            # ЕСли попадает в исходный - Добавляем в наш сет дубликатов
                            dublicate.append({"numper": i, "json_answer": JSON_settings[i],
                                                  "error": "Дубликат уже существующей записи в JSON"})
                        else:
                                # Иначе - не правильно сформирвоаны значения ключей
                                dublicate.append(
                                    {"numper": i, "json_answer": JSON_settings[i], "error": "Таких значений ключей JSON нет в БД"})

            else: dublicate.append({"error": "Длина JSON не равна колличеству записей в БД"})
        else:
            dublicate.append({"error": "Есть дубликаты в БД"})
        return dublicate
# ------------------------------------------------------------------------------------------------------------

    def __concatenation_of_key_values_to_str(self, dict_list: list, name_key :list):
        """
        запилил отдельную функцию для сцепки в единый стринг значений ключей

        :param dict_list:
        :param name_key:
        :return: выдает множество в котором присутствует сцепка значенйи ключей в str
        """
        value_settings_str_set = set()
        for i in range(len(dict_list)):
            # Шаблон слепливания:
            value_dict = ''
            for x in range(len(name_key)):
                value_dict = str(value_dict) +str(' ') + str(dict_list[i][name_key[x]])
            # и добавляем в множество
            value_settings_str_set.add(value_dict)
        return value_settings_str_set

# ------------------------------------------------------------------------------------------------------------
#     Функция для сравнивания при пост запросах
    def __function_checkup_insert(self,
                        Data_Base_original_settings:list,
                        Data_Base_new_settings:list,
                        Data_Base_ids_settings: list,
                        database_field: list,
                        JSON_settings: list,
                        json_ids : list):
        """
        данная функция сравнивает значения из бд , при добавлении записей туды
        :param Data_Base_original_settings: это значения оригинальной бд до записи
        :param Data_Base_new_settings: это значения перезаписанной бд
        :param Data_Base_ids_settings: это значения бд что мы добавили

        :param database_field: это набор полей таблицы
        :param json_ids: значения JSON  по которым делали Select
        :return: Возвращает либо ошибку , либо остаток дублей
        """
        # Создаем список для поиска ошибок
        dublicate = []
        # для начала проверяем наш Data_Base_ids_settings, что он не пустой
        if len(Data_Base_ids_settings) == len(json_ids):
            # после чего составляем три множества -
            # множество полей ID
            Data_Base_ids_str_set = self.__concatenation_of_key_values_to_str(
                dict_list=Data_Base_ids_settings,
                name_key=database_field
            )
            # множество чистой базы данных
            Data_Base_original_str_set = self.__concatenation_of_key_values_to_str(
                dict_list=Data_Base_original_settings,
                name_key=database_field
            )
            # множество записанной базы данных
            Data_Base_new_str_set = self.__concatenation_of_key_values_to_str(
                dict_list=Data_Base_new_settings,
                name_key=database_field
            )
            # Множество которое получаем из JSON_settings
            JSON_settings_str_set = self.__concatenation_of_key_values_to_str(
                dict_list=JSON_settings,
                name_key=database_field
            )
            # немного магии - сравниваем множества с оригиналом
            if ((len(Data_Base_ids_str_set) == len(Data_Base_ids_settings))
                    and (len(Data_Base_original_str_set) == len(Data_Base_original_settings))
                    and (len(Data_Base_new_str_set) == len(Data_Base_new_settings))):
                # если они все равны начинаем сравнивать - из модифицированой БД вычитаем оригинал
                value_post_result = Data_Base_new_str_set - Data_Base_original_str_set
                # если наше множество не равно вот этому, то разницу добавляемв  дубликаты
                if len(value_post_result) == len(JSON_settings_str_set) :
                    if len(value_post_result - JSON_settings_str_set) != 0:

                        dublicate.append({"error": 'JSON Не правильно записался в БД',
                                          'numper':[JSON_settings_str_set,value_post_result]})
                else:
                    result = value_post_result - JSON_settings_str_set
                    dublicate.append({"error": 'Есть лишние записи',
                                      'numper':result})


            else:
                dublicate.append({"error": "В БД найдены дубликаты"})
        else:
            dublicate.append({"error": "Поле id не найдено в БД"})
        return dublicate
# ------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------
    # Функция обработчик удаляшек для metertable - общая
    def __function_checkup_metertable_delete(self,
                                             database_list_full :list,
                                             database_list_after_deletion :list ,
                                             database_list_name_key :list,
                                             ids :list,
                                             data_base_list_must_delete: list):
        """
        Функция обработчик для удаляшек из metertable

        :param database_list_full: пихаем сюда БД до удаления
        :param database_list_after_deletion: сюда пихаем БД после удаления
        :param database_list_name_key: Сюда пихаем лист из названий ключей
        :param ids: Сюда пихаем айдишники того что мы удаляли
        :param data_base_list_must_delete: Сюда пихаем БД что должно удалится
        :return: При хорошем раскладе - возвращает нам пустой массив. При плохом - где именно ошибка
        """
        # Создаем список для поиска ошибок
        dublicate = []
        # для начала проверяем нашу полную БД что она не пустая
        if len(database_list_full) != 0 :
            # Получаем список удаленных dict
            database_list_del = []
            for i in range(len(database_list_full)):
                if (database_list_full[i]["MeterId"] in ids ):
                    database_list_del.append(database_list_full[i])
            # после чего составляем три множества -
            # множество полей Оригинальной БД
            database_full_str_set = self.__concatenation_of_key_values_to_str(
                dict_list=database_list_full,
                name_key=database_list_name_key
            )
            # множество чистой базы данных
            database_after_deletion_str_set = self.__concatenation_of_key_values_to_str(
                dict_list=database_list_after_deletion,
                name_key=database_list_name_key
            )
            # множество  из тех ключей что мы удалили
            database_del_str_set = self.__concatenation_of_key_values_to_str(
                dict_list=database_list_del,
                name_key=database_list_name_key
            )
            # Множество тех ключей что мы должны были удалить
            data_base_must_delete_str_set = self.__concatenation_of_key_values_to_str(
                dict_list=data_base_list_must_delete,
                name_key=database_list_name_key
            )
    # теперь что c этим делаем- Множества из того что удадлили не должно содержаться в множестве что после удаления
            # немного магии - сравниваем множества с оригиналом
            if ((len(database_full_str_set) == len(database_list_full))
                    and (len(database_after_deletion_str_set) == len(database_list_after_deletion))
                    and (len(database_del_str_set) == len(database_list_del))):
                # если они все равны начинаем сравнивать -
                # множество после удаления и множество что удалили не пересекается

                # if len(database_after_deletion_str_set & database_del_str_set) == 0 :
                if len(database_after_deletion_str_set & data_base_must_delete_str_set) == 0:
                    # - из оригинальной БД вычитаем что осталось
                    value_result = database_full_str_set - database_after_deletion_str_set

                    if value_result != data_base_must_delete_str_set :
                        after_deletion = value_result - data_base_must_delete_str_set
                        dublicate = [{"error": "Удаление по id -  Удалилось лишнее", 'numper':after_deletion}]
                    # if value_result != database_del_str_set :
                    #     dublicate = [{"error": "Удаление по id - Ошибки при удалении"}]
                    else:
                        if len(value_result - data_base_must_delete_str_set) != 0 :
                            dublicate = [{"error": "Удаление по id - Ошибки при удалении",
                                          'numper':data_base_must_delete_str_set}]
                else:
                    after_deletion = database_after_deletion_str_set & data_base_must_delete_str_set
                    dublicate = [{"error": "Удаление по id -Удалилось не все.", 'numper':after_deletion }]
            else:
                dublicate = [{"error": "Удаление по id -БД содержит дубликаты"}]
        else:
            dublicate = [{"error":"Удаление по id -БД изначально была пустой, команда INSERT не прошла"}]

        return dublicate
# ------------------------------------------------------------------------------------------------------------
        # Формируем список перезаписанных значений
    def __form_of_overwritten_values_list(self, data_base_original: list,
                                              JSON_settings: list,
                                              key_data_base_list: list,
                                              key_JSON_list: list):
        """
            Вспомогательная Функция, чтоб сделать список из вспомогательных значений
            :param data_base_original: Пихаем сюда оригиналльную БД
            :param JSON_settings: Сюда точ то слали в JSON
            :param key_data_base_list:Сюда название ключей от БД
            :param key_JSON_list: Сюда название ключей от JSON
            :return:
        """
        # Получаем все перезаписанные айдишники
        overwritten_values_list = JSON_settings.copy()
        for i in range(len(data_base_original)):
            for x in range(len(overwritten_values_list)):
                # Перезаписываем исходя по ИД
                if data_base_original[i][key_data_base_list[0]] == overwritten_values_list[x][key_JSON_list[0]]:
                    overwritten_values_list[x][key_JSON_list[1]] = data_base_original[i][key_data_base_list[1]]
        return overwritten_values_list

# ------------------------------------------------------------------------------------------------------------
#     функция для очистки JSON от дублей - Это важная вещь
    def __cleaning_from_duble_update_Arch_info(self, JSON_settings:list):
        """
        Очиститель JSON от дублей
        :param JSON_settings: Кушает наш JSON
        :return: Выдает массив - Наш JSON и Список Дублей
        """
        # сначала реверснем список
        JSON_settings.reverse()
        # сделаем сет для поиска дублей
        double_set = set()
        # и куда будем дубли складировать
        double_list = []
        double_index = []
        # после этого проходимся по каждому элементу массива
        for i in range(len(JSON_settings)):
            # Если данного значения нет в множнестве то добавляем его
            double = JSON_settings[i]['Id']
            if double not in double_set:
                double_set.add(JSON_settings[i]['Id'])
            # Иначе - дабавляем в список
            else:
                double_list.append( {'Дублирующий JSON' : JSON_settings[i]})
                double_index.append(i)
            # И дублирующий dict нужно удалить
        double_index.reverse()
        for i in range(len(double_index)):
            delete_index = double_index[i]
            del JSON_settings[delete_index]
        # переворачиваем обратно
        JSON_settings.reverse()
        return JSON_settings , double_list

# ------------------------------------------------------------------------------------------------------------
    # Функция сравнивания при апдейте
    def __function_checkup_update(self,
                                  data_base_original: list,
                                  data_base_modified: list,
                                  JSON_settings: list,
                                  key_data_base_list: list,
                                  key_JSON_list: list):

        """
        Функция Сравнения UPDATE
        :param data_base_original: Оригинальная БД - Список из словарей
        :param data_base_modified: Измененая БД - Список из словарей
        :param JSON_settings: То что мы отправляли в JSON - Список из словарей
        :param key_data_base_list: имена полей в БД
        :param key_JSON_list:   имена полей в JSON
        :return:
        """
        # Создаем список для поиска ошибок
        dublicate = []
        # Для начала - проверяем не добавилось ли лишних записей
        if len(data_base_original) == len(data_base_modified):
            # Теперь очищаем JSON от дублей

            JSON_settings_cleaned, double_list = self.__cleaning_from_duble_update_Arch_info(JSON_settings)
            if len(double_list) != 0 :
                dublicate.append({"error": "В JSON найдены дубли", 'list':double_list })
            # Берем каждый список словарей и преврщаем их в множество

            data_base_original_str_set = self.__concatenation_of_key_values_to_str(
                dict_list=data_base_original,
                name_key=key_data_base_list
            )
            data_base_modified_str_set = self.__concatenation_of_key_values_to_str(
                dict_list=data_base_modified,
                name_key=key_data_base_list
            )
            JSON_settings_str_set = self.__concatenation_of_key_values_to_str(
                dict_list=JSON_settings_cleaned,
                name_key=key_JSON_list
            )
            # проверяем что значения перезаписались
            if data_base_original_str_set != data_base_modified_str_set:
                # а здесь начинается вся магия -
                #Саначала удаляем все те значения которые были в БД изначально
                convergence_set = (data_base_modified_str_set - data_base_original_str_set)
                # после этого вычитаем все значения JSON
                # convergence_final_set = (convergence_set - JSON_settings_str_set )
                if convergence_set != JSON_settings_str_set:
                    result = convergence_set - JSON_settings_str_set
                    if len(result) > 0 :
                        dublicate.append({"error": "Перезапись выполнена не верно", 'numper':result})
                    else:
                        result = JSON_settings_str_set - convergence_set
                        dublicate.append({"error": "Это не записалось", 'numper': result})

            else:
                dublicate.append({"error": "БД не обновилась"})
        else:
            dublicate.append({"error": "БД не равны по длине. Добавлены лишние записи"})

        return dublicate
# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
    def get_ArchTypes(self, JSON_settings, Data_Base_settings):
        """
        Обработчик для проверки ArchTypes
        :param JSON_settings: Сюда пихать массив settings
        :param Data_Base_settings: Сюда пихать что мы выгрузили из Базы данных
        :return: Возвращает массив в котором находятся не совпавшие элементы.
        Они находятся в массиве - Номер значения - Пара что не совпала
        """
        json_field = ["dataType", "meterType", "name"]
        database_field = ["DataType", "MeterType", "Name"]
        return self.__function_checkup(
            json_field=json_field,
            database_field=database_field,
            JSON_settings=JSON_settings,
            Data_Base_settings=Data_Base_settings
        )


    def get_ArchInfo(self,JSON_settings:list, Data_Base_settings:list):
        """
        Обработчик для проверки ArchInfo
        :param JSON_settings: Сюда пихать массив settings
        :param Data_Base_settings: Сюда пихать что мы выгрузили из Базы данных
        :return:Возвращает массив в котором находятся не совпавшие элементы.
        Они находятся в массиве - Номер значения - Пара что не совпала
        """

        json_field = ["records", "type"]
        database_field = ["Records", "Arch"]
        return self.__function_checkup(
                                        json_field= json_field,
                                        database_field=database_field ,
                                        JSON_settings = JSON_settings,
                                        Data_Base_settings = Data_Base_settings
                                       )

    def get_MeterTypes(self,JSON_settings:list, Data_Base_settings:list):
        """
        Обработчик для проверки MeterTypes
        :param JSON_settings: Сюда пихать массив settings
        :param Data_Base_settings: Сюда пихать что мы выгрузили из Базы данных
        :return:Возвращает массив в котором находятся не совпавшие элементы.
        Они находятся в массиве - Номер значения - Пара что не совпала
        """

        json_field = ["id", "type","class"]
        database_field = ["Id", "Type","Class"]
        return self.__function_checkup(
                                        json_field= json_field,
                                        database_field=database_field ,
                                        JSON_settings = JSON_settings,
                                        Data_Base_settings = Data_Base_settings
                                       )

    def get_MeterIfaces(self,JSON_settings:list, Data_Base_settings:list):
        """
        Обработчик для проверки MeterIfaces
        :param JSON_settings: Сюда пихать массив settings
        :param Data_Base_settings: Сюда пихать что мы выгрузили из Базы данных
        :return:Возвращает массив в котором находятся не совпавшие элементы.
        Они находятся в массиве - Номер значения - Пара что не совпала
        """

        database_field = ["Name"]
        return self.__function_checkup_list(

                                        database_field=database_field ,
                                        JSON_settings = JSON_settings,
                                        Data_Base_settings = Data_Base_settings
                                       )

    def get_MeterTable(self,JSON_settings:list, Data_Base_settings:list):
        """
        Обработчик для проверки MeterTable
        :param JSON_settings: Сюда пихать массив settings
        :param Data_Base_settings: Сюда пихать что мы выгрузили из Базы данных
        :return:Возвращает массив в котором находятся не совпавшие элементы.
        Они находятся в массиве - Номер значения - Пара что не совпала
        """

        json_field = [    "index",
                          "id",
                          "pId",
                          "type",
                          "typeName",
                          "addr",
                          "passRd",
                          "passWr",
                          "ifaceName",
                          "ifaceCfg",
                          "rtuObjType",
                          "rtuFider",
                          "rtuObjNum",
                          ]
        database_field = ["DeviceIdx",
                          "MeterId",
                          "ParentId",
                          "TypeId",
                          "Type",
                          "Address",
                          "ReadPassword",
                          "WritePassword",
                          "Name",
                          "InterfaceConfig",
                          "RTUObjType",
                          "RTUFeederNum",
                          "RTUObjNum"
                          ]
        return self.__function_checkup(
                                        json_field= json_field,
                                        database_field=database_field ,
                                        JSON_settings = JSON_settings,
                                        Data_Base_settings = Data_Base_settings
                                       )
    # Обработчик для MeterTable , при команде post
    def post_MeterTable(self,
                        Data_Base_original_settings:list,
                        Data_Base_new_settings:list,
                        Data_Base_ids_settings: list,
                        JSON_settings: list,
                        json_ids: list):
        """
        Обработчик для MeterTable , при команде post

        :param Data_Base_original_settings: сюда пихать оригинальную бд , до записи
        :param Data_Base_new_settings: сюда пихать бд после записи
        :param Data_Base_ids_settings: сюда пихать что мы населектели
        :param json_ids: сюда пихать ид по которым мы селектели
        :return: Возвращает массив в котором находятся не совпавшие элементы.
        если чего - что именно случилос
        """
        database_field = [
                          "MeterId",
                          "ParentId",
                          "TypeId",
                          "Type",
                          "Address",
                          "ReadPassword",
                          "WritePassword",
                          "Name",
                          "InterfaceConfig",
                          "RTUObjType",
                          "RTUFeederNum",
                          "RTUObjNum"
                          ]

        return self.__function_checkup_insert(
                                                Data_Base_original_settings= Data_Base_original_settings,
                                                Data_Base_new_settings=Data_Base_new_settings,
                                                Data_Base_ids_settings=Data_Base_ids_settings,
                                                JSON_settings= JSON_settings,
                                                database_field=database_field,
                                                json_ids= json_ids )

    # Обработчик для MeterTable , при команде delete
    def delete_MeterTable_all(self, dict_data_base:list, dict_settings:list):
        """
        Данная функция проверяет что у нас удалилось из базы
        :param dict_data_base: сюда тыкать ответ из бд
        :param dict_settings: сюда сувать что у нас в JSON
        :return: Возвращает массив в котором находятся не удаленные элементы
        """

        # сначала проверяем что база пуста
        if len(dict_data_base) == 0 :
            # потом проверяем пустой ли у нас JSON
            if len(dict_settings) == 0:
                # если JSON пустой то отправляем пустую базу в качестве ответа
                return dict_data_base
            # Иначе - отправляем что запара в JSON
            else:
                return [{
                    "error": "Удаление всей базы - JSON возвращается не пустой",
                    'JSON': dict_settings
                }]
        # Не все удалилось из БД
        else:
            return [{
                                    "error": "Удаление всей базы -В БД не удалилось",
                                     "numper": dict_data_base
                    }]

    # Обработчик для MeterTable , при команде delete
    def delete_MeterTable_element(self,
                                             database_list_full :list,
                                             database_list_after_deletion :list ,
                                             ids :list,
                                             data_base_list_must_delete: list ):
        """
        Обработчик для MeterTable , при команде delete
        :param database_list_full:  Сюда пихаем БД которая есть до удаления
        :param database_list_after_deletion: Сюда пихаем БД после удаления
        :param ids: Сюда пихаем ID что в JSON
        :param data_base_list_must_delete: Сюда пихаем что должно быть в БД удаленно
        :return: Возвращает пустой массив при удаче , ошибку при неудаче
        """
        database_list_name_key = [
                                    "MeterId",
                                    "ParentId",
                                    "TypeId",
                                    "Address",
                                    "ReadPassword",
                                    "WritePassword",
                                    "InterfaceId",
                                    "InterfaceConfig",
                                    "RTUObjType",
                                    "RTUFeederNum",
                                    "RTUObjNum"
                                    ]
        return self.__function_checkup_metertable_delete(
                                                         database_list_full = database_list_full,
                                                         database_list_after_deletion = database_list_after_deletion,
                                                         database_list_name_key = database_list_name_key,
                                                         ids = ids,
                                                         data_base_list_must_delete = data_base_list_must_delete)



    def put_ArchInfo(self, data_base_original:list, data_base_modified : list, JSON_settings : list):
        """
        Данная Функция проверяет - перезапись

        :param data_base_original: Сюда пихаем Оригинальную БД
        :param data_base_modified:  сюда пихаем БД после перезаписи
        :param JSON_settings:  сюда пихаем что мы перезаписывали
        :return: Возвращает пустой массив при удаче , ошибку при неудаче
        """
        key_data_base_list = ['RecordTypeId',
                              'Records']
        key_JSON_list = ['Id',
                         'records' ]
        return self.__function_checkup_update(
                                                data_base_original= data_base_original,
                                                data_base_modified = data_base_modified,
                                                JSON_settings = JSON_settings,
                                                key_data_base_list = key_data_base_list,
                                                key_JSON_list = key_JSON_list )


