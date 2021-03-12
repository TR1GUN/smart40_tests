from working_directory.Template.Template_Meter_db_data_API.Template_generator_measures_ts import GeneratorValsByDevices
from working_directory import sqlite
from working_directory.Template.Template_MeterTable_db_API.Template_generator_settings_MeterTable import GeneratorForSettingsMeterTable


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

    # вспомогательная функция для того чтоб узнать максимальное значение - если оно больше чем в MeterTable - догенерируем нужное
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
        generate = GeneratorForSettingsMeterTable(count_id)

        # Загружаем нужные нам ID
        sqlite.recording_MeterTable(generate.get_tuple())
        # А теперь получаем все полученные id
        command = 'MeterTable WHERE DeviceIdx > ' + str(max_value)
        value_id_list = sqlite.readtable_return_dict(collum='DeviceIdx', table_name=command)
        return value_id_list


# --------------------------------------------------------------------------------------------------------------------

class GeneratorIdDevices:
    devices = []
    deconstruct = []
    deconstruct_dict = []

    """
    Конструктор для генерации id в готовое json представление.
    """

    # Конструктор для генерации тэгов - очень важно - принимает строковые значения
    def __init__(self, generate_unicale_ts, generate_unicale_id, measure: str, count_ts: int = 3, count_id: int = 3, ):
        self.devices = []
        self.deconstruct = []
        self.deconstruct_dict = []

        self.devices = self.__generate_ids(
            # Число сколько генерируем айдишников
            count_id=count_id,
            # Тип переменной для которой генерируем
            measure=measure,
            # Количество таймстампов
            count_ts=count_ts,
            # Флаг уникальной генерации для айдишника или готовые айдишники
            generate_unicale_id=generate_unicale_id,
            # Флаг уникальной генерации для таймстампов или готовые таймстампы
            generate_unicale_ts=generate_unicale_ts)

    #     здесь пропишем генератор для айдишников - ОЧЕЕЕНЬ ВАЖНОЕ, ДА

    def __generate_ids(self, count_id: int, measure: str, count_ts: int, generate_unicale_id, generate_unicale_ts):

        # для начала мы должны определиться - мы генерируем уникальные id или используем уже сгенерированные
        # После чего Включачем наш генератор
        if type(generate_unicale_id) != bool:
            value_id_list = generate_unicale_id
        else:
            value_id_list = GeneratorDeviceIdx(count_id=count_id).id
        # Теперь это вставляем в генератор
        devices_ids_list = []
        self.deconstruct = []
        # Генерируем время

        # Теперь тут генируруем айдишники отталкиваясь от заданного максимального значения

        for i in range(count_id):
            devices = {}
            vals = GeneratorValsByDevices(measure=measure, count_ts=count_ts, generate_unicale=generate_unicale_ts)
            # Сюда пихаем ID
            devices['id'] = value_id_list[i]['DeviceIdx']

            # Сюда пихаем что написали для времени
            deconstruct_vals = vals.get_deconstruct()

            deconstruct = []
            deconstruct = self.__generate_deconstruct(list_vals=deconstruct_vals, ids=value_id_list[i]['DeviceIdx'])
            self.deconstruct = self.deconstruct + deconstruct

            devices['vals'] = vals.get_vals()
            devices_ids_list.append(devices)

            # А здесь работает каждый деконструктор  для БД
            # Тоже самое что и выше, только словарь
            deconstruct_dict = []
            deconstruct_dict = vals.get_deconstruct_dict()
            # после чего , к каждому элементу доабвляем нужные нам словари
            deconstruct_dict_append = []
            deconstruct_dict_append = self.__generate_deconstruct_dict(list_vals=deconstruct_dict,
                                                                       ids=value_id_list[i]['DeviceIdx'])

            self.deconstruct_dict = self.deconstruct_dict + deconstruct_dict_append
        return devices_ids_list

    def __generate_deconstruct_dict(self, list_vals: list, ids):
        list_vals_deconstruct = []
        for i in range(len(list_vals)):
            # Делаем новый словарь
            vals_dict = {}
            vals_dict['id'] = ids
            vals_dict.update(list_vals[i])
            list_vals_deconstruct.append(vals_dict)
        return list_vals_deconstruct

    def __generate_deconstruct(self, list_vals: list, ids):
        list_vals_deconstruct = []
        for i in range(len(list_vals)):
            deconstruct = [ids] + list_vals[i]
            list_vals_deconstruct.append(deconstruct)
        return list_vals_deconstruct

    def get_devices(self):
        return self.devices

    def get_devices_deconstruct(self):
        return self.deconstruct

    def get_devices_deconstruct_dict(self):
        return self.deconstruct_dict

