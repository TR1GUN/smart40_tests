
from working_directory import sqlite
from working_directory.Template.Template_MeterTable_db_API.Template_generator_settings_MeterTable import \
    GeneratorForSettingsMeterTable

# --------------------------------------------------------------------------------------------------------------------
#                                 Генератор внутренего idx
# --------------------------------------------------------------------------------------------------------------------
# Отдельный класс генератор для внутренего idx
class GeneratorDeviceIdx:
    """
    Генератор внутренего idx
    """

    id = []

    def __init__(self, count_id):
        self.id = self.__generate_ids(count_id=count_id)

    # Ищем максимальное значение и возвращаем его
    def _find_max(self):
        # итак - сначала надо заселектить максимальные значения всех таблиц чтоб не пересекаться
        find_max = [self.__select_max(table_name='MeterData', collum='DeviceIdx'),
                    self.__select_max(table_name='ElectricConfig', collum='DeviceIdx'),
                    self.__select_max(table_name='DigitalConfig', collum='DeviceIdx'),
                    self.__select_max(table_name='PulseConfig', collum='DeviceIdx')]
        # а теперь получаем это максимальное значение
        max_value = max(find_max)
        # Находим максимальное значение и среди MeterTable , и возвращаем его
        max_value_final = self.__get_max_value(max_value_table=max_value)
        return max_value_final

    # вспомогательная функция для того чтоб узнать максимальное значение - если оно больше чем в MeterTable -
    # догенерируем нужное

    def __get_max_value(self, max_value_table):
        # Получаем максимальное значение из MeterTAble
        max_value_MeterTable = self.__select_max(table_name='MeterTable', collum='DeviceIdx')
        # Теперь сравниваем - Если значения в остальных больше , то генерируем что нужно в БД

        if max_value_table > max_value_MeterTable:
            count = max_value_table - max_value_MeterTable
            # Генерируем и записываем в БД
            generate = GeneratorForSettingsMeterTable(count)
            sqlite.recording_MeterTable(generate.get_tuple())
        # После чего берем МАКИМАЛЬНОЕ ЗНАЧЕНИЕ И ВОЗВРАЩАЕМ ЕГО
        max_value_MeterTable = self.__select_max(table_name='MeterTable', collum='DeviceIdx')
        return max_value_MeterTable

    # Сама команда к БД
    def __select_max(self, table_name: str, collum: str):

        collum_max = 'max(' + collum + ')'
        max_value = sqlite.readtable_return_dict(collum=collum_max, table_name=table_name)
        if len(max_value) > 0:
            max_value = max_value[0][collum_max]
        else:
            max_value = 0

        if max_value is None:
            max_value = 0
        return max_value

    def __generate_ids(self, count_id: int):
        # Теперь надо как то скооперироваться с MeterTable
        # Ищим максимальное значение
        max_value = self._find_max()

        #  генерируем значения в базу - settings и ids для JSON , settings для БД
        from working_directory.Template.Template_MeterJSON.Template_Record_MeterTable import GenerateRecordMeterTable

        generate = GenerateRecordMeterTable(generate_count=count_id,
                                            count_tree=0,
                                            type_connect= 'Iface1',
                                            address_meter="Adress be away",
                                            adress="o.o"
                                            ).DeviceIdx_list

        value_id_list = []
        # ДЕЛАЕМ ИЗ НИХ СПИСОК ТАК СЛОВНО ИХ МЫ ЗАСЕЛЕКТИЛИ , ЛОЛ
        for i in range(len(generate)):
            value_id_list.append({'DeviceIdx': generate[i]})
        return value_id_list

