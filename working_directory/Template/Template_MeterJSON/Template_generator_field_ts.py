
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from working_directory.Template.Template_MeterJSON.Template_generator_field_tags import GeneratorTagsByDevices
from working_directory.Template.Template_MeterJSON.Template_generator_random_timestamp import GeneratorTimestamp
from copy import deepcopy


# --------------------------------------------------------------------------------------------------------------------
#                                 Генератор-конструктор Поля времени
# --------------------------------------------------------------------------------------------------------------------
# Конструктор для времени - добавляет время

class GeneratorValsByDevices:
    """
    Конструктор для времени - добавляет время в наш JSON- скелет

    """
    vals = []
    measure = ''
    count_ts = None
    Castrom_Value = None
    meterdev = False
    time_name = 'ts'

    # Конструктор для генерации тэгов - очень важно - принимает строковые значения

    def __init__(self,
                 # ОЧЕНЬ ВАЖНЫЙ ЭЛЕМЕНТ -УКАЗАТЕЛЬ ГЕНЕРАЦИИ УНИКАЛЬНОГО ВРЕМЕНИ
                 #  ЕСЛИ У НАС БУЛЕВЫЙ МАРКЕР - ТО ЛИБО ДА ЛИБО НЕТ ГЕНЕРАЦИЯ УНИКАЛЬНОГО РАНДОМНОГО TS
                 #  ЕСЛИ У НАС СПИСОК , ТО ПОДСТАВЛЯЕМ ВСЕ ЗНАЧЕНИЯ ИЗ ЭТОГО СПИСКА,
                 #  если список кончается - ставим таймштамп - 0
                 count_ts,
                 # ТИП ДАННЫХ ПОД КОТОРЫЙ ПРОВОДИМ ГЕНЕРАЦИЮ
                 measure: str,
                 # КАСТРОМНЫЕ ТЭГИ
                 Castrom_Value: dict = {},
                 # ЧТОБ БЫЛИ ПРАВИЛЬНЫЕ ТЭГИ -ГЕНЕРАЦИЯ ПОД формат meterdev
                 # ЭТО ВАЖНО, если у нас meterdev
                 meterdev:bool = False
                 ):

        # Переопределяем ТЭГИ
        self.measure = ''
        self.count_ts = None
        self.Castrom_Value = {}
        self.meterdev = False

        self.measure = measure
        self.count_ts = count_ts

        self.Castrom_Value = Castrom_Value
        self.meterdev = meterdev
        if meterdev:
            self.time_name = "time"


        # # Первое что делаем - смотрим - если это конфиг - то всегда время будет одно !!!
        # if (measure in Template_list_ArchTypes.ElectricConfig_ArchType_name_list) or \
        #         (measure in Template_list_ArchTypes.PulseConfig_ArchType_name_list) or \
        #         (measure in Template_list_ArchTypes.DigitalConfig_ArchType_name_list):
        #     self.count_ts = 1

        # ТЕПЕРЬ ГЕНЕРИРУЕМ САМО ПОЛЕ
        self.vals = self.__form_json_list_vals()

        # добавляем поле diff
        if meterdev and (self.vals is not None):
            for i in range(len(self.vals)):
                self.vals[i]["diff"] = 0

    # Конструктор JSON Массива с временем
    def __form_json_list_vals(self):
        # ЗАБИРАЕМ ТЭГИ
        measure = self.measure
        count = self.count_ts
        # Делаем шаблон массива
        vals_list = []
        # ---------------------------------------------------------------------------
        # А теперь факус - В зависимости от того какая нам нужна генерация - делаем разные ветвления.
        # ветка БУЛЕВОГО ПАРАМЕТРА >:
        if type(count) == int:
            # ГЕНЕРИРУЕМ УНИКАЛЬНЫЕ ЗНАЧЕНИЯ УКАЗАНЫМ КОЛИЧЕСТВОМ
            #формируем Отрывок JSON
            for i in range(count):
                # генерируем нужное количество УНИКАЛЬНОГО времени для нас
                unixtime_list = GeneratorTimestamp(count_ts=count).Timestamp
                vals_dict = {self.time_name: unixtime_list[i]}
                # Наш Unix-time
                # А сюда генерим нам массив тэгов что записываем
                generate = GeneratorTagsByDevices(measure=measure)
                # Если должны были что то перезаписать , перезаписываем
                if len(self.Castrom_Value) > 0:
                    generate.get_Castrom_Value(Castrom_Value=self.Castrom_Value)
                # теперь делаем следующее возвращаем массив значений что сгенерировали
                generate_tags = deepcopy(generate.tags)
                vals_dict['tags'] = generate_tags
                vals_list.append(vals_dict)

        # ЕСЛИ МЫ СПУСКАЕМ ЛИСТ
        elif type(count) == list:
            # ЕСЛИ ДЛИНА ЛИСТА БОЛЬШЕ 0
            if len(count) == 0:
                vals_list = None
            else:
                for i in range(len(count)):
                    # генерируем нужное количество УНИКАЛЬНОГО времени для нас
                    vals_dict = {self.time_name: deepcopy(count[i])}
                    # Наш Unix-time
                    # А сюда генерим нам массив тэгов что записываем
                    generate = GeneratorTagsByDevices(measure=measure)
                    # Если должны были что то перезаписать , перезаписываем
                    if len(self.Castrom_Value) > 0:
                        generate.get_Castrom_Value(Castrom_Value=self.Castrom_Value)
                    # теперь делаем следующее возвращаем массив значений что сгенерировали
                    generate_tags = deepcopy(generate.tags)
                    vals_dict['tags'] = generate_tags
                    vals_list.append(vals_dict)
        # ИНАЧЕ ГЕНЕРИУРЕМ ОДИН ТАЙМШТАМП С таймштампом 0
        else:
            # После чего мы берем и формируем Отрывок JSON
            vals_dict = {self.time_name: 0}
            # Наш Unix-time
            # А сюда генерим нам массив тэгов что записываем
            generate = GeneratorTagsByDevices(measure=measure)
            # Если должны были что то перезаписать , перезаписываем
            if len(self.Castrom_Value) > 0:
                generate.get_Castrom_Value(Castrom_Value=self.Castrom_Value)
            # теперь делаем следующее возвращаем массив значений что сгенерировали
            generate_tags = deepcopy(generate.tags)
            vals_dict['tags'] = generate_tags
            vals_list.append(vals_dict)

        return vals_list

    # Теперь отдаем то что нужно было отдавать

    def get_vals(self):
        """
        Функция которая возвращает результат генерации

        :return:
        """
        return self.vals

