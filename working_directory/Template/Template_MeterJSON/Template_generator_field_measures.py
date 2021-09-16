# Итак - начнем сразу с большого . Генератора measures
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from working_directory.Template.Template_MeterJSON.Template_generator_field_id import GeneratorIdDevices
from copy import deepcopy


class GeneratorMeasures:
    json = {}
    measure = []
    count_ts = None
    count_id = 0
    generate_ts_final = 0
    Castrom_Value = {}

    def __init__(self,
                 # ТИП ДАННЫХ ПОД КОТОРЫЙ ПРОВОДИМ ГЕНЕРАЦИЮ
                 measure: list,
                 # ОЧЕНЬ ВАЖНЫЙ ЭЛЕМЕНТ -УКАЗАТЕЛЬ ГЕНЕРАЦИИ УНИКАЛЬНОГО ВРЕМЕНИ
                 #  ЕСЛИ У НАС БУЛЕВЫЙ МАРКЕР - ТО ЛИБО ДА ЛИБО НЕТ ГЕНЕРАЦИЯ УНИКАЛЬНОГО РАНДОМНОГО TS
                 #  ЕСЛИ У НАС СПИСОК , ТО ПОДСТАВЛЯЕМ ВСЕ ЗНАЧЕНИЯ ИЗ ЭТОГО СПИСКА,

                 # КОЛИЧЕСТВО МОМЕНТОВ ВРЕМЕНИ - ЕТО ВАЖНА- В ПОСЛЕДВСТВИИ ВЛИЯЕТ НА ДЛИНУ JSON
                 count_ts: int = 3 or list,

                 # КОЛИЧЕСТВО АЙДИШНИКОВ - ЕТО ВАЖНА- В ПОСЛЕДВСТВИИ ВЛИЯЕТ НА ДЛИНУ JSON
                 count_id: int = 3 or list,

                 # КАСТРОМНЫЕ ТЭГИ
                 Castrom_Value: dict = {}):
        """
        Метод генератора JSON для post запроса
        генерирует JSON исходя из массива конфигов которые мы ему передали

        :param measure:Массив конфигов - Сюда пихать archtype Name
        :param generate_unicale_ts:Маркер генерации одних и тех же ts для всех - по умолчанию true.
                                    Если выставить false, то у всех ненерируемых значений будет один и тот же набор ts
        :param generate_unicale_id:Маркер генерации одних и тех же id для всех - по умолчанию true.
                                    Если выставить false, то у всех ненерируемых значений будет один и тот же набор id
        :param count_ts:Количество timestamp - Количество ts которое будет у каждого id - либо список времени
        :param count_id:Количество id - Количество id которое будет у каждого measure или список айдишников
        :param Castrom_Value:  НАБОР ТЭГОВ КОТОРЫЕ НАДО ПЕРЕООПРЕЛЕЛИТЬ

        :return: Возвращает сгенерированный по задданым параметрам JSON
        """

        # Переопределяем поля
        self.measure = measure

        self.count_ts = count_ts
        self.count_id = count_id

        self.Castrom_Value = Castrom_Value

        self.count_id = self.__generate_set_id()

        self.json = self.__generate_measure()

    def __generate_measure(self):
        """Здесь делаем генерацию основных элементов ,чоб нет """
        # для начала проверяем наш массив , что он не содержит ничего лишнего !!1
        measures = []
        list_measure = self.measure

        # Если у нас длина элементов больше нуля , то продолжаем
        if len(list_measure) > 0:

            # После чего проходимся по каждому элементу массива и проверяем - стринг ли он
            for i in range(len(list_measure)):
                if type(list_measure[i]) == str:
                    # Важный момент - проверяем на конфиг наш атрибут - Если да , то делаем замену
                    self.__limitation_in_quantity_ts_for_config(list_measure[i])

                    # Если это стринг то что мы делаем - формируем элемент массива из словаря
                    measures_dict = {}
                    # дергаем наш конфиг
                    measures_dict['measure'] = list_measure[i]
                    # генерируем данные для него
                    devices = GeneratorIdDevices(count_id=self.count_id,
                                                 count_ts=self.generate_ts_final,
                                                 measure=list_measure[i],
                                                 Castrom_Value=self.Castrom_Value)
                    measures_dict['devices'] = deepcopy(devices.devices)
                    measures.append(measures_dict)
            return measures

    # вспомогательная функция для ограничения ts для конфигов

    def __limitation_in_quantity_ts_for_config(self, measure: str):
        if (measure in Template_list_ArchTypes.ElectricConfig_ArchType_name_list) or \
                (measure in Template_list_ArchTypes.PulseConfig_ArchType_name_list) or \
                (measure in Template_list_ArchTypes.DigitalConfig_ArchType_name_list):
            # Теперь чтоб не выстрелить себе в ногу определяем количество времени
            if type(self.count_ts) == list:
                # Если у нас набор листа больше 1
                if len(self.count_ts) > 1:
                    self.generate_ts_final = [self.count_ts[0]]

                elif len(self.count_ts) == 1:
                    self.generate_ts_final = self.count_ts
                else:
                    self.generate_ts_final = 1

            elif type(self.count_ts) == int:
                # Если у нас набор листа больше 1
                if self.count_ts > 1:
                    self.generate_ts_final = 1

                elif self.count_ts == 1:
                    self.generate_ts_final = self.count_ts
                else:
                    self.generate_ts_final = 1

            else:
                self.generate_ts_final = 1

        else:
            self.generate_ts_final = self.count_ts

    # --------------------------------------------------------------------------------------------------------
    def __generate_set_id(self):
        """
        ОЧЕНЬ ВАЖНЫЙ МОМЕНТ _ ОТКАЗЫЕМСЯ ОТ УНИКАЛЬНЫХ АЙДИШНИКОВ
        :return:
        """

        #
        idx_set_list = []
        # Теперь генерируем айдишники - если это инт значения
        if type(self.count_id) == int:
            from working_directory.Template.Template_MeterJSON.Template_generator_random_device_idx import \
                GeneratorDeviceIdx

            idx = deepcopy(GeneratorDeviceIdx(count_id=self.count_id).id)
            # Теперь оттуда вытаскиваем значения
            for i in range(len(idx)):
                idx_set_list.append(idx[i]['DeviceIdx'])

            # После этого присваиваем новое значение
        else:
            idx_set_list = self.count_id

        return idx_set_list
