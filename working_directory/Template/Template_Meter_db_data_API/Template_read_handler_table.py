# Здесь расположем наш обработчик для уже сформированного JSON чтоб прочитать нужные таблицы
from working_directory import sqlite
from copy import deepcopy
from working_directory.Template.Template_Meter_db_data_API import Template_SQL_request, Template_list_ArchTypes
from working_directory.Template.Template_Meter_db_data_API.Template_list_ArchTypes import \
    ElectricConfig_ArchType_name_list, \
    PulseConfig_ArchType_name_list, \
    DigitalConfig_ArchType_name_list, \
    ElecticEnergyValues_ArchType_name_list, \
    ElectricQualityValues_ArchType_name_list, \
    ElectricPowerValues_ArchType_name_list, \
    PulseValues_ArchType_name_list, \
    DigitalValues_ArchType_name_list, \
    JournalValues_ArchType_name_list


class ReceivingDataAccordingToJSON:
    """
    Данный класс работает разбирает JSON и чистает бд исходя из JSON

    """

    JSON = None
    result = None
    allMeters = None
    column = None
    table_name = None
    allMeters = None
    where_DeviceIdx = None
    where_MeterId = None
    where_Serial = None
    where_Timestamp = None
    __all_tag = None

    def __init__(self, JSON, Select_all: bool = True):
        self.allMeters = None
        self.column = None
        self.table_name = None
        self.allMeters = None
        self.where_DeviceIdx = None
        self.where_MeterId = None
        self.where_Serial = None
        self.where_Timestamp = None
        self.__all_tag = None
        self.result = None

        self.JSON = JSON
        self.result = self.__method_definition(JSON=JSON, Select_all=Select_all)

    def get_result(self):
        return deepcopy(self.result)

    def __method_definition(self, JSON: dict, Select_all: bool = True):
        """
        Сначала определяем по какой ветке мы двигаемся , и какого типа этот JSON
        :param JSON:
        :return:
        """

        method = JSON["method"]
        if method == 'post':
            result = self.__select_to_database_by_JSON_POST(JSON['measures'], Select_all=Select_all)
        if method == 'get':
            result = self.__select_to_database_by_JSON_GET(JSON)

        return result

    # здесь будут методы POST Методов JSON
    # ----------------------------------------------POST----------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Конструкторы запроса - конструируем наши запросы
    def __formation_sql_request_select_by_id(self, json_list_devices: list):
        command_str = '''AND
    	                    DeviceIdx in  '''
        command_str_len = []
        for i in range(len(json_list_devices)):
            command_str_len.append(json_list_devices[i]['id'])

        command_str_len = ' ( ' + str(command_str_len)[1:-1] + ' ) '
        command_str = command_str + str(command_str_len)

        return command_str

    #     Конструктор простой - селект
    def __formation_sql_request_select(self, sql_request: str, json_list_devices: list, Select_all: bool):
        # Сначала проверяем надо ли нам селектить по ИД
        if not Select_all:
            select_by_id = self.__formation_sql_request_select_by_id(json_list_devices=json_list_devices)

            final_command = sql_request + " " + select_by_id
        else:
            final_command = sql_request

        return final_command

    # ------------------------------------------------------------------------------------------------------------------
    #     Обработчик - добавление поля NAME
    def __added_key_name_to_result_select(self, result_select: list, ArchTypeName: str):
        for i in range(len(result_select)):
            if type(result_select[i]) == dict:
                result_select[i]['Name'] = ArchTypeName

        return result_select

    # ------------------------------------------------------------------------------------------------------------------
    # Обработчик для таблицы ElectricConfig , DigitalConfig , PulseConfig
    def __selected_Config(self, Select_all: bool, measures: dict, sql_command_to_table: str):
        # Здесь все просто - Собираем команду воедино , и селектим
        command = self.__formation_sql_request_select(sql_request=sql_command_to_table,
                                                      json_list_devices=measures['devices'],
                                                      Select_all=Select_all)
        # Теперь отправляем нашу команду куда надо
        result_select = sqlite.execute_command_to_read_return_dict(command=command)

        if len(result_select) != 0:
            # А теперь проходимся по каждому элементу что заселектили и добавляем нужный параметр
            result_select = self.__added_key_name_to_result_select(result_select=result_select,
                                                                   ArchTypeName=measures['measure'])
        else:
            result_select = []

        return result_select

    # Обработчик для таблиц для которых надо формировать представления :
    # ElectricEnergyValues , ElectricQualityValues
    def __selected_with_view(self, Select_all: bool,
                             measures: dict,
                             sql_command_to_table_select: list,
                             sql_command_to_table_create_view: list,
                             sql_command_to_table_delete_view: list
                             ):

        # command = self.__formation_sql_request_select(sql_request=sql_command_to_table_select,
        #                                               json_list_devices=measures['devices'],
        #                                               Select_all=Select_all)
        #
        # # Теперь отправляем нашу команду куда надо
        # result_select = sqlite.execute_selected_to_view_return_dict(command_select=command,
        #                                                             command_create_view=sql_command_to_table_create_view,
        #                                                             command_delete_view=sql_command_to_table_delete_view)

        # Итак - все хуйня - начнем по новой - Получаем данные из MeterDadata
        result = deepcopy(SelectToDataBase(JSON_measure=measures, select_all=Select_all,
                                           Command_table_list=sql_command_to_table_select).result)

        print('-----------------------------------------------')

        return result

    def __selected_with_meterdata_and_another_table(self, Select_all: bool, measures: dict,
                                                    sql_command_to_table_select: str):

        # Здесь все просто - Собираем команду воедино , и селектим
        command = self.__formation_sql_request_select(sql_request=sql_command_to_table_select,
                                                      json_list_devices=measures['devices'],
                                                      Select_all=Select_all)

        # Теперь отправляем нашу команду куда надо

        result_select = sqlite.execute_command_to_read_return_dict(command=command)

        return result_select

    # ------------------------------------------------------------------------------------------------------------------
    #   Здесь опрелеляем команду и таблицу к которой у нас пойдет все в дальнейшем.
    def __table_qualifier(self, JSON_measures_dict: dict, Select_all: bool = True):

        measure = JSON_measures_dict['measure']

        # ElectricConfig
        if (measure in ElectricConfig_ArchType_name_list):
            sql_command_to_table = Template_SQL_request.ElectricConfig_Select
            result_select = self.__selected_Config(Select_all=Select_all,
                                                   measures=JSON_measures_dict,
                                                   sql_command_to_table=sql_command_to_table)

        # DigitalConfig
        elif measure in DigitalConfig_ArchType_name_list:
            sql_command_to_table = Template_SQL_request.DigitalConfig_select
            result_select = self.__selected_Config(Select_all=Select_all,
                                                   measures=JSON_measures_dict,
                                                   sql_command_to_table=sql_command_to_table)

        # PulseConfig
        elif measure in PulseConfig_ArchType_name_list:
            sql_command_to_table = Template_SQL_request.PulseConfig_select
            result_select = self.__selected_Config(Select_all=Select_all,
                                                   measures=JSON_measures_dict,
                                                   sql_command_to_table=sql_command_to_table)


        # ElecticEnergyValues
        elif measure in ElecticEnergyValues_ArchType_name_list:
            # # здесь аккуратнее - надо все делать в несколько команд
            # sql_command_to_table_select = Template_SQL_request.ElectricEnergyValues_select
            # sql_command_to_table_create_view = Template_SQL_request.ElectricEnergyValues_create_rate_views
            # sql_command_to_table_delete_view = Template_SQL_request.ElectricEnergyValues_delete_rate_views

            command = Template_SQL_request.ElectricEnergyValues_select_list

            result_select = deepcopy(SelectToDataBase(JSON_measure=JSON_measures_dict,
                                                      select_all=Select_all,
                                                      Command_table_list=command).result)

            # result_select = self.__selected_with_view(Select_all=Select_all,
            #                                           measures=JSON_measures_dict,
            #                                           sql_command_to_table_select=command,
            #                                           sql_command_to_table_create_view=sql_command_to_table_create_view,
            #                                           sql_command_to_table_delete_view=sql_command_to_table_delete_view)

        # ElectricQualityValues
        elif measure in ElectricQualityValues_ArchType_name_list:
            # здесь аккуратнее - надо все делать в несколько команд
            # sql_command_to_table_select = Template_SQL_request.ElectricQualityValues_select
            # sql_command_to_table_create_view = Template_SQL_request.ElectricQualityValues_create_rate_views
            # sql_command_to_table_delete_view = Template_SQL_request.ElectricQualityValues_delete_rate_views
            #
            # result_select = self.__selected_with_view(Select_all=Select_all,
            #                                           measures=JSON_measures_dict,
            #                                           sql_command_to_table_select=sql_command_to_table_select,
            #                                           sql_command_to_table_create_view=sql_command_to_table_create_view,
            #                                           sql_command_to_table_delete_view=sql_command_to_table_delete_view)

            command = Template_SQL_request.ElectricQualityValues_select_list

            result_select = deepcopy(SelectToDataBase(JSON_measure=JSON_measures_dict,
                                                      select_all=Select_all,
                                                      Command_table_list=command).result)

        # ElectricPowerValues
        elif measure in ElectricPowerValues_ArchType_name_list:
            # sql_command_to_table = Template_SQL_request.ElectricPowerValues_select
            #
            #
            # result_select = self.__selected_with_meterdata_and_another_table(Select_all=Select_all,
            #                                                                  measures=JSON_measures_dict,
            #                                                                  sql_command_to_table_select=sql_command_to_table
            #                                                                  )

            command = Template_SQL_request.ElectricPowerValues_select_list

            result_select = deepcopy(SelectToDataBase(JSON_measure=JSON_measures_dict,
                                                      select_all=Select_all,
                                                      Command_table_list=command).result)

        # PulseValues
        elif measure in PulseValues_ArchType_name_list:
            # sql_command_to_table = Template_SQL_request.PulseValues_select
            #
            # result_select = self.__selected_with_meterdata_and_another_table(Select_all=Select_all,
            #                                                                  measures=JSON_measures_dict,
            #                                                                  sql_command_to_table_select=sql_command_to_table
            #                                                                  )

            command = Template_SQL_request.PulseValues_select_list

            result_select = deepcopy(SelectToDataBase(JSON_measure=JSON_measures_dict,
                                                      select_all=Select_all,
                                                      Command_table_list=command).result)

        # DigitalValues
        elif measure in DigitalValues_ArchType_name_list:
            # sql_command_to_table = Template_SQL_request.DigitalValues_select
            #
            # result_select = self.__selected_with_meterdata_and_another_table(Select_all=Select_all,
            #                                                                  measures=JSON_measures_dict,
            #                                                                  sql_command_to_table_select=sql_command_to_table
            #                                                                  )

            command = Template_SQL_request.DigitalValues_select_list

            result_select = deepcopy(SelectToDataBase(JSON_measure=JSON_measures_dict,
                                                      select_all=Select_all,
                                                      Command_table_list=command).result)
        # JournalValues
        elif measure in JournalValues_ArchType_name_list:
            # sql_command_to_table = Template_SQL_request.JournalValues_select
            #
            # result_select = self.__selected_with_meterdata_and_another_table(Select_all=Select_all,
            #                                                                  measures=JSON_measures_dict,
            #                                                                  sql_command_to_table_select=sql_command_to_table
            #                                                                  )

            command = Template_SQL_request.JournalValues_select_list

            result_select = deepcopy(SelectToDataBase(JSON_measure=JSON_measures_dict,
                                                      select_all=Select_all,
                                                      Command_table_list=command).result)

        else:
            result_select = [None]

        return result_select

    # ------------------------------------------------------------------------------------------------------------------

    def __select_to_database_by_JSON_POST(self, JSON_measures: list, Select_all: bool):
        select_to_database = []
        for i in range(len(JSON_measures)):
            # # Старый способ
            result_select = self.__table_qualifier(JSON_measures_dict=JSON_measures[i], Select_all=Select_all)
            select_to_database.append(result_select)
        return select_to_database

    # ----------------------------------------------GET----------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # Здесь напишем сборщик для селекта

    def __select_to_database_by_JSON_GET(self, JSON):
        self.JSON = JSON

        result_full = []

        # определяем таблицы
        for i in range(len(self.JSON['measures'])):
            result = self.__get_define_table(self.JSON['measures'][i])
            result_full = result_full + result

        return result_full

    # правило первое  - смотрим таблицу
    def __get_define_table(self, measure):
        self.__measure = measure
        # ElectricConfig
        if measure in ElectricConfig_ArchType_name_list:
            # Определяем поля
            table_config = 'ElectricConfig'
            self.table_name = ' ElectricConfig   WHERE   '
            self.dict_tag = Template_SQL_request.dictionary_of_correspondences['ElectricConfig']
            self.__all_tag = Template_list_ArchTypes.ElectricConfig_tag
            # Определяем начало команды
            result = self.__select_get_config(table=self.table_name, table_config=table_config)


        # DigitalConfig
        elif measure in DigitalConfig_ArchType_name_list:
            # Определяем поля
            table_config = 'DigitalConfig'
            self.table_name = ' DigitalConfig  WHERE  '
            self.dict_tag = Template_SQL_request.dictionary_of_correspondences['DigitalConfig']
            self.__all_tag = Template_list_ArchTypes.DigitalConfig_tag
            result = self.__select_get_config(table=self.table_name, table_config=table_config)


        # PulseConfig
        elif measure in PulseConfig_ArchType_name_list:

            # Определяем поля
            table_config = 'PulseConfig'
            self.table_name = ' PulseConfig  WHERE  '
            self.dict_tag = Template_SQL_request.dictionary_of_correspondences['PulseConfig']
            self.__all_tag = Template_list_ArchTypes.PulseConfig_tag
            result = self.__select_get_config(table=self.table_name, table_config=table_config)

        # ElecticEnergyValues
        elif measure in ElecticEnergyValues_ArchType_name_list:
            # здесь аккуратнее - надо все делать в несколько команд
            self.table_name = """  MeterData, ArchTypes , TARIF0 , TARIF1 , TARIF2 , TARIF3 , TARIF4
        WHERE ArchTypes.Id = MeterData.RecordTypeId AND MeterData.Id = TARIF0.Id AND MeterData.Id = TARIF1.Id AND MeterData.Id = TARIF2.Id AND  MeterData.Id = TARIF3.Id AND MeterData.Id = TARIF4.Id  """

            # Определим команды для создания представлений и удаления их
            create_view = Template_SQL_request.ElectricEnergyValues_create_rate_views
            delete_view = Template_SQL_request.ElectricEnergyValues_delete_rate_views
            self.dict_tag = Template_SQL_request.dictionary_of_correspondences['ElecticEnergyValues']
            self.__all_tag = Template_list_ArchTypes.ElecticEnergyValues_tag
            result = self.__select_get_table_with_view(table=self.table_name, create_view=create_view,
                                                       delete_view=delete_view)

        # ElectricQualityValues
        elif measure in ElectricQualityValues_ArchType_name_list:
            # здесь аккуратнее - надо все делать в несколько команд
            self.table_name = """  MeterData, ArchTypes , Phase_A , Phase_B , Phase_C , Phase_Summ  WHERE 
            ArchTypes.Id = MeterData.RecordTypeId AND MeterData.Id = Phase_A.Id AND MeterData.Id = Phase_B.Id AND MeterData.Id = Phase_C.Id AND MeterData.Id = Phase_Summ.Id  """
            # Определим команды для создания представлений и удаления их
            create_view = Template_SQL_request.ElectricQualityValues_create_rate_views
            delete_view = Template_SQL_request.ElectricQualityValues_delete_rate_views
            self.dict_tag = Template_SQL_request.dictionary_of_correspondences['ElectricQualityValues']
            self.__all_tag = Template_list_ArchTypes.ElectricQualityValues_tag
            result = self.__select_get_table_with_view(table=self.table_name, create_view=create_view,
                                                       delete_view=delete_view)

        # ElectricPowerValues
        elif measure in ElectricPowerValues_ArchType_name_list:
            table_config = ' ElectricConfig  '
            self.table_name = """  MeterData, ArchTypes , ElectricPowerValues
             WHERE
             ElectricPowerValues.Id = MeterData.Id  AND ArchTypes.Id = MeterData.RecordTypeId 
               """
            self.dict_tag = Template_SQL_request.dictionary_of_correspondences['ElectricPowerValues']
            self.__all_tag = Template_list_ArchTypes.ElectricPowerValues_tag
            result = self.__select_get_table_with_meterdata(table=self.table_name, table_config=table_config)

        # PulseValues
        elif measure in PulseValues_ArchType_name_list:
            # table_config = ' PulseConfig '
            table_config = ' ElectricConfig  '
            self.table_name = """  MeterData, ArchTypes , PulseValues
             WHERE
             ArchTypes.Id = MeterData.RecordTypeId AND PulseValues.Id = MeterData.Id
               """
            self.dict_tag = Template_SQL_request.dictionary_of_correspondences['PulseValues']
            self.__all_tag = Template_list_ArchTypes.PulseValues_tag
            result = self.__select_get_table_with_meterdata(table=self.table_name, table_config=table_config)

        # DigitalValues
        elif measure in DigitalValues_ArchType_name_list:
            # table_config = ' DigitalConfig '
            table_config = ' ElectricConfig  '
            self.table_name = """  MeterData, ArchTypes , DigitalValues
             WHERE
             ArchTypes.Id = MeterData.RecordTypeId AND DigitalValues.Id = MeterData.Id
               """
            self.dict_tag = Template_SQL_request.dictionary_of_correspondences['DigitalValues']
            self.__all_tag = Template_list_ArchTypes.DigitalValues_tag
            result = self.__select_get_table_with_meterdata(table=self.table_name, table_config=table_config)

        # JournalValues
        elif measure in JournalValues_ArchType_name_list:
            table_config = ' ElectricConfig  '
            self.table_name = """  MeterData, ArchTypes , JournalValues
             WHERE
             ArchTypes.Id = MeterData.RecordTypeId AND JournalValues.Id = MeterData.Id
              """
            self.dict_tag = Template_SQL_request.dictionary_of_correspondences['JournalValues']
            self.__all_tag = Template_list_ArchTypes.JournalValues_tag
            result = self.__select_get_table_with_meterdata(table=self.table_name, table_config=table_config)


        else:
            result = None

        return result

    # теперь разбираем по разным селектам
    def __get_parse_answer(self):
        # с таблицей определись -

        # теперь смотрим по различным флагам
        # первый флаг - ид
        self.allMeters = self.__get_define_allMeters()
        # если этого тэга нет стоит в неправде - можно селектить по id
        if not self.allMeters:
            # Проверяем наличие селекта по внутренему ид
            self.where_DeviceIdx = self.__get_command_select_DeviceIdx()
            # Проверяем наличие селекта по внешнему ид
            self.where_MeterId = self.__get_command_select_MeterId()
            # Проверяем наличие селекта по серийнику
            self.where_Serial = self.__get_command_select_Serial()
        # второй флаг - время
        self.where_Timestamp = self.__get_command_select_Timestamp()

        self.lastTime = self.__get_define_lastTime()
        if self.lastTime:
            # ЕСли он есть - то добавляем к команде
            self.where_Timestamp = self.where_Timestamp + " ORDER BY Timestamp DESC LIMIT 1 "

        # Теперь собираем команды по тэгам
        self.column = self.__get_command_select_tag()

        # Теперь когда собрали все команды , делаем запросы !!

    # -----------------------------------------Сборщик команд ---------------------------------------------------------
    # Конфиги:
    def __select_get_config(self, table, table_config):
        # Первое - собираем нужные переменные
        self.__get_parse_answer()
        # Проверяем наличие тэга селектим все
        result = []
        # Селектим конфиги по схеме
        if self.allMeters:

            # Сначала выгребаем из MeterTable все возможные записи
            command_select = 'SELECT MeterTable.DeviceIdx AS deviceIdx , MeterTable.MeterId AS meter  FROM MeterTable '
            result_select_of_MeterTable = sqlite.execute_command_to_read_return_dict(command=command_select)

            # После чего ПО ЭЛЕМЕНТНО СЕЛЕКТИМ по каждому айдишнику их связь в таблице Конфига
            for i in range(len(result_select_of_MeterTable)):

                # Если у нас нет колонок , то мы селектим без них
                if len(self.column) > 0:
                    # Добавляем Нужное время и точ то есть в таблциееее!!!
                    command_select = 'SELECT  ' + str(
                        self.column) + ' , ' + table_config + '.Timestamp AS ts ' + ' FROM ' + table + \
                                     '  DeviceIdx IN ( ' + str(
                        result_select_of_MeterTable[i]['deviceIdx']) + ' ) ' + \
                                     str(self.where_Timestamp)
                else:
                    command_select = 'SELECT  ' + table_config + '.Timestamp AS ts ' + ' FROM ' + table + \
                                     '  DeviceIdx IN ( ' + str(
                        result_select_of_MeterTable[i]['deviceIdx']) + ' ) ' + \
                                     str(self.where_Timestamp)
                # Отправляем это все в космос
                result_select_of_MeterData = sqlite.execute_command_to_read_return_dict(command=command_select)

                # После чего КАЖДОМУ РЕЗУЛЬТАТУ ДОБАВЛЯЕМ этот айдишник
                result_select = []
                if len(result_select_of_MeterData) > 0:
                    for x in range(len(result_select_of_MeterData)):
                        result_select_dict = result_select_of_MeterData[x]
                        result_select_dict['measure'] = str(self.__measure)
                        result_select_dict.update(result_select_of_MeterTable[i])
                        result_select.append(result_select_dict)

                # ЕСЛИ У НАС ПУСТОТА , ТО ДОБАВЛЯЕМ ПУСТОТУ
                else:

                    result_select_dict = result_select_of_MeterTable[i]
                    result_select_dict['measure'] = str(self.__measure)
                    result_select_dict['vals'] = None
                    result_select.append(result_select_of_MeterTable[i])

                result = result + result_select

        else:

            if self.where_DeviceIdx is not None:

                # Если не пустота , то селектим по внутренему айдишнику
                idx = self.where_DeviceIdx
                # Сначала выгребаем Айдишники
                command_select = 'SELECT MeterTable.DeviceIdx AS deviceIdx FROM MeterTable ' + \
                                 ' WHERE MeterTable.DeviceIdx IN (' + str(idx)[1:-1] + ' ) '
                result_select_of_MeterTable_where_DeviceIdx = sqlite.execute_command_to_read_return_dict(
                    command=command_select
                )

                # После чего для каждого выбранного айдишника формируем нужные вариации команды
                for i in range(len(result_select_of_MeterTable_where_DeviceIdx)):

                    if len(self.column) > 0:
                        # Здесь нужна запятая после self.column
                        command = 'SELECT  ' + str(self.column) + '  , ' + \
                                  table_config + '.Timestamp AS ts   FROM ' + table + " " + ' DeviceIdx IN (' + \
                                  str(result_select_of_MeterTable_where_DeviceIdx[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)
                    else:
                        command = 'SELECT  ' + \
                                  table_config + '.Timestamp AS ts   FROM ' + table + " " + ' DeviceIdx IN (' + \
                                  str(result_select_of_MeterTable_where_DeviceIdx[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)

                    # Опускаем это  в функцию обработчик
                    result_where_DeviceIdx = sqlite.execute_command_to_read_return_dict(command=command)
                    # После чего КАЖДОМУ РЕЗУЛЬТАТУ ДОБАВЛЯЕМ этот айдишник

                    result_select = []
                    if len(result_where_DeviceIdx) > 0:
                        for x in range(len(result_where_DeviceIdx)):
                            result_select_dict = result_where_DeviceIdx[x]
                            result_select_dict['measure'] = str(self.__measure)
                            result_select_dict.update(result_select_of_MeterTable_where_DeviceIdx[i])
                            result_select.append(result_select_dict)

                        # ЕСЛИ У НАС ПУСТОТА , ТО ДОБАВЛЯЕМ ПУСТОТУ
                    else:
                        result_select_dict = result_select_of_MeterTable_where_DeviceIdx[i]
                        result_select_dict['measure'] = str(self.__measure)
                        result_select_dict['vals'] = None
                        result_select.append(result_select_of_MeterTable_where_DeviceIdx[i])
                    # Добавляем Полученный Результат
                    result = result + result_select
            if self.where_MeterId is not None:

                # Если не пустота , то селектим по внутренему айдишнику
                idx = self.where_MeterId
                # Сначала выгребаем Айдишники
                command_select = 'SELECT' + \
                                 ' MeterTable.MeterId AS meter , MeterTable.DeviceIdx AS deviceIdx FROM MeterTable ' + \
                                 ' WHERE MeterTable.MeterId IN (' + str(idx)[1:-1] + ' ) '
                result_select_of_MeterTable_where_MeterId = sqlite.execute_command_to_read_return_dict(
                    command=command_select
                )
                # После чего для каждого выбранного айдишника формируем нужные вариации команды
                for i in range(len(result_select_of_MeterTable_where_MeterId)):
                    # Здесь нужна запятая после str(self.column)

                    if len(self.column) > 0:

                        command = 'SELECT  ' + str(self.column) + \
                                  '  , ' + table_config + '.Timestamp AS ts  FROM ' + \
                                  table + '  DeviceIdx IN (' + \
                                  str(result_select_of_MeterTable_where_MeterId[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)

                    else:
                        command = 'SELECT  ' + \
                                  table_config + '.Timestamp AS ts  FROM ' + \
                                  table + '  DeviceIdx IN (' + \
                                  str(result_select_of_MeterTable_where_MeterId[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)

                    # Опускаем это  в функцию обработчик
                    result_where_DeviceIdx = sqlite.execute_command_to_read_return_dict(command=command)

                    # После чего КАЖДОМУ РЕЗУЛЬТАТУ ДОБАВЛЯЕМ этот айдишник
                    result_select = []
                    if len(result_where_DeviceIdx) > 0:
                        for x in range(len(result_where_DeviceIdx)):
                            result_select_dict = result_where_DeviceIdx[x]
                            result_select_dict['measure'] = str(self.__measure)
                            result_select_dict.update(result_select_of_MeterTable_where_MeterId[i])
                            result_select.append(result_select_dict)

                        # ЕСЛИ У НАС ПУСТОТА , ТО ДОБАВЛЯЕМ ПУСТОТУ
                    else:
                        result_select_dict = result_select_of_MeterTable_where_MeterId[i]
                        result_select_dict['measure'] = str(self.__measure)
                        result_select_dict['vals'] = None
                        result_select.append(result_select_of_MeterTable_where_MeterId[i])
                    # Добавляем Полученный Результат

                    result = result + result_select

            # # Теперь предстоит совсем жаришка - селект по cерийнику.
            if self.where_Serial is not None:
                # Берем серийник
                idx = self.where_Serial
                # Здесь c конфигами куда интереснее - он спускается сверху

                # # Сначала выгребаем Айдишники по серийнику
                idx_list = []
                for i in range(len(idx)):
                    command_select = 'SELECT ' + ' Serial as serials , ' + \
                                     ' DeviceIdx AS  deviceIdx FROM  ' + \
                                     table + ' Serial LIKE  \'%' + str(idx[i]) + '%\''

                    result_select_of_MeterTable_where_Serial = sqlite.execute_command_to_read_return_dict(
                        command=command_select
                    )
                    idx_list = idx_list + result_select_of_MeterTable_where_Serial

                # После чего для каждого выбранного айдишника формируем нужные вариации команды
                for i in range(len(idx_list)):

                    if len(self.column) > 0:
                        command = 'SELECT  ' + str(self.column) + \
                                  ' , ' + table_config + '.Timestamp AS ts FROM ' + \
                                  table + ' DeviceIdx IN ( ' + \
                                  str(idx_list[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)

                    else:
                        command = 'SELECT  ' + table_config + '.Timestamp AS ts FROM ' + \
                                  table + ' DeviceIdx IN ( ' + \
                                  str(idx_list[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)

                    # Опускаем это  в функцию обработчик
                    result_where_Serial = sqlite.execute_command_to_read_return_dict(command=command)

                    # После чего КАЖДОМУ РЕЗУЛЬТАТУ ДОБАВЛЯЕМ этот айдишник
                    result_select = []
                    if len(result_where_Serial) > 0:
                        for x in range(len(result_where_Serial)):
                            result_select_dict = result_where_Serial[x]
                            result_select_dict['measure'] = str(self.__measure)
                            result_select_dict.update(idx_list[i])
                            result_select.append(result_select_dict)

                        # ЕСЛИ У НАС ПУСТОТА , ТО ДОБАВЛЯЕМ ПУСТОТУ
                    else:
                        result_select_dict = idx_list[i]
                        result_select_dict['measure'] = str(self.__measure)
                        result_select_dict['vals'] = None
                        result_select.append(result_select_dict)
                    result = result + result_select

        return result

    def __select_element_config(self, collum: str, table_name1: str, idx: list, table_name2: str = ' '):
        result = []
        for i in range(len(idx)):
            # Далее добавляем время и запускаем по элементный селект
            result_select = sqlite.readtable_return_dict(
                collum=collum, table_name=str(table_name1) + str(idx[i]) + str(table_name2) + str(
                    self.where_Timestamp))
            # Выбираем первый элемет
            result_select = result_select[0]
            # Добавляем ему имя
            result_select['measure'] = self.__measure
            # И первый элемент добавляем в  основной массив
            result.append(result_select)
        return result

    # -----------------------------------------------------------------------------------------------------------------
    # Простые двойные таблицы которые требуют селекта только из meter data
    def __select_get_table_with_meterdata(self, table, table_config):
        # Первое - собираем нужные переменные
        self.__get_parse_answer()
        # Проверяем наличие тэга селектим все
        result = []
        if self.allMeters:

            # Делаем по примекру с представлениями

            # Сначала выгребаем из MeterTable все возможные записи
            command_select = 'SELECT MeterTable.DeviceIdx AS deviceIdx , MeterTable.MeterId AS meter  FROM MeterTable '
            result_select_of_MeterTable = sqlite.execute_command_to_read_return_dict(command=command_select)

            # После чего ПО ЭЛЕМЕНТНО СЕЛЕКТИМ по каждому айдишнику их связь в таблице METERDATA
            for i in range(len(result_select_of_MeterTable)):

                # Создаем Временное Представление, для удобности селекта

                # Добавляем Нужное время и точ то есть в таблциееее!!!
                if len(self.column) > 0:
                    command_select = 'SELECT MeterData.Timestamp AS ts , ArchTypes.Name AS measure , ' + str(
                        self.column) + ' FROM ' + table + \
                                     " AND ArchTypes.Name = \'" + str(self.__measure) + "\'" + \
                                     ' AND MeterData.DeviceIdx IN ( ' + str(
                        result_select_of_MeterTable[i]['deviceIdx']) + ' )  ' + \
                                     str(self.where_Timestamp)

                else:
                    command_select = 'SELECT MeterData.Timestamp AS ts , ArchTypes.Name AS measure  ' + ' FROM ' + \
                                     table + " AND ArchTypes.Name = \'" + str(self.__measure) + "\'" + \
                                     ' AND MeterData.DeviceIdx IN ( ' + str(
                        result_select_of_MeterTable[i]['deviceIdx']) + ' )  ' + \
                                     str(self.where_Timestamp)

                # Отправляем это все в космос
                result_select_of_MeterData = sqlite.execute_command_to_read_return_dict(command=command_select)

                # После чего КАЖДОМУ РЕЗУЛЬТАТУ ДОБАВЛЯЕМ этот айдишник
                result_select = []
                if len(result_select_of_MeterData) > 0:
                    for x in range(len(result_select_of_MeterData)):
                        result_select_dict = result_select_of_MeterData[x]
                        result_select_dict.update(result_select_of_MeterTable[i])
                        result_select.append(result_select_dict)

                # ЕСЛИ У НАС ПУСТОТА , ТО ДОБАВЛЯЕМ ПУСТОТУ
                else:
                    result_select_dict = result_select_of_MeterTable[i]
                    result_select_dict['measure'] = str(self.__measure)
                    result_select_dict['vals'] = None
                    result_select.append(result_select_of_MeterTable[i])

                result = result + result_select

        else:

            if self.where_DeviceIdx is not None:

                # Если не пустота , то селектим по внутренему айдишнику
                idx = self.where_DeviceIdx
                # Сначала выгребаем Айдишники
                command_select = 'SELECT MeterTable.DeviceIdx AS deviceIdx FROM MeterTable ' + \
                                 ' WHERE MeterTable.DeviceIdx IN (' + str(idx)[1:-1] + ' ) '
                result_select_of_MeterTable_where_DeviceIdx = sqlite.execute_command_to_read_return_dict(
                    command=command_select
                )

                # После чего для каждого выбранного айдишника формируем нужные вариации команды
                for i in range(len(result_select_of_MeterTable_where_DeviceIdx)):
                    if len(self.column) > 0:
                        command = 'SELECT  ' + str(self.column) + \
                                  ' , MeterData.Timestamp AS ts , ArchTypes.Name AS measure FROM ' + \
                                  table + " AND ArchTypes.Name = \'" + str(
                            self.__measure) + "\'" + ' AND MeterData.DeviceIdx IN (' + \
                                  str(result_select_of_MeterTable_where_DeviceIdx[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)
                    else:
                        command = 'SELECT  ' + ' MeterData.Timestamp AS ts , ArchTypes.Name AS measure FROM ' + \
                                  table + " AND ArchTypes.Name = \'" + str(self.__measure) + \
                                  "\'" + ' AND MeterData.DeviceIdx IN (' + \
                                  str(result_select_of_MeterTable_where_DeviceIdx[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)
                    # Опускаем это  в функцию обработчик
                    result_where_DeviceIdx = sqlite.execute_command_to_read_return_dict(command=command)
                    # После чего КАЖДОМУ РЕЗУЛЬТАТУ ДОБАВЛЯЕМ этот айдишник
                    result_select = []
                    if len(result_where_DeviceIdx) > 0:
                        for x in range(len(result_where_DeviceIdx)):
                            result_select_dict = result_where_DeviceIdx[x]
                            result_select_dict.update(result_select_of_MeterTable_where_DeviceIdx[i])
                            result_select.append(result_select_dict)

                        # ЕСЛИ У НАС ПУСТОТА , ТО ДОБАВЛЯЕМ ПУСТОТУ
                    else:
                        result_select_dict = result_select_of_MeterTable_where_DeviceIdx[i]
                        result_select_dict['measure'] = str(self.__measure)
                        result_select_dict['vals'] = None
                        result_select.append(result_select_of_MeterTable_where_DeviceIdx[i])
                    # Добавляем Полученный Результат
                    result = result + result_select

            if self.where_MeterId is not None:

                # Если не пустота , то селектим по внутренему айдишнику
                idx = self.where_MeterId
                # Сначала выгребаем Айдишники
                command_select = 'SELECT' + \
                                 ' MeterTable.MeterId AS meter , MeterTable.DeviceIdx AS deviceIdx FROM MeterTable ' + \
                                 ' WHERE MeterTable.MeterId IN (' + str(idx)[1:-1] + ' ) '
                result_select_of_MeterTable_where_MeterId = sqlite.execute_command_to_read_return_dict(
                    command=command_select
                )
                # После чего для каждого выбранного айдишника формируем нужные вариации команды
                for i in range(len(result_select_of_MeterTable_where_MeterId)):

                    if len(self.column) > 0:
                        command = 'SELECT  ' + str(self.column) + \
                                  ' , MeterData.Timestamp AS ts , ArchTypes.Name AS measure FROM ' + \
                                  table + " AND ArchTypes.Name = \'" + str(
                            self.__measure) + "\'" + ' AND MeterData.DeviceIdx IN (' + \
                                  str(result_select_of_MeterTable_where_MeterId[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)
                    else:
                        command = 'SELECT  ' + ' MeterData.Timestamp AS ts , ArchTypes.Name AS measure FROM ' + \
                                  table + " AND ArchTypes.Name = \'" + str(self.__measure) + \
                                  "\'" + ' AND MeterData.DeviceIdx IN (' + \
                                  str(result_select_of_MeterTable_where_MeterId[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)
                    # Опускаем это  в функцию обработчик
                    result_where_DeviceIdx = sqlite.execute_command_to_read_return_dict(command=command)

                    # После чего КАЖДОМУ РЕЗУЛЬТАТУ ДОБАВЛЯЕМ этот айдишник
                    result_select = []
                    if len(result_where_DeviceIdx) > 0:
                        for x in range(len(result_where_DeviceIdx)):
                            result_select_dict = result_where_DeviceIdx[x]
                            result_select_dict.update(result_select_of_MeterTable_where_MeterId[i])
                            result_select.append(result_select_dict)

                        # ЕСЛИ У НАС ПУСТОТА , ТО ДОБАВЛЯЕМ ПУСТОТУ
                    else:
                        result_select_dict = result_select_of_MeterTable_where_MeterId[i]
                        result_select_dict['measure'] = str(self.__measure)
                        result_select_dict['vals'] = None
                        result_select.append(result_select_of_MeterTable_where_MeterId[i])
                    # Добавляем Полученный Результат

                    result = result + result_select

            # # Теперь предстоит совсем жаришка - селект по cерийнику.
            if self.where_Serial is not None:
                # Берем серийник
                idx = self.where_Serial
                # Здесь c конфигами куда интереснее - он спускается сверху

                # # Сначала выгребаем Айдишники по серийнику
                idx_list = []
                for i in range(len(idx)):
                    command_select = 'SELECT ' + ' Serial as serials , ' + \
                                     ' DeviceIdx AS  deviceIdx FROM  ' + table_config + \
                                     ' WHERE ' + ' Serial LIKE  \'%' + str(idx[i]) + '%\''

                    result_select_of_MeterTable_where_Serial = sqlite.execute_command_to_read_return_dict(
                        command=command_select
                    )
                    idx_list = idx_list + result_select_of_MeterTable_where_Serial

                # После чего для каждого выбранного айдишника формируем нужные вариации команды
                for i in range(len(idx_list)):
                    if len(self.column) > 0:
                        command = 'SELECT  ' + str(self.column) + \
                                  ' , MeterData.Timestamp AS ts , ArchTypes.Name AS measure FROM ' + \
                                  table + " AND ArchTypes.Name = \'" + str(
                            self.__measure) + "\'" + ' AND MeterData.DeviceIdx IN ( ' + \
                                  str(idx_list[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)
                    else:
                        command = 'SELECT  ' + ' MeterData.Timestamp AS ts , ArchTypes.Name AS measure FROM ' + \
                                  table + " AND ArchTypes.Name = \'" + str(self.__measure) + \
                                  "\'" + ' AND MeterData.DeviceIdx IN ( ' + \
                                  str(idx_list[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)

                    # Опускаем это  в функцию обработчик
                    result_where_Serial = sqlite.execute_command_to_read_return_dict(command=command)

                    # После чего КАЖДОМУ РЕЗУЛЬТАТУ ДОБАВЛЯЕМ этот айдишник
                    result_select = []
                    if len(result_where_Serial) > 0:
                        for x in range(len(result_where_Serial)):
                            result_select_dict = result_where_Serial[x]
                            result_select_dict.update(idx_list[i])
                            result_select.append(result_select_dict)

                        # ЕСЛИ У НАС ПУСТОТА , ТО ДОБАВЛЯЕМ ПУСТОТУ
                    else:
                        result_select_dict = idx_list[i]
                        result_select_dict['measure'] = str(self.__measure)
                        result_select_dict['vals'] = None
                        result_select.append(result_select_dict)
                    result = result + result_select

        return result

    # -----------------------------------------------------------------------------------------------------------------
    # Обработчик множенственного селекта для нескольких таблиц  с представлениями
    def __select_get_table_with_view(self, table, create_view, delete_view):

        # Первое - собираем нужные переменные
        self.__get_parse_answer()

        # Проверяем наличие тэга селектим все
        result = []
        if self.allMeters:

            # Версия исправленная, правильная

            # Сначала выгребаем из MeterTable все возможные записи
            command_select = 'SELECT MeterTable.DeviceIdx AS deviceIdx , MeterTable.MeterId AS meter  FROM MeterTable '
            result_select_of_MeterTable = sqlite.execute_command_to_read_return_dict(command=command_select)

            # После чего ПО ЭЛЕМЕНТНО СЕЛЕКТИМ по каждому айдишнику их связь в таблице METERDATA
            for i in range(len(result_select_of_MeterTable)):

                # Создаем Временное Представление, для удобности селекта

                # Добавляем Нужное время и точ то есть в таблциееее!!!
                if len(self.column) > 0:
                    command_select = 'SELECT MeterData.Timestamp AS ts , ArchTypes.Name AS measure , ' + str(
                        self.column) + ' FROM ' + table + \
                                     " AND ArchTypes.Name = \'" + str(self.__measure) + "\'" + \
                                     ' AND MeterData.DeviceIdx IN ( ' + str(
                        result_select_of_MeterTable[i]['deviceIdx']) + ' )  ' + \
                                     str(self.where_Timestamp)
                else:
                    command_select = 'SELECT MeterData.Timestamp AS ts , ArchTypes.Name AS measure ' + \
                                     ' FROM ' + table + \
                                     " AND ArchTypes.Name = \'" + str(self.__measure) + "\'" + \
                                     ' AND MeterData.DeviceIdx IN ( ' + str(
                        result_select_of_MeterTable[i]['deviceIdx']) + ' )  ' + \
                                     str(self.where_Timestamp)

                # Отправляем это все в космос
                result_select_of_MeterData = sqlite.execute_selected_to_view_return_dict(
                    command_create_view=create_view,
                    command_delete_view=delete_view,
                    command_select=command_select)

                # После чего КАЖДОМУ РЕЗУЛЬТАТУ ДОБАВЛЯЕМ этот айдишник
                result_select = []
                if len(result_select_of_MeterData) > 0:
                    for x in range(len(result_select_of_MeterData)):
                        result_select_dict = result_select_of_MeterData[x]
                        result_select_dict.update(result_select_of_MeterTable[i])
                        result_select.append(result_select_dict)

                # ЕСЛИ У НАС ПУСТОТА , ТО ДОБАВЛЯЕМ ПУСТОТУ
                else:
                    result_select_dict = result_select_of_MeterTable[i]
                    result_select_dict['measure'] = str(self.__measure)
                    result_select_dict['vals'] = None
                    result_select.append(result_select_of_MeterTable[i])

                result = result + result_select

        else:
            command_select_list_full = []

            if self.where_DeviceIdx is not None:

                # Если не пустота , то селектим по внутренему айдишнику
                idx = self.where_DeviceIdx
                # Сначала выгребаем Айдишники
                command_select = 'SELECT MeterTable.DeviceIdx AS deviceIdx FROM MeterTable ' + \
                                 ' WHERE MeterTable.DeviceIdx IN (' + str(idx)[1:-1] + ' ) '
                result_select_of_MeterTable_where_DeviceIdx = sqlite.execute_command_to_read_return_dict(
                    command=command_select
                )

                # После чего для каждого выбранного айдишника формируем нужные вариации команды
                for i in range(len(result_select_of_MeterTable_where_DeviceIdx)):

                    if len(self.column) > 0:
                        command = 'SELECT  ' + str(self.column) + \
                                  ' , MeterData.Timestamp AS ts , ArchTypes.Name AS measure FROM ' + \
                                  table + " AND ArchTypes.Name = \'" + str(
                            self.__measure) + "\'" + ' AND MeterData.DeviceIdx IN (' + \
                                  str(result_select_of_MeterTable_where_DeviceIdx[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)
                    else:
                        command = 'SELECT  ' + \
                                  '  MeterData.Timestamp AS ts , ArchTypes.Name AS measure FROM ' + \
                                  table + " AND ArchTypes.Name = \'" + str(self.__measure) + \
                                  "\'" + ' AND MeterData.DeviceIdx IN (' + \
                                  str(result_select_of_MeterTable_where_DeviceIdx[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)

                    # Опускаем это  в функцию обработчик

                    result_where_DeviceIdx = sqlite.execute_selected_to_view_return_dict(
                        command_create_view=create_view,
                        command_delete_view=delete_view,
                        command_select=command
                    )
                    # После чего КАЖДОМУ РЕЗУЛЬТАТУ ДОБАВЛЯЕМ этот айдишник
                    result_select = []
                    if len(result_where_DeviceIdx) > 0:
                        for x in range(len(result_where_DeviceIdx)):
                            result_select_dict = result_where_DeviceIdx[x]
                            result_select_dict.update(result_select_of_MeterTable_where_DeviceIdx[i])
                            result_select.append(result_select_dict)

                        # ЕСЛИ У НАС ПУСТОТА , ТО ДОБАВЛЯЕМ ПУСТОТУ
                    else:
                        result_select_dict = result_select_of_MeterTable_where_DeviceIdx[i]
                        result_select_dict['measure'] = str(self.__measure)
                        result_select_dict['vals'] = None
                        result_select.append(result_select_of_MeterTable_where_DeviceIdx[i])
                    # Добавляем Полученный Результат
                    result = result + result_select

            if self.where_MeterId is not None:

                # Если не пустота , то селектим по внутренему айдишнику
                idx = self.where_MeterId
                # Сначала выгребаем Айдишники
                command_select = 'SELECT' + \
                                 ' MeterTable.MeterId AS meter , MeterTable.DeviceIdx AS deviceIdx FROM MeterTable ' + \
                                 ' WHERE MeterTable.MeterId IN (' + str(idx)[1:-1] + ' ) '
                result_select_of_MeterTable_where_MeterId = sqlite.execute_command_to_read_return_dict(
                    command=command_select
                )
                # После чего для каждого выбранного айдишника формируем нужные вариации команды
                for i in range(len(result_select_of_MeterTable_where_MeterId)):

                    if len(self.column) > 0:
                        command = 'SELECT  ' + str(self.column) + \
                                  ' , MeterData.Timestamp AS ts , ArchTypes.Name AS measure FROM ' + \
                                  table + " AND ArchTypes.Name = \'" + str(
                            self.__measure) + "\'" + ' AND MeterData.DeviceIdx IN (' + \
                                  str(result_select_of_MeterTable_where_MeterId[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)
                    else:
                        command = 'SELECT  ' + ' MeterData.Timestamp AS ts , ArchTypes.Name AS measure FROM ' + \
                                  table + " AND ArchTypes.Name = \'" + str(self.__measure) + \
                                  "\'" + ' AND MeterData.DeviceIdx IN (' + \
                                  str(result_select_of_MeterTable_where_MeterId[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)

                    # Опускаем это  в функцию обработчик
                    result_where_DeviceIdx = sqlite.execute_selected_to_view_return_dict(
                        command_create_view=create_view,
                        command_delete_view=delete_view,
                        command_select=command
                    )

                    # После чего КАЖДОМУ РЕЗУЛЬТАТУ ДОБАВЛЯЕМ этот айдишник
                    result_select = []
                    if len(result_where_DeviceIdx) > 0:
                        for x in range(len(result_where_DeviceIdx)):
                            result_select_dict = result_where_DeviceIdx[x]
                            result_select_dict.update(result_select_of_MeterTable_where_MeterId[i])
                            result_select.append(result_select_dict)

                        # ЕСЛИ У НАС ПУСТОТА , ТО ДОБАВЛЯЕМ ПУСТОТУ
                    else:
                        result_select_dict = result_select_of_MeterTable_where_MeterId[i]
                        result_select_dict['measure'] = str(self.__measure)
                        result_select_dict['vals'] = None
                        result_select.append(result_select_of_MeterTable_where_MeterId[i])
                    # Добавляем Полученный Результат

                    result = result + result_select

            # # Теперь предстоит совсем жаришка - селект по cерийнику.
            if self.where_Serial is not None:
                # Берем серийник
                idx = self.where_Serial
                # Здесь берем серийник из ElectricConfig

                table_config = ' ElectricConfig  '

                # # Сначала выгребаем Айдишники по серийнику
                idx_list = []
                for i in range(len(idx)):
                    command_select = 'SELECT ' + ' Serial as serials , ' + \
                                     ' DeviceIdx AS  deviceIdx FROM  ' + table_config + \
                                     ' WHERE ' + ' Serial LIKE  \'%' + str(idx[i]) + '%\''

                    result_select_of_MeterTable_where_Serial = sqlite.execute_command_to_read_return_dict(
                        command=command_select
                    )
                    idx_list = idx_list + result_select_of_MeterTable_where_Serial

                # После чего для каждого выбранного айдишника формируем нужные вариации команды
                for i in range(len(idx_list)):

                    if len(self.column) > 0:
                        command = 'SELECT  ' + str(self.column) + \
                                  ' , MeterData.Timestamp AS ts , ArchTypes.Name AS measure FROM ' + \
                                  table + " AND ArchTypes.Name = \'" + str(
                            self.__measure) + "\'" + ' AND MeterData.DeviceIdx IN ( ' + \
                                  str(idx_list[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)
                    else:
                        command = 'SELECT  ' + \
                                  '  MeterData.Timestamp AS ts , ArchTypes.Name AS measure FROM ' + \
                                  table + " AND ArchTypes.Name = \'" + str(
                            self.__measure) + "\'" + ' AND MeterData.DeviceIdx IN ( ' + \
                                  str(idx_list[i]['deviceIdx']) + ' )   ' + \
                                  str(self.where_Timestamp)

                    # Опускаем это  в функцию обработчик
                    result_where_Serial = sqlite.execute_selected_to_view_return_dict(
                        command_create_view=create_view,
                        command_delete_view=delete_view,
                        command_select=command
                    )

                    # После чего КАЖДОМУ РЕЗУЛЬТАТУ ДОБАВЛЯЕМ этот айдишник
                    result_select = []
                    if len(result_where_Serial) > 0:
                        for x in range(len(result_where_Serial)):
                            result_select_dict = result_where_Serial[x]
                            result_select_dict.update(idx_list[i])
                            result_select.append(result_select_dict)

                        # ЕСЛИ У НАС ПУСТОТА , ТО ДОБАВЛЯЕМ ПУСТОТУ
                    else:
                        result_select_dict = idx_list[i]
                        result_select_dict['measure'] = str(self.__measure)
                        result_select_dict['vals'] = None
                        result_select.append(result_select_dict)
                    result = result + result_select

        return result

    # -----------------------------------------------------------------------------------------------------------------
    # ----------------------------------------Обработчики флагов-------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # Правило второе - Обработчик селекта по ид
    def __get_define_allMeters(self):
        try:
            # Если у нас есть это поле то соответственно ничего не возвращает
            if "allMeters" in self.JSON["flags"]:
                allMeters_flags = True
            else:
                allMeters_flags = False
        except:
            # если вылетает это поле - то можно спокойно селектить по айдишникам
            allMeters_flags = False
        finally:
            return allMeters_flags

        # Правило третье - обработчик флага по времени

    def __get_define_lastTime(self):
        try:
            # Если у нас есть это поле то соответственно ничего не возвращает
            if "lastTime" in self.JSON["flags"]:
                lastTime = True
            else:
                lastTime = False

        except:
            # если вылетает это поле - то можно спокойно селектить по айдишникам
            lastTime = False
        finally:
            return lastTime

    # --------------------------------------------Сборщики селектов разных айдишников----------------------------------
    # Делаем селект по внутренему ид
    def __get_command_select_DeviceIdx(self):
        try:
            # devices_list = self.JSON["devices"]
            sql_command = self.JSON["devices"]
            # sql_command = " AND DeviceIdx in  " + " ( " + str(devices_list)[1:-1] + ' ) '
        except:
            sql_command = None
        finally:
            return sql_command

    # Делаем селект по внешнему ид
    def __get_command_select_MeterId(self):
        try:
            # devices_list = self.JSON["ids"]
            sql_command = self.JSON["ids"]
            # sql_command = " AND MeterId in  " + " ( " + str(devices_list)[1:-1] + ' ) '
        except:
            sql_command = None
        finally:
            return sql_command

    # Делаем селект по серийному номеру
    def __get_command_select_Serial(self):
        try:
            # devices_list = self.JSON["serials"]
            sql_command = self.JSON["serials"]
            # sql_command = " AND Serial in  " + " (" + str(devices_list)[1:-1] + ') '
        except:
            sql_command = None
        finally:
            return sql_command

    # -------------------------------------------------------------------------------------------------
    # ----------------------------------Сборщик селектов по времени -----------------------------------
    def __get_command_select_Timestamp(self):
        # А здесь надо быть аккуратнее , так как поле может быть пустым
        if (self.__measure in Template_list_ArchTypes.ElectricConfig_ArchType_name_list) or \
                (self.__measure in Template_list_ArchTypes.DigitalConfig_ArchType_name_list) or \
                (self.__measure in Template_list_ArchTypes.PulseConfig_ArchType_name_list):
            MeterData = ''
        else:
            MeterData = ' MeterData.'

        try:
            Timestamp_list = self.JSON["time"]
            if len(Timestamp_list) > 0:
                sql_command = ''

                for i in range(len(Timestamp_list)):
                    sql_command_now = ' ( ' + MeterData + 'Timestamp >= ' + str(
                        Timestamp_list[i]["start"]) + "  AND " + MeterData + "Timestamp <= " + str(
                        Timestamp_list[i]["end"]) + "  ) "
                    sql_command = sql_command_now + ' OR ' + sql_command

                sql_command = sql_command[:-3]
                sql_command = ' ( ' + sql_command + ' ) '

                # И добавляем в начало И

                sql_command = ' AND ' + sql_command

            else:
                sql_command = ''

        except:
            sql_command = None

        finally:
            return sql_command

    # -------------------------------------------------------------------------------------------------
    # ----------------------------------Сборщик тэгов--------------------------------------------------

    def __get_command_select_tag(self):
        try:
            sql_command = ''
            requested_tags = self.JSON["tags"]
            # Если у нас там что то есть , то тогда селектим по тэгам
            if len(requested_tags) > 0:
                for i in range(len(requested_tags)):
                    # Сначала проверяем каждый тэг на пренадлежность к этой таблице
                    if requested_tags[i] in self.__all_tag:
                        # Добавляем эту команду в селект
                        sql_command_tag = self.dict_tag[requested_tags[i]] + ' , '
                        sql_command = sql_command + sql_command_tag
                    # Если тэгов нет , тогда оставляем пустым
                # После делаем обрезание последней запятой
                sql_command = sql_command[:-2]
            else:
                # Если у нас длины нет, значит массив пустой , и селектим все что есть. Ух
                sql_command = ''
                for key in self.dict_tag:
                    sql_command = sql_command + self.dict_tag[key] + ' , '
                    # Обрезаем последнюю запятую
                sql_command = str(sql_command)[:-2]

        except:
            sql_command = None
        finally:
            return sql_command


# -------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# -----------------КЛАСС КОТОРЫЙ ОСУЩЕСТВЛЯЕТ ЗАПИСЬ ВСЕХ ЗНАЧЕНИЙ В НУЖНУЮ ТАБЛИЦУ-------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class RecordDataToDB:
    """
    Данный клас преднозначен только для записи каких либо значений в БД в формате ДЕКОНСТРУИРОВАННОГО JSON

    Обычный JSON он не поддерживает. Это важно.


    """
    JSON_data = None
    error = []

    def __init__(self, data: list):
        self.error = []
        # Пускай будет все же принимать данные в листах , в которых есть словари
        self.JSON_data = data
        self.__recording_data_to_element_measure(data)

    # Проходимся по всем элементам массива!!
    def __recording_data_to_element_measure(self, data):

        for i in range(len(data)):

            result = self.__definition_table(data=data[i])
            # Включаем обработчик ошибок
            if len(result) > 0:
                self.error.append({"error": 'Ошибка при записи в БД'})

    # Определитель таблицы с которой будем взаимодействовать
    def __definition_table(self, data):

        # определяем таблицу по первому элементу
        measure = data[0]['Name']
        self.measure = measure
        # ElectricConfig
        if measure in ElectricConfig_ArchType_name_list:
            sql_command_to_table = Template_SQL_request.ElectricConfig_insert

            return self.__insert_config(command_insert=sql_command_to_table,
                                        devices_list=data,
                                        keys_list=Template_list_ArchTypes.ElectricConfig_tag)

        # DigitalConfig
        elif measure in DigitalConfig_ArchType_name_list:
            sql_command_to_table = Template_SQL_request.DigitalConfig_insert

            return self.__insert_config(command_insert=sql_command_to_table,
                                        devices_list=data,
                                        keys_list=Template_list_ArchTypes.DigitalConfig_tag)

        # PulseConfig
        elif measure in PulseConfig_ArchType_name_list:
            sql_command_to_table = Template_SQL_request.PulseConfig_insert

            return self.__insert_config(command_insert=sql_command_to_table,
                                        devices_list=data,
                                        keys_list=Template_list_ArchTypes.PulseConfig_tag)


        # ElecticEnergyValues
        elif measure in ElecticEnergyValues_ArchType_name_list:
            # здесь аккуратнее -
            sql_command_to_table = Template_SQL_request.ElectricEnergyValues_insert
            return self.__insert_ElecticEnergyValues(command_insert=sql_command_to_table,
                                                     devices_list=data)

        # ElectricQualityValues
        elif measure in ElectricQualityValues_ArchType_name_list:
            # здесь аккуратнее -
            sql_command_to_table = Template_SQL_request.ElectricQualityValues_insert
            return self.__insert_ElectricQualityValues(command_insert=sql_command_to_table,
                                                       devices_list=data)


        # ElectricPowerValues
        elif measure in ElectricPowerValues_ArchType_name_list:
            sql_command_to_table = Template_SQL_request.ElectricPowerValues_insert
            return self.__insert_together_with_meter_data(command_insert=sql_command_to_table,
                                                          devices_list=data,
                                                          keys_list=Template_list_ArchTypes.ElectricPowerValues_tag)


        # PulseValues
        elif measure in PulseValues_ArchType_name_list:
            sql_command_to_table = Template_SQL_request.PulseValues_insert
            return self.__insert_digital_and_pulse_values(command_insert=sql_command_to_table,
                                                          devices_list=data,
                                                          keys_list=Template_list_ArchTypes.PulseValues_tag)

        # DigitalValues
        elif measure in DigitalValues_ArchType_name_list:
            sql_command_to_table = Template_SQL_request.DigitalValues_insert
            return self.__insert_digital_and_pulse_values(command_insert=sql_command_to_table,
                                                          devices_list=data,
                                                          keys_list=Template_list_ArchTypes.DigitalValues_tag)



        # JournalValues
        elif measure in JournalValues_ArchType_name_list:
            sql_command_to_table = Template_SQL_request.JournalValues_insert
            return self.__insert_together_with_meter_data(command_insert=sql_command_to_table,
                                                          devices_list=data,
                                                          keys_list=Template_list_ArchTypes.JournalValues_tag)



        else:
            result_select = [None]

    # ----------------------------------------------------------------------------------------------------------------------
    # Функции Которые записывают в нужную таблицу данные:
    # ----------------------------------------------------------------------------------------------------------------------

    def __insert_config(self, command_insert: str, devices_list: list, keys_list: list):

        """
        Функция для записи конфигов

        :param command_insert:
        :param devices_list:
        :param keys_list:
        :return:
        """
        # Итак - для начала  собираем значения для команд начиная с айдишника
        keys_list_full = ['id', 'ts'] + keys_list
        data_insert_full = ''
        for i in range(len(devices_list)):
            data_insert_element = []
            for x in range(len(keys_list_full)):
                data_insert_element.append(devices_list[i][keys_list_full[x]])
            data_insert_full = data_insert_full + str((tuple(data_insert_element))) + ','
        # После того как сформировали команду - отправляем ее в космос
        # ормируем команду
        command_insert_full = command_insert + str(data_insert_full)
        # Обрезаем последнюю запятую
        command_insert_full = command_insert_full[:-1]
        # отправляем в космос

        result = sqlite.execute_command_to_write_return_dict(command_insert_full)
        return result

    def __find_RecordTypeId(self):
        measure = str(self.measure)

        RecordTypeId = sqlite.execute_command_to_read_return_dict(
            'SELECT Id FROM ArchTypes WHERE Name =  ' + "\'" + measure + "\' ")
        return RecordTypeId[0]['Id']

    # Это функция инсерта вместе с метор дата
    def __insert_together_with_meter_data(self, command_insert: str, devices_list: list, keys_list: list):
        """
        Функция для записи вместе с meterdata , если нет полей кроме тех что есть в JSON

        :param command_insert:
        :param devices_list:
        :param keys_list:
        :return:
        """
        # Что по итогу делаем:
        # Записываем все необходимое в meterdata, Получая их id

        MeterData_ids = self.__insert_meterdata(devices_list=devices_list)

        # Формируем инсерт для таблицы
        keys_list_full = keys_list
        for i in range(len(devices_list)):
            data_insert_element = []
            # Селектим нужный нам рекорд тайп айди
            RecordTypeId = self.__find_RecordTypeId()
            # селектим нужный нам ID

            command_select_ids = 'SELECT Id FROM MeterData WHERE DeviceIdx = ' + str(
                devices_list[i]['id']) + " AND Timestamp = " + str(
                devices_list[i]['ts']) + " AND RecordTypeId = " + str(
                RecordTypeId)
            selection_id = sqlite.execute_command_to_read_return_dict(command_select_ids)
            # И добавляем его в список
            data_insert_element.append(selection_id[0]['Id'])
            # После этого проходимся по всем ключам и добавляим их в список тех что есть
            for x in range(len(keys_list_full)):
                data_insert_element.append(devices_list[i][keys_list_full[x]])
            # на выходе имеем массив , и его должнв записать . дап.

            result = sqlite.execute_command_values_to_write_return_dict(values=tuple(data_insert_element),
                                                                        command=command_insert)

        return result

    # Функция инсерта в метер дата
    def __insert_meterdata(self, devices_list: list):
        """
        Данная функция является вспомогательной и записывает нужную часть данных в MeterData

        :param devices_list:
        :return:
        """
        # Собираем команду :
        Command = 'INSERT INTO  MeterData (DeviceIdx, Timestamp,Valid, RecordTypeId ) VALUES '

        data_insert_full = ' '
        ids = []

        for device_element in devices_list:
            data_insert_element = []
            data_insert_element.append(device_element['id'])
            ids.append(device_element['id'])
            data_insert_element.append(device_element['ts'])

            # Добавляем Valid
            data_insert_element.append(1)
            # Добавляем RecordTypeId

            Command_RecordType = 'SELECT Id FROM ArchTypes WHERE Name = ' + '\'' + device_element['Name'] + '\''
            result_select_RecordTypeId = sqlite.execute_command_to_read_return_dict(Command_RecordType)

            RecordTypeId = result_select_RecordTypeId[0]['Id']
            data_insert_element.append(RecordTypeId)

            data_insert_full = data_insert_full + str((tuple(data_insert_element))) + ','

        # После того как сформировали команду - отправляем ее в космос
        # ормируем команду
        command_insert_full = Command + str(data_insert_full)
        # Обрезаем последнюю запятую
        command_insert_full = command_insert_full[:-1]

        # Теперь все это отправляем в БД
        result = sqlite.execute_command_to_write_return_dict(command_insert_full)

        # Далее мы селектим нужные нам ID
        # command_select_ids = 'SELECT Id ,DeviceIdx,Timestamp  FROM MeterData WHERE DeviceIdx IN' + str(tuple(ids))

        # return sqlite.execute_command_to_read_return_dict(command_select_ids)

        command_select_ids = 'SELECT Id ,DeviceIdx,Timestamp  FROM MeterData WHERE DeviceIdx IN (' + (len(
            tuple(ids)) * ', ? ')[1:] + ')'

        return sqlite.execute_command_values_to_write_return_dict(command=command_select_ids, values=tuple(ids))

    # ----------------------------------------------------------------------------------------------------------------------
    # Insert ElecticEnergyValues
    # ----------------------------------------------------------------------------------------------------------------------
    #     Здесь универсально никак , поэтому сделаем частный случай
    def __insert_ElecticEnergyValues(self, command_insert: str, devices_list: list):

        # Сначала записываем все значения в метер дата
        # Записываем все необходимое в meterdata, Получая их id
        MeterData_ids = self.__insert_meterdata(devices_list=devices_list)

        # Формируем инсерт для таблицы

        data_insert_full = ''

        # Проходимся по каждому из элементов :
        for i in range(len(devices_list)):
            data_insert_element_tariff0 = []
            data_insert_element_tariff1 = []
            data_insert_element_tariff2 = []
            data_insert_element_tariff3 = []
            data_insert_element_tariff4 = []

            # Селектим нужный нам рекорд тайп айди
            RecordTypeId = self.__find_RecordTypeId()

            # селектим нужный нам ID
            command_select_ids = 'SELECT Id FROM MeterData WHERE DeviceIdx = ' + str(
                devices_list[i]['id']) + " AND Timestamp = " + str(
                devices_list[i]['ts']) + " AND RecordTypeId = " + str(
                RecordTypeId)
            selection_id = sqlite.execute_command_to_read_return_dict(command_select_ids)
            value_id = selection_id[0]['Id']
            # Добавляем нужные тэги теперь
            #     id
            data_insert_element_tariff0.append(value_id)
            data_insert_element_tariff1.append(value_id)
            data_insert_element_tariff2.append(value_id)
            data_insert_element_tariff3.append(value_id)
            data_insert_element_tariff4.append(value_id)

            # tariff
            data_insert_element_tariff0.append(0)
            data_insert_element_tariff1.append(1)
            data_insert_element_tariff2.append(2)
            data_insert_element_tariff3.append(3)
            data_insert_element_tariff4.append(4)

            # A+
            data_insert_element_tariff0.append(devices_list[i]['A+0'])
            data_insert_element_tariff1.append(devices_list[i]['A+1'])
            data_insert_element_tariff2.append(devices_list[i]['A+2'])
            data_insert_element_tariff3.append(devices_list[i]['A+3'])
            data_insert_element_tariff4.append(devices_list[i]['A+4'])
            # R+
            data_insert_element_tariff0.append(devices_list[i]['R+0'])
            data_insert_element_tariff1.append(devices_list[i]['R+1'])
            data_insert_element_tariff2.append(devices_list[i]['R+2'])
            data_insert_element_tariff3.append(devices_list[i]['R+3'])
            data_insert_element_tariff4.append(devices_list[i]['R+4'])
            # A-
            data_insert_element_tariff0.append(devices_list[i]['A-0'])
            data_insert_element_tariff1.append(devices_list[i]['A-1'])
            data_insert_element_tariff2.append(devices_list[i]['A-2'])
            data_insert_element_tariff3.append(devices_list[i]['A-3'])
            data_insert_element_tariff4.append(devices_list[i]['A-4'])
            # R-
            data_insert_element_tariff0.append(devices_list[i]['R-0'])
            data_insert_element_tariff1.append(devices_list[i]['R-1'])
            data_insert_element_tariff2.append(devices_list[i]['R-2'])
            data_insert_element_tariff3.append(devices_list[i]['R-3'])
            data_insert_element_tariff4.append(devices_list[i]['R-4'])

            data_insert_full = data_insert_full + str((tuple(data_insert_element_tariff0))) + ',' + str(
                tuple(data_insert_element_tariff1)) + ',' + str((tuple(data_insert_element_tariff2))) + ',' + str(
                (tuple(data_insert_element_tariff3))) + ',' + str((tuple(data_insert_element_tariff4))) + ','
            # После того как сформировали команду - отправляем ее в космос
            # ормируем команду
        command_insert_full = command_insert + str(data_insert_full)
        # Обрезаем последнюю запятую
        command_insert_full = command_insert_full[:-1]
        # отправляем в космос

        result = sqlite.execute_command_to_write_return_dict(command_insert_full)
        return result

    # ----------------------------------------------------------------------------------------------------------------------
    # Insert    ElectricQualityValues
    # ----------------------------------------------------------------------------------------------------------------------

    #     Здесь универсально никак , поэтому сделаем здесь тоооже частный случай
    def __insert_ElectricQualityValues(self, command_insert: str, devices_list: list):
        # Сначала записываем все значения в метер дата
        # Записываем все необходимое в meterdata, Получая их id
        MeterData_ids = self.__insert_meterdata(devices_list=devices_list)

        # Формируем инсерт для таблицы

        data_insert_full = ''
        command_insert_full_list = []
        # Проходимся по каждому из элементов :
        for i in range(len(devices_list)):
            data_insert_element_phase_A = []
            data_insert_element_phase_B = []
            data_insert_element_phase_C = []
            data_insert_element_phase_SUMM = []

            # Селектим нужный нам рекорд тайп айди
            RecordTypeId = self.__find_RecordTypeId()

            # селектим нужный нам ID
            command_select_ids = 'SELECT Id FROM MeterData WHERE DeviceIdx = ' + str(
                devices_list[i]['id']) + " AND Timestamp = " + str(
                devices_list[i]['ts']) + " AND RecordTypeId = " + str(
                RecordTypeId)
            selection_id = sqlite.execute_command_to_read_return_dict(command_select_ids)
            value_id = selection_id[0]['Id']
            # Добавляем нужные тэги теперь
            #     id
            data_insert_element_phase_A.append(value_id)
            data_insert_element_phase_B.append(value_id)
            data_insert_element_phase_C.append(value_id)
            data_insert_element_phase_SUMM.append(value_id)

            # PHASE
            data_insert_element_phase_A.append('A')
            data_insert_element_phase_B.append('B')
            data_insert_element_phase_C.append('C')
            data_insert_element_phase_SUMM.append('Summ')

            # U
            data_insert_element_phase_A.append(devices_list[i]['UA'])
            data_insert_element_phase_B.append(devices_list[i]['UB'])
            data_insert_element_phase_C.append(devices_list[i]['UC'])
            data_insert_element_phase_SUMM.append(None)

            # I
            data_insert_element_phase_A.append(devices_list[i]['IA'])
            data_insert_element_phase_B.append(devices_list[i]['IB'])
            data_insert_element_phase_C.append(devices_list[i]['IC'])
            data_insert_element_phase_SUMM.append(None)

            # P
            data_insert_element_phase_A.append(devices_list[i]['PA'])
            data_insert_element_phase_B.append(devices_list[i]['PB'])
            data_insert_element_phase_C.append(devices_list[i]['PC'])
            data_insert_element_phase_SUMM.append(devices_list[i]['PS'])

            # Q
            data_insert_element_phase_A.append(devices_list[i]['QA'])
            data_insert_element_phase_B.append(devices_list[i]['QB'])
            data_insert_element_phase_C.append(devices_list[i]['QC'])
            data_insert_element_phase_SUMM.append(devices_list[i]['QS'])

            # S
            data_insert_element_phase_A.append(devices_list[i]['SA'])
            data_insert_element_phase_B.append(devices_list[i]['SB'])
            data_insert_element_phase_C.append(devices_list[i]['SC'])
            data_insert_element_phase_SUMM.append(devices_list[i]['SS'])

            # KP
            data_insert_element_phase_A.append(devices_list[i]['kPA'])
            data_insert_element_phase_B.append(devices_list[i]['kPB'])
            data_insert_element_phase_C.append(devices_list[i]['kPC'])
            data_insert_element_phase_SUMM.append(devices_list[i]['kPS'])

            # Angle
            data_insert_element_phase_A.append(devices_list[i]['AngAB'])
            data_insert_element_phase_B.append(devices_list[i]['AngBC'])
            data_insert_element_phase_C.append(devices_list[i]['AngAC'])
            data_insert_element_phase_SUMM.append(None)

            # F
            data_insert_element_phase_A.append(None)
            data_insert_element_phase_B.append(None)
            data_insert_element_phase_C.append(None)
            data_insert_element_phase_SUMM.append(devices_list[i]['Freq'])

            # Вариант 2
            # Все выше указанное добавляем в обработчик команд
            result = sqlite.execute_command_values_to_write_return_dict(values=tuple(data_insert_element_phase_A),
                                                                        command=command_insert)
            result = sqlite.execute_command_values_to_write_return_dict(values=tuple(data_insert_element_phase_B),
                                                                        command=command_insert)
            result = sqlite.execute_command_values_to_write_return_dict(values=tuple(data_insert_element_phase_C),
                                                                        command=command_insert)
            result = sqlite.execute_command_values_to_write_return_dict(values=tuple(data_insert_element_phase_SUMM),
                                                                        command=command_insert)

        return result

    # ---------------------------------------------------------------------------------------------------------------
    # Insert    PulseValues and DigitalValues
    # ---------------------------------------------------------------------------------------------------------------

    # общая функция для общего инсерта для таблиц PulseValues и DigitalValues
    def __insert_digital_and_pulse_values(self, command_insert: str, devices_list: list, keys_list: list):
        # Сначала записываем все значения в метер дата
        # Записываем все необходимое в meterdata, Получая их id
        MeterData_ids = self.__insert_meterdata(devices_list=devices_list)

        # Формируем инсерт для таблицы

        data_insert_full = ''
        command_insert_full_list = []

        # Для начала формируем два листа ю Один с айдишкником и чанелс, другой только с теми тэгами что есть в JSON
        # Сначала формируем лист из тэгов джейсона
        # Проходимся по каждому из элементов:

        for i in range(len(devices_list)):
            data_insert = []
            # После этого проходимся по всем ключам и добавляим их в список тех что есть
            for x in range(len(keys_list)):
                data_insert.append(devices_list[i][keys_list[x]])
            # на выходе имеем массив  которому надо добавить chanls

            data_insert_element = []

            # Селектим нужный нам рекорд тайп айди
            RecordTypeId = self.__find_RecordTypeId()

            # селектим нужный нам ID
            command_select_ids = 'SELECT Id FROM MeterData WHERE DeviceIdx = ' + str(
                devices_list[i]['id']) + " AND Timestamp = " + str(
                devices_list[i]['ts']) + " AND RecordTypeId = " + str(
                RecordTypeId)
            selection_id = sqlite.execute_command_to_read_return_dict(command_select_ids)
            # И добавляем его в список
            data_insert_element.append(selection_id[0]['Id'])
            # После этого получаем чанлс
            data_insert_element.append(len(data_insert))
            # соедленяем
            command_insert_full_list = data_insert_element + data_insert

            # Записываем
            result = sqlite.execute_command_values_to_write_return_dict(values=tuple(command_insert_full_list),
                                                                        command=command_insert)
        return result


class SelectToMeterDataDataBase:
    JSON_measure = {}
    Select_all = None
    result = [None]
    Arch_Type_Id = 0

    def __init__(self, JSON_measure, select_all):
        self.JSON_measure = JSON_measure
        # Итак - Первое что делаем - Определяем тип данных
        self.Arch_Type_Id = self.__define_arch_type_id()
        self.Select_all = select_all
        # Теперь селектим нужные нам вещи - ИЩЕМ МЕТЕР ДАТУ
        self.result = self.__define_MeterData()

    def __define_arch_type_id(self):

        command = 'SELECT Id , Name FROM ArchTypes WHERE Name == ' + '\'' + str(self.JSON_measure['measure']) + '\''
        Arch_Type_Id = sqlite.execute_command_to_read_return_dict(command)
        # Теперь очищаем от мусора - берем первый Элемент , и в нем айдишник
        Arch_Type_Id = Arch_Type_Id[0]['Id']

        return Arch_Type_Id

    def __define_MeterData(self):
        # ЕСЛИ СЕЛЕКТИМ ВСЕ :

        command = 'SELECT * FROM MeterData ' + ' WHERE ' + ' RecordTypeId = ' + str(self.Arch_Type_Id)

        # СЕЛЕКТИМ ТОЛЬКО ТЕ АЙДИШНИКИ ЧТО У НАС ЕСТЬ
        if not self.Select_all:
            IDx_list = []
            for i in range(len(self.JSON_measure["devices"])):
                IDx_list.append(deepcopy(self.JSON_measure["devices"][i]["id"]))

            idx = '( '
            for i in range(len(IDx_list)):
                idx = idx + ' ' + str(IDx_list[i]) + ' ,'
            idx = idx[:-1] + ' ) '
            # Добавляем наш айдишник
            command = command + ' AND ' + ' DeviceIdx in ' + idx

        result = sqlite.execute_command_to_read_return_dict(command)

        return result


class SelectToDataBase:
    JSON_measure = {}
    Select_all = None
    result = []

    def __init__(self, JSON_measure, select_all, Command_table_list):
        self.result = []
        # переопрелеляем
        self.JSON_measure = JSON_measure
        # Теперь селектим метер дату
        result = SelectToMeterDataDataBase(JSON_measure=JSON_measure, select_all=select_all).result

        for i in range(len(result)):
            # Проверяем поле валид

            Value = {'Name': self.JSON_measure['measure'],
                     'id': result[i]['DeviceIdx'],
                     'Valid': result[i]['Valid'],
                     'ts': result[i]['Timestamp']}
            # ЕСЛИ У НАС ВАЛИДНАЯ ЗАПИСЬ , ТО СЕЛЕКТИМ сопусттчвующие таблицы
            if result[i]['Valid'] == 1:
                # Теперь для каждой команды -
                for x in range(len(Command_table_list)):
                    command = Command_table_list[x] + ' AND Id = ' + str(result[i]['Id'])
                    select_result = sqlite.execute_command_to_read_return_dict(command)
                    if len(select_result) > 0:
                        Value.update(select_result[0])
            # Далее обновляем этим наш список селекта
            self.result.append(Value)
