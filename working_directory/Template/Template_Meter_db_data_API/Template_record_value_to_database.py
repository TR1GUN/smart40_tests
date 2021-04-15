from working_directory.Template.Template_Meter_db_data_API.Template_read_handler_table import RecordDataToDB
from working_directory.Template.Template_Meter_db_data_API.Template_list_ArchTypes import \
    ElectricConfig_ArchType_name_list, \
    PulseConfig_ArchType_name_list, \
    DigitalConfig_ArchType_name_list , \
    ElectricQualityValues_ArchType_name_list
from copy import deepcopy


# //-------------------------------------------------------------------------------------------------------------------
#                                                   КЛАСС ЗАПИСИ
# //-------------------------------------------------------------------------------------------------------------------

class RecordValueToDataBase:
    """
    Данный класс предназначен для записи необходимых данных в нашу БД

    """

    JSON_deconstruct = []
    DeviceIdx_list = []

    def __init__(self, JSON_deconstruct: list):
        self.DeviceIdx_list = []
        self.JSON_deconstruct = []

        self.JSON_deconstruct = JSON_deconstruct
        # Определяем - есть ли значения для записи
        if len(self.JSON_deconstruct) > 0:
            # ЕСЛИ ДА , ТО ОПРЕДЕЛЯЕМ ЕСТЬ ЛИ КОНФИГ
            self.__define_config()
            # После чего ЗАПИСЫВАЕМ ПОУЛЧИВШИЙСЯ РЕЗУЛЬТАТ
            # print('----------------------------------------')
            # print('----------------ЗАПИСЬ------------------')
            # print(self.JSON_deconstruct)
            # print('----------------------------------------')
            RecordDataToDB(data=self.JSON_deconstruct)

    # Здесь определяем Есть ли у нас Конфиг , если нет - То добавляем
    def __define_config(self):
        """Здесь определяем Есть ли у нас Конфиг , если нет - То добавляем EL CONFIG """
        config = False

        # /////////////////////////////////////////////////////////////////////////////////////////////////////////
        #                     ОЧЕНЬ ВАЖНАЯ ХРЕНЬ - ПОКА ДОБАВЛЯЕТСЯ ТОЛЬКО ЭЛЕКТРОННЫЙ КОНФИГ
        # /////////////////////////////////////////////////////////////////////////////////////////////////////////
        config_list = ElectricConfig_ArchType_name_list + \
                        PulseConfig_ArchType_name_list + \
                        DigitalConfig_ArchType_name_list

        # config_list = ElectricConfig_ArchType_name_list
        # full_elconfig = Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list + \
        #                 Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list + \
        #                 Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list + \
        #                 Template_list_ArchTypes.JournalValues_ArchType_name_list

        # /////////////////////////////////////////////////////////////////////////////////////////////////////////

        for i in range(len(self.JSON_deconstruct)):
            # Если есть - То ставим в ТРУ

            if self.JSON_deconstruct[i][0]['Name'] in config_list:
                config = True
        # Если его не нашли - то добавляем
        if not config:
            # получаем наши айдишники
            for x in range(len(self.JSON_deconstruct[0])):
                self.DeviceIdx_list.append(self.JSON_deconstruct[0][x]['id'])
            # После чего получаем Конфиг
            # self.JSON_deconstruct = deepcopy(self.JSON_deconstruct)
            # Перезаписываем с конфигом
            self.JSON_deconstruct = self.JSON_deconstruct + self.__adding_config()

    def __adding_config(self):
        """Добавляем НАШ КОНФИГ"""
        # сналачала Генерируем его

        from working_directory.Template.Template_MeterJSON.Template_generate_meter_data_JSON import GeneratorJSON
        from working_directory.Template.Template_MeterJSON.Template_Deconstruct import DeconstructJSON
        # Генерируем наш Конфиг

        Generator = GeneratorJSON(measure=ElectricConfig_ArchType_name_list,
                                  count_ts=1,
                                  count_id=list(set(self.DeviceIdx_list)),
                                  Castrom_Value={'model': 'Автоматически добавленный конфиг'})
        # Получаем данные - голый скелет
        skeleton_JSON = Generator.JSON

        # И наш JSON
        self.JSON_dict = Generator.Generator_JSON_for_Meter_data_POST()

        # Теперь получаем деконструированный JSON
        JSON_deconstruct = DeconstructJSON(JSON=self.JSON_dict).JSON_deconstruct


        # JSON_Meter_Dev = GenerateDataForMeterDev(measure_list=ElectricConfig_ArchType_name_list).JSON_Meter_Dev
        #
        # JSON_dict_meterdata = AssemblyDictLikeMeterData(JSON_Meter_Dev, self.DeviceIdx_list).JSON
        #
        # JSON_for_compare_to_data_base = DecostructMeterDataJSONForDaemon(JSON=JSON_dict_meterdata).JSON_deconstruct

        return JSON_deconstruct

