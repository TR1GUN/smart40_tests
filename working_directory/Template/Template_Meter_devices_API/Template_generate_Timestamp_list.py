from datetime import datetime, timedelta
import time
from working_directory.Template.Template_Meter_devices_API.Template_generator_time import measure_containin_day_list, \
    delta_day, measure_containin_month_list, measure_containin_half_hour_list, measure_containin_hour_list, \
    measure_moment_list, measure_Journal_list, delta_month, delta_half_hour, delta_hour, delta_moment, delta_Journal


# # -------------------------------------------------------------------------------------------------------------------
#                             Класс для Генерации нужного массива таймштампов - ЭТО ВАЖНО
# # -------------------------------------------------------------------------------------------------------------------

class GenerateTimestamp:
    measure = ''
    Time = None
    Timestamp_list = []
    # Глубина запроса времени
    delta_day: int = delta_day
    delta_month: int = delta_month
    delta_half_hour: int = delta_half_hour
    delta_hour: int = delta_hour
    delta_moment: int = delta_moment
    delta_Journal: int = delta_Journal
    cTime = 30
    Count_timestamp = None

    def __init__(self,
                 # Обязательные параметры:
                 # ТИП ДАННЫХ
                 measure,
                 # Временные ограничения
                 Time,
                 # КОЛИЧЕСТВО тайм штампов что генерируем - ЕСЛИ ПО СТАНДАРТУ - ТО ПИШЕМ ЗНАЧЕНИЕ NONE
                 Count_timestamp=None):


        self.measure = measure
        self.Time = Time
        self.Count_timestamp = Count_timestamp

        # НЕ ОБЯЗАТЕЛЬНЫЕ ДАННЫЕ
        # Глубина запроса времени

    def Generate_Timestamp_list(self):
        """
        Здесь генерируем нужное количество нужного времени относительно нашего JSON запроса
        :return:
        """

        # Пункт первый смотрим что у нас за 'measures'  и относительно него нам нужны таймштампы

        # Группа первая - Значения показателей на день
        if self.measure in measure_containin_day_list:
            # Число таймштампов равно глубине разницы дней -
            if self.Count_timestamp is not None:
                self.delta_day = self.Count_timestamp
            else:
                self.delta_day = datetime.fromtimestamp(self.Time['end']) - datetime.fromtimestamp(self.Time['start'])
                self.delta_day = self.delta_day.days
            # Если у нас показатель на начало суток - то включаем и сегодня тоже
            if self.measure in [measure_containin_day_list[0], measure_containin_day_list[2]]:
                self.delta_day = self.delta_day
                self.timestamp_list = self.__generate_correct_timestamp_through_timedelta(range_ts=self.delta_day,
                                                                                          day=1,
                                                                                          add_day=False)
            # Если нет , то и не включаем - СЧЕТ ИДЕТ ОТ ВЧЕРА
            else:
                self.delta_day = self.delta_day - 1
                # self.coun_ts = self.delta_day
                # А теперь генерируем список этих данных
                # Получаем наш список дат , измеряя каждый день
                self.timestamp_list = self.__generate_correct_timestamp_through_timedelta(range_ts=self.delta_day,
                                                                                          day=1,
                                                                                          add_day=True)

        # Группа вторая -  Значения показателей на месяц
        elif self.measure in measure_containin_month_list:
            if self.Count_timestamp is not None:
                self.delta_month = self.Count_timestamp

            if self.measure in [measure_containin_month_list[0], measure_containin_month_list[2]]:
                # self.coun_ts = self.delta_month
                self.timestamp_list = self.__generate_correct_timestamp(range_ts=self.delta_month, month=1)
            # Здесь делаем тоже самое что и с днями - для показаний потребления - отнимаем минус месяц
            else:
                # А теперь генерируем список этих данных
                self.delta_month = self.delta_month - 1
                self.timestamp_list = self.__generate_correct_timestamp(range_ts=self.delta_month, month=1,
                                                                        add_month=True)

        # Группа третья -  Значения показателей на 30 минут - ПРОФИЛИ МОЩНОСТИ
        elif self.measure in measure_containin_half_hour_list:
            # Число таймштампов равно глубине разницы дней -
            if self.Count_timestamp is not None:
                self.delta_half_hour = self.Count_timestamp
            # self.coun_ts = self.delta_half_hour
            # А теперь генерируем список этих данных
            # Получаем наш список дат , измеряя каждый день

            self.timestamp_list = self.__generate_correct_timestamp_through_timedelta(range_ts=self.delta_half_hour,
                                                                                      minute=int(self.cTime),
                                                                                      add_day=False)
        # Группа четвертая  - Значения показателей на час
        elif self.measure in measure_containin_hour_list:
            # Число таймштампов равно глубине разницы дней -
            if self.Count_timestamp is not None:
                self.delta_hour = self.Count_timestamp
            # self.coun_ts = delta_hour
            # А теперь генерируем список этих данных
            # Получаем наш список дат , измеряя каждый день
            self.timestamp_list = self.__generate_correct_timestamp_through_timedelta(range_ts=self.delta_hour, hour=1)

        # Группа пятая -  Моментное время
        elif self.measure in measure_moment_list:
            # Число таймштампов равно глубине разницы дней -
            # self.coun_ts = self.delta_moment
            # А теперь генерируем список этих данных
            # Получаем наш список дат , измеряя каждый день
            # self.timestamp_list = self.__generate_correct_timestamp_through_timedelta(range_ts=delta_moment, minute=1)
            # Обозначаем тут что это МГНОВЕНЫНЙ ПОКАЗАТЕЛЬ
            self.timestamp_list = [0]

        # Группа Шестая   -  ЖУРНАЛЫ
        elif self.measure in measure_Journal_list:
            # Число таймштампов равно глубине разницы дней -
            if self.Count_timestamp is not None:
                self.delta_Journal = self.Count_timestamp


            # self.coun_ts = delta_Journal
            # А теперь генерируем список этих данных
            # Получаем наш список дат , измеряя каждый день
            self.timestamp_list = self.__generate_correct_timestamp_through_timedelta(range_ts=self.delta_Journal,
                                                                                      day=1)

        # Иначе - Мы обрабаотываем мгновенные показатели
        else:

            # число таймштампов равно 1 - так как мгновенные показатели
            self.coun_ts = 1
            self.timestamp_list = self.__generate_correct_timestamp_through_timedelta(range_ts=self.delta_moment,
                                                                                      minute=0)

        return self.timestamp_list

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
        date_start = self.Time['start']
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
                                     month: int = 0, day: int = 0, hour: int = 0, minute: int = 0, add_month=False):
        """
        Итак - данная функция делает список из timestamp которые будут коректны
        :return:
        """
        timestamp_list = []
        # Пункт первый - Берем стартовую дату
        # date_start = self.Time['start']

        date_start = self.Time['end']
        # Переводим ее в нормальную дату
        date = datetime.fromtimestamp(date_start)
        # После чего начинаем ее изменять
        date = date.replace(day=1)
        # Если у нас стоит показатель на начало месяца то отнимаем один месяц
        if add_month:
            # НАЧИНАЕМ СО ПРОШЛОГО МЕСЯЦА
            last_month = date.month - 1
            if last_month < 1:
                last_year = date.year - 1
                last_month = 12
                date = date.replace(year=last_year, month=last_month)
            else:
                date = date.replace(month=last_month)

        for i in range(range_ts):
            # Изначально добавляем нашу дату, переведя ее в unixtime
            # ТЕПЕРЬ СТАВИМ ПЕРВОЕ ЧИСЛО !!!!

            unix_date = time.mktime(date.timetuple())
            timestamp_list.append(int(unix_date))
            # сначала делаем дельту
            # date_month = date.month + month
            date_month = date.month - month

            # Если у нас поулчается 13 месяц то меняем на 1
            # if date_month > 12:
            # date_year = date.year + 1
            # date_month = 1
            if date_month < 1:
                date_year = date.year - 1
                date_month = 12
                date = date.replace(year=date_year, month=date_month)
            else:
                date = date.replace(month=date_month)

            # # ТЕПЕРЬ СТАВИМ ПЕРВОЕ ЧИСЛО !!!!
            # date = date.replace(day=1)

        timestamp_list.reverse()
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
        # date_start = self.Time['start']
        # Начинаем с конца
        date_start = self.Time['end']
        # Переводим ее в нормальную дату
        date = datetime.fromtimestamp(date_start)
        if add_day:
            # НАЧИНАЕМ СО ВЧЕРА
            adding_day = timedelta(days=1)
            # adding_day = date.day + 1
            date = date - adding_day
            # date = date.replace(day=adding_day)
        # После чего начинаем ее изменять

        for i in range(range_ts):
            # Изначально добавляем нашу дату, переведя ее в unixtime
            unix_date = time.mktime(date.timetuple())
            timestamp_list.append(int(unix_date))
            # сначала делаем дельту

            time_delta = timedelta(days=day, hours=hour, minutes=minute, seconds=0, microseconds=0)
            # Добавляем нашу дельту времени
            # date = date + time_delta
            date = date - time_delta

        # После чего возвращаем наш массив

        timestamp_list.reverse()
        return timestamp_list


    # def _define_MomentTime(self):
    #     """
    #     :return:
    #     """
    # # Здесь расположим наш распределитель Который возвращает нужную функцию генерации
    # measure_dict =\
    #     {
    #
    #     # КОНФИГ
    #     'ElConfig': _define_ElConfig,
    #     # МОМЕНТНАЯ ЭНЕРГИЯ
    #     'ElMomentEnergy':_define_ElMomentEnergy,
    #     # ЭНЕРГИЯ НА НАЧАЛО ДНЯ
    #     'ElDayEnergy':_define_ElDayEnergy,
    #     # ЭНЕРГИЯ НА НАЧАЛО МЕСЯЦА
    #     'ElMonthEnergy':_define_ElMonthEnergy,
    #     # ПОТРЕБЛЯЕМАЯ ЭНЕРГИЯ НА НАЧАЛО ДНЯ
    #     'ElDayConsEnergy':_define_ElDayConsEnergy,
    #     # ПОТРЕБЛЯЕМАЯ ЭНЕРГИЯ НА МЕСЯЦ
    #     'ElMonthConsEnergy':_define_ElMonthConsEnergy,
    #     # ТЕКУЩИЕ ПОКАЗАНИЯ ПОКАЗАНИЯ КАЧЕСТВА СЕТИ
    #     'ElMomentQuality': _define_ElMomentQuality,
    #     # ПРОФИЛЬ МОЩНОСТИ
    #     'ElArr1ConsPower': _define_ElArr1ConsPower,
    #
    #     # ЖУРНАЛЫ
    #     'ElJrnlPwr':_define_Journal,
    #     'ElJrnlTimeCorr':_define_Journal,
    #     'ElJrnlReset':_define_Journal,
    #     'ElJrnlTrfCorr':_define_Journal,
    #     'ElJrnlOpen':_define_Journal,
    #     'ElJrnlUnAyth':_define_Journal,
    #     'ElJrnlPwrA':_define_Journal,
    #     'ElJrnlPwrB':_define_Journal,
    #     'ElJrnlPwrC':_define_Journal,
    #     'ElJrnlLimUAMax':_define_Journal,
    #     'ElJrnlLimUAMin':_define_Journal,
    #     'ElJrnlLimUBMax':_define_Journal,
    #     'ElJrnlLimUBMin':_define_Journal,
    #     'ElJrnlLimUCMax':_define_Journal,
    #     'ElJrnlLimUCMin':_define_Journal,
    # }
