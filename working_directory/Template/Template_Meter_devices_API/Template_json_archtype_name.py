# Здесь расположим класс сборщик шаблона JSON ответа которые основаны на archtype_name
from Emulator.Counters import Config_settings
from Emulator.ParserXML import ReadCounters
from working_directory.Template.Template_Meter_devices_API.Template_generate_meter_value import GeneratorMeterValue
from working_directory.Template.Template_Meter_devices_API.Template_list_job import GetSerial_list


class ArchTypesNameJSON:
    """
    Шаблон для генерации JSON ответа для типов данных из ArchTypesName
    """
    JSON = {}
    model = 'CE303'
    path = Config_settings.path
    Settings = None
    count_ts = None

    def __init__(self, measure: str, count_ts, Settings=None):
        # Переопределяем поля

        self.measure = measure
        self.count_ts = count_ts
        if Settings is None :
            # Парсим наш файл с настройками
            self.__parse_xml()

        # Собираем скелет json
        self.JSON = self.generator_JSON()

    def __parse_xml(self):
        """
        # Здесь парсим наш xml c настройками

        """

        # Получаем ПУТЬ
        xmlpath = self.path + '/' + self.model + '.xml'

        # Открываем
        self.Settings = ReadCounters(xmlpath=xmlpath)

    def generator_JSON(self):
        """
        Собираем финальный вид поля data JSON ответа
        :return:
        """
        JSON_Data = {
            "measures": self.__generate_measures()
        }

        return JSON_Data

    def __generate_measures(self):
        """
        Генерируем наш блок measures
        :return:
        """

        measure = self.measure
        json_measures = {"devices": self.__generate_devices(), "type": measure}
        return [json_measures]

    def __generate_devices(self):
        """
        Конструируем наш блок devices
        :return:
        """

        json_dict = \
            {
                # "model": self.Settings.name,
                "serial": self.Settings.snumber,
                "vals": self.__generate_vals()
            }

        # Пропишем условия генерации для параметра модели для команды получения серийника
        if self.measure in GetSerial_list:
            # model = {"model": ''}
            model = {}
        else:
            model = {"model": self.Settings.name}

        json_dict.update(model)

        return [json_dict]

    def __generate_vals(self):
        """
        Генерируем Блок vals
        :return: Возвращаем блок vals
        """

        # Итак - Что нам надо - сгенерировать и сохранить поле vals

        # Переопределяем поля
        measure = self.measure
        count_ts = self.count_ts

        # Генерируем
        # Если серийник
        if self.measure in GetSerial_list:
            tags = self.__generate_serial()
            JSON_vals = [{"tags": tags}]
        else:
            JSON_vals = GeneratorMeterValue(measure=measure,
                                            time=count_ts,
                                            Settings=self.Settings).JSON_vals
            # Вытаскиваем нужное поле
            JSON_vals = JSON_vals["vals"]

        return JSON_vals

    def __generate_serial(self):
        """Генерируем серийник """

        tag = [
            {
                "tag": "serial",
                "val": str(self.Settings.snumber)
            }
        ]

        return tag
