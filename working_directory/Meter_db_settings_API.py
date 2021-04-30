# Здесь прописываем Наши методы для Meter DB API, какие они должны быть

# Здесь расположим сборщик JSON из всех тех объектов что есть


import json

# Либа для формирования JSON запроса
from working_directory.Template.Template_MeterTable_db_API import Template_JSON_for_Meter_db_API
from working_directory import sqlite

from working_directory.Template.Template_Setup import Setup
from working_directory.Template.JSON_handler_error import error_handler, parse_id_from_json
from working_directory.Template.Template_MeterTable_db_API.Template_checkup_JSON_from_Meter_db_API import CheckUP
from working_directory.Template.Template_MeterTable_db_API.Template_generator_settings_MeterTable import \
    GeneratorForSettingsMeterTable
from working_directory.Template.Template_MeterTable_db_API.Template_generator_settings_ArchInfo import \
    GeneratorForSettingsArchInfo
import time
from working_directory.log import log


# ----------------------------------------------------------------------------------------------------------------------
#                                                   GET
# ----------------------------------------------------------------------------------------------------------------------
class GET:
    """
    Класс для работы с методом GET
    """
    setting = None
    ids = None
    select_all = False
    type_connect: str = 'virtualbox'

    def __init__(self, type_connect: str = 'virtualbox'):
        self.type_connect = type_connect

    # Дёргаем таблицу ArchTypes

    def ArchTypes(self):
        """
        Тест для Метода чтения значений таблицы MeterIfaces.

        Дополнительных параметров не надо

        :return: Возваращет массив. Он пустой если тест успешен
        """
        # Наши переменные в этом методе :
        # сама таблица
        name_ArchTypes = "ArchTypes"
        # ее поля
        ArchTypes_field = "DataType, MeterType, Name"
        # Для начала считывем базу данных
        database_ArchTypes_dict = sqlite.readtable_return_dict(collum=ArchTypes_field, table_name=name_ArchTypes)
        # Теперь составляем нам нужный JSON
        JSON = Template_JSON_for_Meter_db_API.GET().ArchTypes(setting=self.setting, ids=self.ids)
        # Теперь его отправляем на нужную нам в космос
        # Замереем время
        time_start = time.time()

        JSON_Setup = Setup(JSON, API='meter_db_settings', type_connect=self.type_connect)
        answer_JSON = JSON_Setup.answer_JSON

        # Получаем время
        time_finis = time.time()

        print('JSON Обрабабатывался:', time_finis - time_start)

        # Теперь пихаем это все в обработчик ошибок
        JSON_setting = error_handler(answer_JSON)
        if (type(JSON_setting) == list) or (type(JSON_setting) == tuple):
            # Пихаем данные из сетинга и бд в сравниватель
            result = CheckUP().get_ArchTypes(JSON_settings=JSON_setting, Data_Base_settings=database_ArchTypes_dict)
            if len(result) > 0:
                result = log(API_name='Meter db settings API - GET - ' + str(name_ArchTypes),
                             Error=result,
                             JSON=JSON,
                             answer_JSON=answer_JSON,
                             JSON_normal=None)

            return result
            # Иначе - Возвращаем код ошибки
        else:
            result = log(API_name='Meter db settings API - GET - ' + str(name_ArchTypes),
                         Error=JSON_setting,
                         JSON=JSON,
                         answer_JSON=answer_JSON,
                         JSON_normal=None)

            return result

    # Дёргаем таблицу MeterIfaces

    def MeterIfaces(self):
        """
        Тест для Метода чтения значений таблицы MeterIfaces.

        Дополнительных параметров не надо

        :return: Возваращет массив. Он пустой если тест успешен
        """
        # Наши переменные в этом методе :
        # сама таблица
        name_table = "MeterIfaces"
        # ее поля
        table_field = "Name"
        # Для начала считывем базу данных
        database_MeterIfaces_dict = sqlite.readtable_return_dict(collum=table_field, table_name=name_table)
        # Теперь составляем нам нужный JSON
        JSON = Template_JSON_for_Meter_db_API.GET().MeterIfaces(setting=self.setting, ids=self.ids)

        # Замереем время
        time_start = time.time()

        JSON_Setup = Setup(JSON, API='meter_db_settings', type_connect=self.type_connect)
        answer_JSON = JSON_Setup.answer_JSON

        # Получаем время
        time_finis = time.time()

        print('JSON Обрабабатывался:', time_finis - time_start)


        # Теперь пихаем это все в обработчик ошибок
        JSON_setting = error_handler(answer_JSON)
        if (type(JSON_setting) == list) or (type(JSON_setting) == tuple):
            # Пихаем данные из сетинга и бд в сравниватель
            result = CheckUP().get_MeterIfaces(JSON_settings=JSON_setting, Data_Base_settings=database_MeterIfaces_dict)
            if len(result) > 0:
                result = log(API_name='Meter db settings API - GET - ' + str(name_table),
                             Error=result,
                             JSON=JSON,
                             answer_JSON=answer_JSON,
                             JSON_normal=None)
            return result
            # Иначе - Возвращаем код ошибки
        else:
            result = log(API_name='Meter db settings API - GET - ' + str(name_table),
                         Error=JSON_setting,
                         JSON=JSON,
                         answer_JSON=answer_JSON,
                         JSON_normal=None)

            return result

    # Дёргаем таблицу MeterTypes

    def MeterTypes(self):
        """
        Тест для Метода чтения значений таблицы MeterTypes.

        Дополнительных параметров не надо

        :return: Возваращет массив. Он пустой если тест успешен
        """
        # Наши переменные в этом методе :
        # сама таблица
        name_table = "MeterTypes"
        # ее поля
        table_field = "*"
        # Для начала считывем базу данных
        database_MeterTypes_dict = sqlite.readtable_return_dict(collum=table_field, table_name=name_table)
        # Теперь составляем нам нужный JSON

        JSON = Template_JSON_for_Meter_db_API.GET().MeterTypes(setting=self.setting, ids=self.ids)
        # Теперь его отправляем на нужную нам в космос

        # Замереем время
        time_start = time.time()

        JSON_Setup = Setup(JSON, API='meter_db_settings', type_connect=self.type_connect)
        answer_JSON = JSON_Setup.answer_JSON

        # Получаем время
        time_finis = time.time()

        print('JSON Обрабабатывался:', time_finis - time_start)

        # Теперь пихаем это все в обработчик ошибок
        JSON_setting = error_handler(answer_JSON)
        if (type(JSON_setting) == list) or (type(JSON_setting) == tuple):
            # Пихаем данные из сетинга и бд в сравниватель
            result = CheckUP().get_MeterTypes(JSON_settings=JSON_setting, Data_Base_settings=database_MeterTypes_dict)
            if len(result) > 0:
                result = log(API_name='Meter db settings API - GET - ' + str(name_table),
                             Error=result,
                             JSON=JSON,
                             answer_JSON=answer_JSON,
                             JSON_normal=None)
            return result
            # Иначе - Возвращаем код ошибки
        else:
            result = log(API_name='Meter db settings API - GET - ' + str(name_table),
                         Error=JSON_setting,
                         JSON=JSON,
                         answer_JSON=answer_JSON,
                         JSON_normal=None)
            return result

    # Дёргаем таблицу ArchInfo

    def ArchInfo(self):
        """
         Тест для Метода чтения значений таблицы ArchInfo.

        Дополнительных параметров не надо

        :return: Возваращет массив. Он пустой если тест успешен
        """
        # Наши переменные в этом методе :
        # сама таблица
        name_table = "ArchInfo"
        # ее поля
        table_field = "*"
        # Для начала считывем базу данных
        database_ArchInfo_dict = sqlite.readArchInfo_return_dict()
        # Теперь составляем нам нужный JSON

        JSON = Template_JSON_for_Meter_db_API.GET().ArchInfo(setting=self.setting, ids=self.ids)
        # Теперь его отправляем на нужную нам в космос
        # Замереем время
        time_start = time.time()

        JSON_Setup = Setup(JSON, API='meter_db_settings', type_connect=self.type_connect)
        answer_JSON = JSON_Setup.answer_JSON

        # Получаем время
        time_finis = time.time()

        print('JSON Обрабабатывался:', time_finis - time_start)

        # Теперь пихаем это все в обработчик ошибок
        JSON_setting = error_handler(answer_JSON)
        if (type(JSON_setting) == list) or (type(JSON_setting) == tuple):
            # Пихаем данные из сетинга и бд в сравниватель
            result = CheckUP().get_ArchInfo(JSON_settings=JSON_setting, Data_Base_settings=database_ArchInfo_dict)
            if len(result) > 0:
                result = log(API_name='Meter db settings API - GET - ' + str(name_table),
                             Error=result,
                             JSON=JSON,
                             answer_JSON=answer_JSON,
                             JSON_normal=None)
            return result
            # Иначе - Возвращаем код ошибки
        else:
            result = log(API_name='Meter db settings API - GET - ' + str(name_table),
                         Error=JSON_setting,
                         JSON=JSON,
                         answer_JSON=answer_JSON,
                         JSON_normal=None)
            return result

    # Дёргаем таблицу MeterTable

    def MeterTable(self, count_get_ids: int = 3, count_generate_ids: int = 3, ids=None):
        """
        Тест для Метода чтения значений таблицы MeterTable.
        Здесь работает Генератор, который наполняет базу , и после чего задает заданное число элементов через JSON.
        Надо задать число сколько надо генерировать.
        Заложена возможность для ручного ввода через ids, но функционал вырезан

        Успешный тест возвращает пустой массив. Неуспешный - массив из словарей в которых описана ошибка.
        ошибка ищутся по ключу error

        :param count_get_ids: Число id оторые дергаем из таблицы. При 0 запрашивает все
        :param count_generate_ids: Число которое отвечает за количество сгенерирвоанных значенйи в таблице
        :param ids: Вырезан
        :return: Возваращет массив. Он пустой если тест успешен
        """
        # Наши переменные в этом методе :
        # сама таблица
        name_table = "MeterTable"
        # ее поля
        table_field = "*"
        # частный случай - селектим все
        if count_get_ids == 0:
            self.select_all = True
            count_get_ids = count_generate_ids
        # Все это начинает работать только если количество генераций больше или равно количеству селектов
        if (count_generate_ids >= 1) and (count_generate_ids >= count_get_ids):
            #  генерируем значения в базу - settings и ids для JSON , settings для БД
            generate = GeneratorForSettingsMeterTable(count_generate_ids)
            # Загружаем нужные нам ID
            sqlite.recording_MeterTable(generate.get_tuple())
            # Теперь надо сделать конструктор для ID котоыре полетят в select

            if self.select_all == True:
                ids_select = None

            else:
                ids_select = tuple(generate.get_id_to_delete(count_get_ids))
            # Для начала считывем базу данных
            database_MeterTable_dict = sqlite.readMeterTable_return_dict(ids=ids_select)
            # Теперь составляем нам нужный JSON

            JSON = Template_JSON_for_Meter_db_API.GET().MeterTable(setting=self.setting, ids=ids_select)
            # Замереем время
            time_start = time.time()

            JSON_Setup = Setup(JSON, API='meter_db_settings', type_connect=self.type_connect)
            answer_JSON = JSON_Setup.answer_JSON

            # Получаем время
            time_finis = time.time()
            # print('JSON\n', JSON)
            #
            # print('answer_JSON\n', answer_JSON)


            print('JSON Обрабабатывался:', time_finis - time_start)

            # Теперь пихаем это все в обработчик ошибок
            JSON_setting = error_handler(answer_JSON)
            if (type(JSON_setting) == list) or (type(JSON_setting) == tuple):
                # Пихаем данные из сетинга и бд в сравниватель
                result = CheckUP().get_MeterTable(JSON_settings=JSON_setting,
                                                  Data_Base_settings=database_MeterTable_dict)
                if len(result) > 0:
                    result = log(API_name='Meter db settings API - GET - ' + str(name_table),
                                             Error=result,
                                             JSON=JSON,
                                             answer_JSON=answer_JSON,
                                             JSON_normal=None)
                return result
                # Иначе - Возвращаем код ошибки
            else:
                result = log(API_name='Meter db settings API - GET - ' + str(name_table),
                                         Error=JSON_setting,
                                         JSON=JSON,
                                         answer_JSON=answer_JSON,
                                         JSON_normal=None)
                return result

        else:
            result = log(API_name='Meter db settings API - GET - ' + str(name_table),
                             Error=['Неправильно заданы параметры запроса'],
                             JSON= {'Не был сгенерирован':'не был отправлен'},
                             answer_JSON={'не был отправлен':'не был получен'},
                             JSON_normal=None)
            return result


