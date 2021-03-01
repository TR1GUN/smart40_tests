# Здесь расположим генератор значений для имитатора Счетчика
from working_directory.Template.Template_Meter_db_data_API.Template_generator_measures_ts import GeneratorValsByDevices
from working_directory.Connect.JSON_format_coding_decoding import code_JSON, decode_JSON
import time, write_file
from working_directory.Template.Template_Meter_devices_API.Template_generator_time import measure_containin_day_list, \
    delta_day, measure_containin_month_list, measure_containin_half_hour_list, measure_containin_hour_list, \
    measure_moment_list, measure_Journal_list, delta_month, delta_half_hour, delta_hour, delta_moment, delta_Journal

from working_directory.Template.Template_Meter_devices_API.Template_list_job import Journal_dict
from datetime import datetime, timedelta


class GeneratorMeterValue:
    """
    Здесь расположим генератор для значений которые будет слать счетчик

    """
    measure = None
    coun_ts = None
    JSON_vals = {}
    time = {}
    Settings = {'model': '', 'serial': ''}

    def __init__(self, measure: str, time: dict, Settings=None):
        # Переопределяем наши переменные
        if Settings is None:
            config = {'model': '', 'serial': ''}
        self.measure = measure
        self.time = time
        self.Settings = Settings

        # Генерируем нужные ts
        self.__generate_count_ts_relatively_time_json_request()

        # Генерируем наши данные
        JSON_meter_value = self.__generate_primary_JSON()
        # Теперь его Отдаем взад
        self.JSON_vals = JSON_meter_value

        # А теперь сохраняем все то что мы на генерирвоали
        self.__save_JSON_meter_value()

    def __save_JSON_meter_value(self):
        """
        Метод Для сохранения в папку счетчика всего того что мы нагенерирвоали - ЭТО ВАЖНО
        :return:
        """
        JSON_meter_value = self.JSON_vals
        # Теперь все это упаковываем в JSON и сохраняем
        JSON_meter_value = code_JSON(JSON_meter_value)

        write_file.write_file_JSON_on_Emulator(writen_text=JSON_meter_value)

    def __generate_primary_JSON(self):
        """
        Здесь генерируем первичный JSON из meter_data

        :return:
        """
        # Количество таймштампов равно сгенерированных ранее отрезков времени!!!

        self.coun_ts = len(self.timestamp_list)
        # Вызываем нужный генератор -
        JSON_primary_meter_value = GeneratorValsByDevices(measure=self.measure,
                                                          count_ts=self.coun_ts,
                                                          generate_unicale=True).get_vals()

        # Здесь берем и переопределяем некоторые знеачения в зависимости от шаблона
        JSON_primary_meter_value = self.__redefinition_of_keys(JSON_primary_meter_value)

        # Что делаем теперь - Перезаписываем некоторые поля
        for i in range(len(JSON_primary_meter_value)):
            # Переназначаем тэги
            JSON_primary_meter_value[i]["time"] = JSON_primary_meter_value[i].pop('ts')
            # Здесь можно перезаписать наш Time
            JSON_primary_meter_value[i]["time"] = self.timestamp_list[i]
            # Добавляем поле diff
            JSON_primary_meter_value[i]["diff"] = 0

        # И Здесь что мы делаем - МЫ назначаем это все на ключ vals и отдаем
        JSON_meter_value = {"vals": JSON_primary_meter_value}
        return JSON_meter_value

    def __redefinition_of_keys(self, JSON_meter_value):
        '''
        ВААААЖНЫЙ МЕТОД ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ КЛЮЧей И ИХ ЗНАЧЕНИЙ.


        :param JSON_meter_value:
        :return:
        '''
        # Переопределяем - Итак - самое кайфовое - ЖУРНАЛЫ

        # ПУНКТ ПЕРВЫЙ - ЖУРНАЛЬНЫЕ ЗНАЧЕНИЯ
        if self.measure in ['ElJrnlLimUAMax', 'ElJrnlLimUAMin',
                            'ElJrnlLimUBMax', 'ElJrnlLimUBMin',
                            'ElJrnlLimUCMax', 'ElJrnlLimUCMin',
                            'ElJrnlPwrC', 'ElJrnlPwrB', 'ElJrnlPwrA',
                            'ElJrnlPwr', 'ElJrnlTimeCorr', 'ElJrnlReset', 'ElJrnlTrfCorr', 'ElJrnlOpen', 'ElJrnlUnAyth'
                            ]:
            for i in range(len(JSON_meter_value)):

                # Не ТРОГАЕМ ТАЙМШТАМПЫ
                tags_list = JSON_meter_value[i]['tags']
                for x in range(len(tags_list)):
                    # После ЭТОГО переопределяем eventId
                    if JSON_meter_value[i]['tags'][x]['tag'] == 'eventId':
                        # Ставим эвент номеру элемента
                        JSON_meter_value[i]['tags'][x]['val'] = i + 1
                # После добавляем новый словарь JournalID
                JournalID_dict = {'tag': 'journalID', 'val': Journal_dict[self.measure]}
                # А теперь его добавляем к нашим значениям
                JSON_meter_value[i]['tags'].append(JournalID_dict)
        # ПУНКТ ВТОРОЙ - КОНФИГИ
        if self.measure in ["ElConfig"]:
            # Формируем тут конфиги Которых нет
            config_list = [
                {
                    "tag": "VarConsDepth",
                    "val": None
                },
                {
                    "tag": "MonDepth",
                    "val": None
                },
                {
                    "tag": "MonConsDepth",
                    "val": None
                },
                {
                    "tag": "DayDepth",
                    "val": None
                },
                {
                    "tag": "DayConsDepth",
                    "val": None
                },
                {
                    "tag": "cTime",
                    "val": None
                },
                {
                    "tag": "isCons",
                    "val": None
                }
            ]

            for i in range(len(JSON_meter_value)):
                # Не ТРОГАЕМ ТАЙМШТАМПЫ
                JSON_meter_value[i]['tags'] = JSON_meter_value[i]['tags'] + config_list
                tags_list = JSON_meter_value[i]['tags']
                for x in range(len(tags_list)):

                    # После ЭТОГО переопределяем :
                    # МОДЕЛЬ
                    if JSON_meter_value[i]['tags'][x]['tag'] == 'model':
                        JSON_meter_value[i]['tags'][x]['val'] = self.Settings.name
                    # СЕРИЙНИК
                    elif JSON_meter_value[i]['tags'][x]['tag'] == 'serial':
                        JSON_meter_value[i]['tags'][x]['val'] = self.Settings.snumber
                    # cArrays - количество архивов профилей мощности (на данный момент -  всегда 1)
                    elif JSON_meter_value[i]['tags'][x]['tag'] == 'cArrays':
                        JSON_meter_value[i]['tags'][x]['val'] = 1

                    elif JSON_meter_value[i]['tags'][x]['tag'] == 'const':
                        JSON_meter_value[i]['tags'][x]['val'] = 1.0
                    # значение тэга isDst - разрешение перехода на летнее время - берется из Кучи параметров -
                    # здесь хардкодим , как в самом счетчике
                    elif JSON_meter_value[i]['tags'][x]['tag'] == 'isDst':
                        JSON_meter_value[i]['tags'][x]['val'] = False
                    # наличие часов (есть всегда для энергомеры)
                    elif JSON_meter_value[i]['tags'][x]['tag'] == 'isClock':
                        JSON_meter_value[i]['tags'][x]['val'] = True
                    # isTrf - наличие тарификатора (есть всегда для энергомеры)
                    elif JSON_meter_value[i]['tags'][x]['tag'] == 'isTrf':
                        JSON_meter_value[i]['tags'][x]['val'] = True

                    elif JSON_meter_value[i]['tags'][x]['tag'] == 'isCons':
                        JSON_meter_value[i]['tags'][x]['val'] = True
                    elif JSON_meter_value[i]['tags'][x]['tag'] == 'cTime':
                        JSON_meter_value[i]['tags'][x]['val'] = 30

                    # Глубина хранения суточных энергий, накопленных по тарифам
                    elif JSON_meter_value[i]['tags'][x]['tag'] == 'DayConsDepth':
                        JSON_meter_value[i]['tags'][x]['val'] = 44
                    elif JSON_meter_value[i]['tags'][x]['tag'] == 'DayDepth':
                        JSON_meter_value[i]['tags'][x]['val'] = 44

                    # Глубина хранения месячных максимумов мощности по тарифам
                    elif JSON_meter_value[i]['tags'][x]['tag'] == 'MonConsDepth':
                        JSON_meter_value[i]['tags'][x]['val'] = 13
                    elif JSON_meter_value[i]['tags'][x]['tag'] == 'MonDepth':
                        JSON_meter_value[i]['tags'][x]['val'] = 12
                    elif JSON_meter_value[i]['tags'][x]['tag'] == 'VarConsDepth':
                        JSON_meter_value[i]['tags'][x]['val'] = 4752

                    # наличие обратной активной энергии ,
                    # наличие обратной реактивной энергии и наличие прямой реактивной энергии
                    elif JSON_meter_value[i]['tags'][x]['tag'] in ['isAm', 'isRm', 'isAm', 'isCons', 'isRp']:
                        if self.Settings.name == 'CE303':
                            JSON_meter_value[i]['tags'][x]['val'] = True
                        else:
                            JSON_meter_value[i]['tags'][x]['val'] = True
        # ПУНКТ ТРЕТИЙ - профили мощности первого архива электросчетчика
        if self.measure in ["ElArr1ConsPower"]:
            # Формируем тут тэги Которых нет
            config_list = [
                {
                    "tag": "isMeas",
                    "val": False
                },
                {
                    "tag": "cTime",
                    "val": 42
                }
            ]
            # перезаписываем те что уже сгенерирвоаны
            for i in range(len(JSON_meter_value)):
                # Не ТРОГАЕМ ТАЙМШТАМПЫ
                JSON_meter_value[i]['tags'] = JSON_meter_value[i]['tags'] + config_list
                tags_list = JSON_meter_value[i]['tags']
                for x in range(len(tags_list)):
                    # После ЭТОГО переопределяем :
                    if JSON_meter_value[i]['tags'][x]['tag'] in ["isPart", "isOvfl", "isSummer"]:
                        JSON_meter_value[i]['tags'][x]['val'] = False

        # ПУНКТ Четвертый - текущие ПКЭ электросчетчика Достраиваем до нужного значения
        if self.measure in ["ElMomentQuality"]:
            # перезаписываем те что уже сгенерирвоаны
            for i in range(len(JSON_meter_value)):
                # Не ТРОГАЕМ ТАЙМШТАМПЫ
                JSON_meter_value[i]['tags'] = JSON_meter_value[i]['tags']
                tags_list = JSON_meter_value[i]['tags']
                for x in range(len(tags_list)):
                    # После ЭТОГО переопределяем :
                    if JSON_meter_value[i]['tags'][x]['tag'] in ['SA', 'SB', 'SC', 'SS']:
                        JSON_meter_value[i]['tags'][x]['val'] = None

        return JSON_meter_value

    def __generate_count_ts_relatively_time_json_request(self):
        """
        Здесь генерируем нужное количество нужного времени относительно нашего jSON запроса
        :return:
        """

        # Пункт первый смотрим что у нас за 'measures'  и относительно него нам нужны таймштампы

        # Группа первая - Значения показателей на день
        if self.measure in measure_containin_day_list:
            # Число таймштампов равно глубине разницы дней -
            delta_day = datetime.fromtimestamp(self.time['end']) - datetime.fromtimestamp(self.time['start'])

            # Если у нас показатель на начало суток - то включаем и сегодня тоже
            if self.measure in [measure_containin_day_list[0], measure_containin_day_list[2]]:
                delta_day = delta_day.days + 1

            # Если нет , то и не включаем
            else:
                delta_day = delta_day.days
            self.coun_ts = delta_day
            # А теперь генерируем список этих данных
            # Получаем наш список дат , измеряя каждый день
            self.timestamp_list = self.__generate_correct_timestamp_through_timedelta(range_ts=delta_day, day=1)

        # Группа вторая -  Значения показателей на месяц
        elif self.measure in measure_containin_month_list:
            # Число таймштампов равно глубине разницы дней -

            self.coun_ts = delta_month
            # А теперь генерируем список этих данных
            self.timestamp_list = self.__generate_correct_timestamp(range_ts=delta_month, month=1)

        # Группа третья -  Значения показателей на 30 минут
        elif self.measure in measure_containin_half_hour_list:
            # Число таймштампов равно глубине разницы дней -
            self.coun_ts = delta_half_hour
            # А теперь генерируем список этих данных
            # Получаем наш список дат , измеряя каждый день
            self.timestamp_list = self.__generate_correct_timestamp_through_timedelta(range_ts=delta_half_hour,
                                                                                      minute=30, add_day=False)
        # Группа четвертая  -  Значения показателей на час
        elif self.measure in measure_containin_hour_list:
            # Число таймштампов равно глубине разницы дней -

            self.coun_ts = delta_hour
            # А теперь генерируем список этих данных
            # Получаем наш список дат , измеряя каждый день
            self.timestamp_list = self.__generate_correct_timestamp_through_timedelta(range_ts=delta_hour, hour=1)

        # Группа пятая   -  Моментное время
        elif self.measure in measure_moment_list:
            # Число таймштампов равно глубине разницы дней -
            self.coun_ts = delta_moment
            # А теперь генерируем список этих данных
            # Получаем наш список дат , измеряя каждый день
            self.timestamp_list = self.__generate_correct_timestamp_through_timedelta(range_ts=delta_moment, minute=1)

        # Группа Шестая   -  ЖУРНАЛЫ
        elif self.measure in measure_Journal_list:
            # Число таймштампов равно глубине разницы дней -
            self.coun_ts = delta_Journal
            # А теперь генерируем список этих данных
            # Получаем наш список дат , измеряя каждый день
            self.timestamp_list = self.__generate_correct_timestamp_through_timedelta(range_ts=delta_Journal, day=1)

        # Иначе - Мы обрабаотываем мгновенные показатели
        else:
            # число таймштампов равно 1 - так как мгновенные показатели
            self.coun_ts = 1
            self.timestamp_list = self.__generate_correct_timestamp_through_timedelta(range_ts=delta_moment, minute=0)

    def __generate_correct_timestamp_for_beginning_of_month(self, range_ts: int = 0,
                                                            month: int = 0, day: int = 0,
                                                            hour: int = 0, minute: int = 0):
        """
        ФУНКЦИЯ ГЕНЕРАЦИИ ВРЕМЕНИ НА НАЧАЛО МЕСЯЦА - ЭТО ВАЖНО
        :param range_ts:
        :param month:
        :param day:
        :param hour:
        :param minute:
        :return:
        """

        timestamp_list = []
        # Пункт первый - Берем стартовую дату
        date_start = self.time['start']
        # Переводим ее в нормальную дату
        date = datetime.fromtimestamp(date_start)
        # После чего начинаем ее изменять
        for i in range(range_ts):
            # Изначально добавляем нашу дату, переведя ее в unixtime
            unix_date = time.mktime(date.timetuple())
            timestamp_list.append(int(unix_date))
            # сначала делаем дельту
            date_month = date.month + month
            # Если у нас поулчается 13 месяц то меняем на 1
            if date_month > 12:
                date_year = date.year + 1
                date_month = 1
                date = date.replace(year=date_year, month=date_month)
            else:
                date = date.replace(month=date_month)

            # ТЕПЕРЬ СТАВИМ ПЕРВОЕ ЧИСЛО !!!!
            date = date.replace(day=1)
            # А теперь добавляем наше число
            unix_date = time.mktime(date.timetuple())
            timestamp_list.append(int(unix_date))
            # После чего возвращаем наш массив

        return timestamp_list

    def __generate_correct_timestamp(self, range_ts: int = 0,
                                     month: int = 0, day: int = 0, hour: int = 0, minute: int = 0):
        """
        Итак - данная функция делает список из timestamp которые будут коректны
        :return:
        """
        timestamp_list = []
        # Пункт первый - Берем стартовую дату
        date_start = self.time['start']
        # Переводим ее в нормальную дату
        date = datetime.fromtimestamp(date_start)
        # После чего начинаем ее изменять
        for i in range(range_ts):
            # Изначально добавляем нашу дату, переведя ее в unixtime
            unix_date = time.mktime(date.timetuple())
            timestamp_list.append(int(unix_date))
            # сначала делаем дельту
            date_month = date.month + month
            # Если у нас поулчается 13 месяц то меняем на 1
            if date_month > 12:
                date_year = date.year + 1
                date_month = 1
                date = date.replace(year=date_year, month=date_month)
            else:
                date = date.replace(month=date_month)

            # ТЕПЕРЬ СТАВИМ ПЕРВОЕ ЧИСЛО !!!!
            date = date.replace(day=1)

        # После чего возвращаем наш массив
        return timestamp_list

    def __generate_correct_timestamp_through_timedelta(self, range_ts: int = 0, day: int = 0,
                                                       hour: int = 0, minute: int = 0, add_day: bool = False):

        """
        Итак - данная функция делает список из timestamp которые будут коректны через таймдельту

        :param range_ts:
        :param day:
        :param hour:
        :param minute:
        :return:
        """
        timestamp_list = []
        # Пункт первый - Берем стартовую дату
        date_start = self.time['start']

        # Переводим ее в нормальную дату
        date = datetime.fromtimestamp(date_start)
        if add_day:
            # Добавляем один день вперед
            adding_day = timedelta(days=1)
            # adding_day = date.day + 1
            date = date + adding_day
            # date = date.replace(day=adding_day)

        # После чего начинаем ее изменять
        for i in range(range_ts):
            # Изначально добавляем нашу дату, переведя ее в unixtime
            unix_date = time.mktime(date.timetuple())
            timestamp_list.append(int(unix_date))
            # сначала делаем дельту

            time_delta = timedelta(days=day, hours=hour, minutes=minute, seconds=0, microseconds=0)
            # Добавляем нашу дельту времени
            date = date + time_delta

        # После чего возвращаем наш массив
        return timestamp_list
