# Здесь расположим генератор значений для имитатора Счетчика
from working_directory.Template.Template_MeterJSON.Template_generator_field_ts import GeneratorValsByDevices

from working_directory.Template.Template_Meter_devices_API.Template_define_rewrite_added_tags import AddedKeysTag, \
    DefineKeysTag

from copy import deepcopy


class GeneratorMeterValue:
    """
    Здесь расположим генератор для значений которые будет слать счетчик

    """
    measure = None
    coun_ts = None
    JSON_vals = {}
    time = {}
    Settings = {'model': '', 'serial': ''}

    def __init__(self, measure: str, time: list, Settings=None , save = False):
        # Переопределяем наши переменные
        if Settings is None:
            config = {'model': '', 'serial': ''}
        self.measure = measure
        # self.time = time
        self.timestamp_list = time
        self.Settings = Settings

        # Генерируем наши данные
        JSON_meter_value = self.__generate_primary_JSON()
        # Теперь его Отдаем взад
        self.JSON_vals = JSON_meter_value

        if save:
            # А теперь сохраняем все то что мы на генерирвоали
            self.__save_JSON_meter_value()

    def __save_JSON_meter_value(self):
        """
        Метод Для сохранения в папку счетчика всего того что мы нагенерирвоали - ЭТО ВАЖНО
        :return:
        """
        from working_directory.Connect.JSON_format_coding_decoding import code_JSON
        import write_file

        JSON_meter_value = self.JSON_vals
        # Теперь все это упаковываем в JSON и сохраняем
        JSON_meter_value = code_JSON(JSON_meter_value)

        write_file.write_file_JSON_on_Emulator(writen_text=JSON_meter_value)

    def __generate_primary_JSON(self):
        """
        Здесь генерируем первичный JSON из meter_data

        :return:
        """

        # Вызываем нужный генератор -
        JSON_primary_meter_value = GeneratorValsByDevices(measure=self.measure,
                                                          count_ts=deepcopy(self.timestamp_list),
                                                          meterdev=True,
                                                          Castrom_Value=DefineKeysTag(measure=self.measure,
                                                                                      Settings=self.Settings).tags
                                                          ).vals
        # Здесь берем и переопределяем некоторые знеачения в зависимости от шаблона
        JSON_primary_meter_value = self.__redefinition_of_keys(JSON_primary_meter_value)

        # И Здесь что мы делаем - МЫ назначаем это все на ключ vals и отдаем
        JSON_meter_value = {"vals": JSON_primary_meter_value}

        return JSON_meter_value

    def __redefinition_of_keys(self, JSON_meter_value):
        '''
        ВААААЖНЫЙ МЕТОД ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ КЛЮЧей И ИХ ЗНАЧЕНИЙ.

        :param JSON_meter_value:
        :return:
        '''

        for i in range(len(JSON_meter_value)):
            # Получаем наш список необходимых для добавления значений
            added_tags = AddedKeysTag(measure=self.measure, Settings=self.Settings).tags

            # И апгрейдим его
            JSON_meter_value[i]['tags'] = JSON_meter_value[i]['tags'] + added_tags


        # ПРИВОДИМ К НОРМАЛЬНОЙ ФОРМЕ
        JSON_meter_value = self.__rewrite_normal_form(JSON_meter_value)


            # print('ЧО НАЩЛИ',added_tags)
            # print('КУДА ДОБАВЛЯЕМ',JSON_meter_value[i])

        return JSON_meter_value

    def __rewrite_normal_form(self, JSON_meter_value):
        """
        ЗДЕСЬ ПРИВОДИМ К НОРМАЛЬНОЙ ФОРМКЕ НАШ JSON
        :return:
        """

        from working_directory.Template.Template_Meter_db_data_API.Template_list_ArchTypes import \
            JournalValues_ArchType_name_list

        # ПУНКТ ПЕРВЫЙ - ЖУРНАЛЬНЫЕ ЗНАЧЕНИЯ
        if self.measure in JournalValues_ArchType_name_list:
            for i in range(len(JSON_meter_value)):
                # Не ТРОГАЕМ ТАЙМШТАМПЫ
                tags_list = JSON_meter_value[i]['tags']
                for x in range(len(tags_list)):
                    # После ЭТОГО переопределяем eventId
                    if JSON_meter_value[i]['tags'][x]['tag'] == 'eventId':
                        # Ставим эвент номеру элемента
                        JSON_meter_value[i]['tags'][x]['val'] = i

        return JSON_meter_value