# ----------------------------------------------------------------------------------------------------------------------
#                                                   POST
# ----------------------------------------------------------------------------------------------------------------------
class POST:
    """
        Класс для работы с методом POST
    """
    ids = None
    type_connect: str = 'virtualbox'

    def __init__(self, type_connect: str = 'virtualbox'):
        name_table = ""
        self.type_connect = type_connect

    # Дёргаем таблицу MeterTable

    def MeterTable(self, count_settings: int = 3, setting=None):
        """
        Тест для Метода записи значений таблицы MeterTable.
        Здесь работает Генератор, который наполняет базу , и после чего добавляет заданное число элементов через JSON.
        Надо задать число сколько надо генерировать.
        Заложена возможность для ручного ввода через setting, но функционал вырезан

        Успешный тест возвращает пустой массив. Неуспешный - массив из словарей в которых описана ошибка.
        ошибка ищится по ключу error

        Дополнительных параметры можно выставить в setting

        :param count_settings: Число settings которые получатся при генерации
        :param setting: Сюда пихаем наши сеттингс - вырезано
        :return: Массив из словарей. Если тест успешен , то массив пустой

        """
        # Наши переменные в этом методе :
        # сама таблица
        name_table = "MeterTable"
        # ее поля
        table_field = "*"
        if count_settings > 0:
            #  генерируем значения в базу - settings и ids для JSON , settings для БД
            generate = GeneratorForSettingsMeterTable(count_settings)
            generate_setting = generate.get_dict()
            JSON_settings_Format_to_DB = generate.get_JSON_setting_Format_to_DB()
            generate_ids = tuple(generate.get_ids())
            # Для начала считывем базу данных до изменений
            database_MeterTable_original_dict = sqlite.readMeterTable_return_dict()
            # Теперь составляем нам нужный JSON
            JSON = Template_JSON_for_Meter_db_API.POST().MeterTable(setting=generate_setting, ids=self.ids)
            # Теперь его отправляем на нужную нам в космос
            # Замереем время
            time_start = time.time()

            print(JSON)

            JSON_Setup = Setup(JSON, API='meter_db_settings', type_connect=self.type_connect)
            answer_JSON = JSON_Setup.answer_JSON

            # Получаем время
            time_finis = time.time()

            print('JSON Обрабабатывался:', time_finis - time_start)

            # Теперь пихаем это все в обработчик ошибок
            JSON_setting = error_handler(answer_JSON)
            if (type(JSON_setting) == list) or (type(JSON_setting) == tuple):
                # для обработчика нам нужно :

                # Новая обновленная БД
                database_MeterTable_new_dict = sqlite.readMeterTable_return_dict()
                # Дергаем нужные ID из БД с помощью JSON что мы отправляли
                ids = parse_id_from_json(json.loads(JSON))
                database_MeterTable_ids_dict = sqlite.readMeterTable_return_dict(ids=generate_ids)
                # и отправляем это все в обработчик
                result = CheckUP().post_MeterTable(
                    Data_Base_original_settings=database_MeterTable_original_dict,
                    Data_Base_new_settings=database_MeterTable_new_dict,
                    Data_Base_ids_settings=database_MeterTable_ids_dict,
                    JSON_settings=JSON_settings_Format_to_DB,
                    json_ids=list(ids)
                )
                # а после проверки - можно и удалить
                # sqlite.deleteMeterTable(ids=generate_ids)
                if len(result) > 0:
                    result = log(API_name='Meter db settings API - POST - ' + str(name_table),
                                 Error=result,
                                 JSON=JSON,
                                 answer_JSON=answer_JSON,
                                 JSON_normal=None)
                return result
                # Иначе - Возвращаем код ошибки
            else:
                result = log(API_name='Meter db settings API - POST - ' + str(name_table),
                             Error=[JSON_setting],
                             JSON=JSON,
                             answer_JSON=answer_JSON,
                             JSON_normal=None)

                return result
        else:
            result = log(API_name='Meter db settings API - GET - ' + str(name_table),
                         Error=['Неправильно заданы параметры запроса'],
                         JSON={'Не был сгенерирован': 'не был отправлен'},
                         answer_JSON={'не был отправлен': 'не был получен'},
                         JSON_normal=None)

            return result


