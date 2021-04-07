# Здесь Расположим деконструктор JSONa

class Deconstruct:
    """
    Класс для валидации JSON + Его деконструктор до состояния набора масивов из ключей
    """
    JSON = {}
    JSON_deconstruct = []
    json_deconstruct_measures = None
    json_deconstruct_tag_val = None
    json_deconstruct_devices = None
    json_deconstruct_vals = None
    error = None

    Valid = False

    def __init__(self, JSON):

        self.JSON = JSON

        # Определяем сборщик ошибок
        self.error = []
        # Переопределяем нужные поля
        self.JSON_deconstruct = []
        self.json_deconstruct_measures = {}
        self.json_deconstruct_tag_val = {}
        self.json_deconstruct_devices = {}
        self.json_deconstruct_vals = {}
        # Опускаем в деконструктор
        self.parse_key_data()

        # Теперь смотрим сколько ошибок насобиралось
        if len(self.error) == 0:
            # Валидация успешна
            self.Valid = True

    def parse_key_data(self):
        """
        Проваливаемся в поле data
        :return:
        """
        try:
            data = self.JSON['data']
            self.parse_key_measures(data)
        except:
            self.error.append('Ошибка при валидации поля data ')

    def parse_key_measures(self, data):
        """
        Проваливаеся в поле measures
        :param data:
        :return:
        """
        try:
            measures = data['measures']
            for i in range(len(measures)):
                self.parse_key_devices(measures[i])
        except:
            self.error.append('Ошибка при валидации поля measures')

    def parse_key_devices(self, measures):
        """Проваливаемся в поле devices, забирая все ключи что должны быть"""
        try:
            # Забираем тип операции
            self.json_deconstruct_measures = {'type': measures['type']}

            devices = measures['devices']
            # Теперь перебираем все возможные комбинации
            for i in range(len(devices)):

                self.parse_key_vals(devices[i])

        except:
            self.error.append('Ошибка при валидации поля devices')

    def parse_key_vals(self, devices):
        """
        Проваливаемся в vals забирая все ключи что должны быть
        :return:
        """
        try:
            # Забираем все ключи , что насобирали
            self.json_deconstruct_devices = {}


            self.json_deconstruct_devices.update(self.json_deconstruct_measures)
            # Добавляем все ключи что тут будут
            self.json_deconstruct_devices["devices_model"] = devices["model"]
            self.json_deconstruct_devices["devices_serial"] = devices["serial"]
            vals = devices["vals"]
            # Теперь перебираем все возможные комбинации
            for i in range(len(vals)):
                self.parse_key_tags(vals[i])

        except:
            self.error.append('Ошибка при валидации поля vals')

    def parse_key_tags(self, vals):
        """
        Проваливаемся в tags забирая все ключи что должны быть
        :param vals:
        :return:
        """
        try:
            self.json_deconstruct_vals = {}
            # Забираем все ключи , что насобирали
            self.json_deconstruct_vals.update(self.json_deconstruct_devices)
            # Добавляем все ключи что тут будут
            self.json_deconstruct_vals["diff"] = vals["diff"]
            self.json_deconstruct_vals["time"] = vals["time"]
            # Теперь перебираем все возможные комбинации
            tags = vals["tags"]
            if tags is not None:
                self.parse_key_tag_val(tags)
            else:
                self.json_deconstruct_vals["tags"] = tags
                # и теперь обновляем наш JSON
                self.JSON_deconstruct.append(self.json_deconstruct_vals)

        except:
            self.error.append('Ошибка при валидации поля tags')

    def parse_key_tag_val(self, tags):
        """
        Забираем значения всех ключей из массива tags
        :param tags:
        """
        try:
            self.json_deconstruct_tag_val = {}
            # Собираем все ключи что были до этого
            self.json_deconstruct_tag_val.update(self.json_deconstruct_vals)
            # Теперь берем - и забиваем значениями
            for i in range(len(tags)):
                self.json_deconstruct_tag_val[tags[i]['tag']] = tags[i]['val']

            # Теперь все это собираем
            self.construct_json_list()

        except:
            self.error.append('Ошибка при валидации поля tag_val  - Тэги переных и их значения, блок данных!!!!')

    def construct_json_list(self):
        """
        А теперь здесь добавляем полученный нами список в общий массив
        :return:
        """
        try:
            self.JSON_deconstruct.append(self.json_deconstruct_tag_val)

        except:
            self.error.append('Ошибка при попытке сделать деконструктор')


class DeconstructGetSerial(Deconstruct):
    """
    Класс для валидации JSON + Его деконструктор до состояния набора масивов из ключей

    ЗДЕСЬ НЕ УЧИТЫВАЕТСЯ TS И ПОЛЕ MODEL
    """

    def parse_key_tags(self, vals):
        """
        Проваливаемся в tags забирая все ключи что должны быть
        :param vals:
        :return:
        """
        try:
            self.json_deconstruct_vals = {}
            # Забираем все ключи , что насобирали
            self.json_deconstruct_vals.update(self.json_deconstruct_devices)
            # Добавляем все ключи что тут будут


            # self.json_deconstruct_vals["diff"] = vals["diff"]


            # self.json_deconstruct_vals["time"] = vals["time"]
            # Теперь перебираем все возможные комбинации
            tags = vals["tags"]
            self.parse_key_tag_val(tags)

        except:
            self.error.append('Ошибка при валидации поля tags')

    def parse_key_vals(self, devices):
        """
        Проваливаемся в vals забирая все ключи что должны быть
        :return:
        """
        try:
            # Забираем все ключи , что насобирали
            self.json_deconstruct_devices = {}


            self.json_deconstruct_devices.update(self.json_deconstruct_measures)
            # Добавляем все ключи что тут будут
            # self.json_deconstruct_devices["devices_model"] = devices["model"]
            self.json_deconstruct_devices["devices_serial"] = devices["serial"]
            vals = devices["vals"]
            # Теперь перебираем все возможные комбинации
            for i in range(len(vals)):
                self.parse_key_tags(vals[i])

        except:
            self.error.append('Ошибка при валидации поля vals')


class DecostructSetType:
    """
    Класс для валидации JSON запросов на звапись настроек
    """
    JSON = {}
    JSON_deconstruct = []
    error = None
    Valid = False

    def __init__(self, JSON):

        self.JSON = JSON
        self.Valid = False
        # Определяем сборщик ошибок
        self.error = []
        # Переопределяем нужные поля

        # Деконструируем

        try:
            if self.JSON['data'] is None :
                self.JSON_deconstruct = [self.JSON['data']]

            else:
                self.error.append('Поле data Содержит какие то значения')
        except :
            self.error.append('Поля data не существует')

        # Теперь смотрим сколько ошибок насобиралось
        if len(self.error) == 0:
            # Валидация успешна
            self.Valid = True