# ----------------------------------------------------------------------------------------------------------------------
#                                                   PUT
# ----------------------------------------------------------------------------------------------------------------------
class PUT:
    """
        Класс для работы с методом PUT
    """
    name_table = None
    table_field = None
    ids = None
    type_connect: str = 'virtualbox'

    def __init__(self, type_connect: str = 'virtualbox'):
        self.name_table = ''
        self.table_field = '*'
        self.type_connect = type_connect

    # Дёргаем таблицу ArchInfo

    def ArchInfo(self, count_settings: int = 3, setting=None):

        """
        Тест для Метода перезаписи значений таблицы ArchInfo.
        Здесь работает Генератор, который наполняет базу , и после чего изменяет заданное число элементов через JSON.
        Надо задать число сколько надо генерировать. невозможно сгенерировать больше чем есть в таблице
        Заложена возможность для ручного ввода через setting, но функционал вырезан

        Успешный тест возвращает пустой массив. Неуспешный - массив из словарей в которых описана ошибка.
        ошибка ищится по ключу error

        :param count_settings: если мы не хотим их пихать, можно их рандомно сгенерировать. Этот вариант для вас.
        Указываем число
        :param setting: Сюда пихаем наши сеттингс - вырезано
        :return: Массив из словарей. Если тест успешен , то массив пустой

        """
        # сама таблица
        self.name_table = 'ArchInfo'
        # ее поля
        self.table_field = '*'
        # сначала мы приводим БД в исходное состояние -
        sqlite.updateArchInfo_for_stoc()
        # После мы селектим ее
        database_ArchInfo_original_dict = sqlite.readtable_return_dict(
            table_name=self.name_table,
            collum=self.table_field
        )
        # Важный момент - если мы передали значение больше чем есть записей в БД - То тест будет крашится.
        # Поэто необходимо сделать проверку на это
        if len(database_ArchInfo_original_dict) >= count_settings:
            # Теперь начинаем формировать JSON
            # Начинаем с генератора setting
            generate = GeneratorForSettingsArchInfo(count_settings)
            # Теперь формируем сам JSON - Отдаем туда сеттинг
            setting_generate = generate.get_dict()
            # Переключатель на ручное управление
            # if setting != None:
            #     setting_JSON = setting
            setting_JSON = generate.get_dict_without_id()
            # Теперь конструируем сам JSON
            JSON = Template_JSON_for_Meter_db_API.PUT().ArchInfo(setting=setting_JSON)
            # Замереем время
            time_start = time.time()

            JSON_Setup = Setup(JSON, API='meter_db_settings', type_connect=self.type_connect)
            answer_JSON = JSON_Setup.answer_JSON

            # Получаем время
            time_finis = time.time()

            print('JSON Обрабабатывался:', time_finis - time_start)
            # Теперь пихаем это все в обработчик ошибок
            JSON_setting = error_handler(answer_JSON)
            if (type(JSON_setting) == list) or (type(JSON_setting) == tuple):
                # для обработчика нам нужно :
                #     Уже измененая БД
                database_ArchInfo_modoified_dict = sqlite.readtable_return_dict(
                    table_name=self.name_table,
                    collum=self.table_field
                )

                # Теперь пихаем это все в обработчик
                result = CheckUP().put_ArchInfo(data_base_original=database_ArchInfo_original_dict,
                                                data_base_modified=database_ArchInfo_modoified_dict,
                                                JSON_settings=setting_generate
                                                )
                if len(result) > 0:
                    result = log(API_name='Meter db settings API - PUT - ' + str(self.name_table),
                                 Error=result,
                                 JSON=JSON,
                                 answer_JSON=answer_JSON,
                                 JSON_normal=None)
                return result
            else:
                result = log(API_name='Meter db settings API - PUT - ' + str(self.name_table),
                             Error=[JSON_setting, 'Ошибка при перезаписи'],
                             JSON=JSON,
                             answer_JSON=answer_JSON,
                             JSON_normal=None)
                return result
        else:
            result = log(API_name='Meter db settings API - PUT - ' + str(self.name_table),
                         Error=['Привышен лимит количества записей. Максимально число для использования: '
                    + str(len(database_ArchInfo_original_dict))],
                         JSON={'Не был сгенерирован': 'не был отправлен'},
                         answer_JSON={'не был отправлен': 'не был получен'},
                         JSON_normal=None)
            return result


# --------------------------------------------------------------------------------------------------------------------
#                                                   DELETE
# --------------------------------------------------------------------------------------------------------------------
class DELETE:
    """
        Класс для работы с методом DELETE
    """
    setting = None
    type_connect: str = 'virtualbox'

    def __init__(self, type_connect: str = 'virtualbox'):
        name_table = ""
        self.type_connect = type_connect

    # Дёргаем таблицу MeterTable

    def MeterTable(self, count_settings_generate: int = 3, count_settings_delete: int = 3, ids=None):
        """
        Тест для Метод для удаления из таблицы MeterTable.
        Здесь работает Генератор, который наполняет базу , и после чего удаляет заданное число элементов через JSON.
        Надо задать число сколько надо генерировать, а так же сколько надо удалять.
        Заложена возможность для ручного ввода через Id , но функционал вырезан

        Успешный тест возвращает пустой массив. Неуспешный - массив из словарей в которых описана ошибка.
        ошибка ищится по ключу error

        :param count_settings_generate: - Сюда пихаем число сколько генерим для базы полей
        :param count_settings_delete:  - Сюда пихаем сколько удаляем
        :param ids: - ручное задание ID - вырезано.
        :return: Массив из словарей. Если тест успешен , то массив пустой
        """

        # Наши переменные в этом методе :
        # сама таблица
        name_table = "MeterTable"
        # ее поля
        table_field = "*"
        # Все это начинает работать только если количество генераций больше или равно количеству удалений
        if (count_settings_generate >= 1) and (count_settings_generate >= count_settings_delete):
            # Первое - Чистим базу - всю
            sqlite.deleteMeterTable()
            # Второе - генерируем значения в базу - settings и ids для JSON , settings для БД
            generate = GeneratorForSettingsMeterTable(count_settings_generate)

            # Загружаем нужные нам ID
            sqlite.recording_MeterTable(generate.get_tuple())
            # Получаем всю БД

            dict_data_base_full = sqlite.readtable_return_dict(table_name=name_table)
            # Теперь надо сделать конструктор для ID котоыре полетят в удаление

            ids_del = generate.get_id_to_delete(count_settings_delete)
            # Переключатель на ручное управление
            # if ids != None:
            #     ids_del = ids
            # Теперь нам надо получить только те ID из БД которые дооолжны удалить
            if ids_del == None:
                must_delete = name_table + ''
            else:
                must_delete = tuple(ids_del)
                if len(must_delete) == 1:
                    must_delete = '( ' + str(must_delete[0]) + ' )'
                must_delete = name_table + ' WHERE  MeterTable.MeterId  IN ' + str(must_delete)
            # Получаем словарь того что должны были удалить по их ИД
            dict_data_base_must_delete = sqlite.readtable_return_dict(table_name=must_delete)
            # Теперь составляем нам нужный JSON
            JSON = Template_JSON_for_Meter_db_API.DELETE().MeterTable(setting=self.setting, ids=ids_del)
            # Замереем время
            time_start = time.time()

            JSON_Setup = Setup(JSON, API='meter_db_settings', type_connect=self.type_connect)
            answer_JSON = JSON_Setup.answer_JSON


            # Получаем время
            time_finis = time.time()

            print('JSON Обрабабатывался:', time_finis - time_start)
            # Теперь пихаем это все в обработчик ошибок
            JSON_setting = error_handler(answer_JSON)
            if (type(JSON_setting) == list) or (type(JSON_setting) == tuple):
                # для обработчика нам нужно :
                # база данных - селектим все
                dict_data_base = sqlite.readtable_return_dict(table_name=name_table)
                # После этого - пихаем это в обработчик
                result = CheckUP().delete_MeterTable_element(
                    database_list_full=dict_data_base_full,
                    database_list_after_deletion=dict_data_base,
                    ids=[ids_del],
                    data_base_list_must_delete=dict_data_base_must_delete
                )
                if len(result) > 0:
                    result = log(API_name='Meter db settings API - DELETE - ' + str(name_table),
                                 Error=result,
                                 JSON=JSON,
                                 answer_JSON=answer_JSON,
                                 JSON_normal=None)
                return result
            else:
                result = log(API_name='Meter db settings API - DELETE - ' + str(name_table),
                             Error=[JSON_setting, 'Ошибка при удалении'],
                             JSON=JSON,
                             answer_JSON=answer_JSON,
                             JSON_normal=None)
                return result
        else:
            result = log(API_name='Meter db settings API - DELETE - ' + str(name_table),
                         Error=['Неправильно заданы параметры удаления'],
                         JSON={'Не был сгенерирован': 'не был отправлен'},
                         answer_JSON={'не был отправлен': 'не был получен'},
                         JSON_normal=None)
            return result

# --------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------
#
# meter_settings = GET().MeterTable(count_get_ids=1, count_generate_ids=1)
# print(meter_settings)