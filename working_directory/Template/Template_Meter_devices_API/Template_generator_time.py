from working_directory.Template.Template_Meter_db_data_API.Template_list_ArchTypes import \
    JournalValues_ArchType_name_list, DigitalValues_ArchType_name_list, PulseValues_ArchType_name_list, \
    ElectricPowerValues_ArchType_name_list, ElectricQualityValues_ArchType_name_list, \
    ElecticEnergyValues_ArchType_name_list, DigitalConfig_ArchType_name_list, PulseConfig_ArchType_name_list, \
    ElectricConfig_ArchType_name_list
from datetime import datetime, timedelta
import time

# Что делаем - Делим все наши значения на несколько групп :

# Группа первая - Значения показателей на день
measure_containin_day_list = \
    [
        ElecticEnergyValues_ArchType_name_list[1],
        ElecticEnergyValues_ArchType_name_list[3],
        PulseValues_ArchType_name_list[1]
    ]
# Группа вторая -  Значения показателей на месяц
measure_containin_month_list = \
    [
        ElecticEnergyValues_ArchType_name_list[2],
        ElecticEnergyValues_ArchType_name_list[4],
        PulseValues_ArchType_name_list[2],

        # добаляем Журнал включения/выключения питания
        JournalValues_ArchType_name_list[0],
        # добаляем Журнал отказов в доступе
        JournalValues_ArchType_name_list[7]
    ]

# Группа третья -  Значения показателей на 30 минут
measure_containin_half_hour_list = \
    [
        ElectricPowerValues_ArchType_name_list[0]
    ]
# Группа четвертая  -  Значения показателей на час
measure_containin_hour_list = \
    [
        PulseValues_ArchType_name_list[3]
    ]
# Группа пятая   -  Моментное время
measure_moment_list = \
    [
        ElectricConfig_ArchType_name_list[0],
        PulseConfig_ArchType_name_list[0],
        DigitalConfig_ArchType_name_list[0],
        ElecticEnergyValues_ArchType_name_list[0],
        ElectricQualityValues_ArchType_name_list[0],
        PulseValues_ArchType_name_list[0],
        DigitalValues_ArchType_name_list[0],
    ]
# Группа Шестая   -  ЖУРНАЛЫ
measure_Journal_list = JournalValues_ArchType_name_list + [DigitalValues_ArchType_name_list[1]]
# Глубина запроса времени
delta_day = 30
delta_month = 12
delta_half_hour = 48
delta_hour = 24
delta_moment = 1
delta_Journal = 30


class GeneratorTime:
    """
    Генератор Времени

    Использует генератор юникс тайма из Meter_db_data_API

    Можно задать количество отрезков времени в count_time. По умолчанию стоит 1
    """

    time = None
    __count_time = 0

    def __init__(self, count_time: int = 1, measure: str = 'ElConfig'):
        self.time = []
        self.__count_time = count_time
        self.measure = measure
        # итак - Для более точной генерации времени нам понадобиться определить какой отрезок времени нам генерировать

        # Генерация на глубину 30 дней
        if measure in measure_containin_day_list:
            # Здесь разделяем - На начало дня или нет
            self.time = GeneratorTimestampDepthDay().Timestamp
        # Генерация на глубину 12 месяцев
        elif measure in measure_containin_month_list:
            # Здесь разделяем - На начало месяца или нет

            # начало месяца
            if measure in [measure_containin_month_list[0], measure_containin_month_list[2]]:
                self.time = GeneratorTimestampDepthMonth(before_month=True).Timestamp
            # или просто срез по месяцам
            else:
                self.time = GeneratorTimestampDepthMonth(before_month=False).Timestamp
        # Генерация на глубину по пол часа на сутки
        elif measure in measure_containin_half_hour_list:
            self.time = GeneratorTimestampByParameters(day=1).Timestamp
        # Генерация на глубину по часу на сутки
        elif measure in measure_containin_hour_list:
            self.time = GeneratorTimestampByParameters(day=1).Timestamp
        # Генерация на глубину в 1 запись
        elif measure in measure_moment_list:
            self.time = GeneratorTimestampByParameters(hour=1).Timestamp
        # Генерация на глубину 30 дней
        elif measure in measure_Journal_list:
            # self.time = GeneratorTimestampDepthMonth().Timestamp
            self.time = GeneratorTimestampByParameters(day=30).Timestamp
        else:
            # Иначе - ставим время по умолчанию
            self.time = [{"start": 1506180007, "end": 1609459200}]


class GeneratorTimestampDepthDay:
    """
    Генератор времени на глубину 30 дней от текущей даты
    """
    Timestamp = []

    def __init__(self, before_day: bool = False):
        if before_day:
            self.__generate_ts_before_day()
        else:
            self.__generate_ts()

    def __generate_ts(self):
        """
        Функция для генерации двух отрезков времени - от текущей даты , на глубину в 30 дней

        Значения переводятся в UNIX time

        :return:  Возвращает рандомное время в заданом диапазоне
        """

        # Генерируем сегодняшяшнюю дату-время
        end = datetime.now()

        # Ставим начало суток
        end = end.replace(hour=0, minute=0, second=0, microsecond=0)

        # Отматываем на завтра

        # Берем дельту времени
        start = timedelta(days=delta_day)
        # После чего ее вычитаем
        start = end - start
        # Теперь переводим все это в юнекс тайм
        unix_start = time.mktime(start.timetuple())
        unix_end = time.mktime(end.timetuple())

        self.Timestamp = [{"start": int(unix_start), "end": int(unix_end)}]

    def __generate_ts_before_day(self):
        """
        Функция для генерации двух отрезков времени - от текущей даты , на глубину в 30 дней НА НАЧАЛО СУТОК

        Значения переводятся в UNIX time

        :return:  Возвращает рандомное время в заданом диапазоне
        """

        # Генерируем сегодняшяшнюю дату-время
        end = datetime.now()

        # Ставим начало суток
        end = end.replace(hour=0, minute=0, second=0, microsecond=0)

        # Отматываем на завтра

        # Берем дельту времени
        start = timedelta(days=delta_day + 1)
        # После чего ее вычитаем
        start = end - start
        # Теперь переводим все это в юнекс тайм
        unix_start = time.mktime(start.timetuple())
        unix_end = time.mktime(end.timetuple())

        self.Timestamp = [{"start": int(unix_start), "end": int(unix_end)}]


class GeneratorTimestampDepthMonth:
    """

        Генератор времени на глубину 12 месяцев от текущей даты

    """

    Timestamp = []

    def __init__(self, before_month: bool):
        if before_month:
            self.__generate_ts_before_Month()
        else:
            self.__generate_ts()

    def __generate_ts(self):
        """
        Функция для генерации двух отрезков времени - от текущей даты , на глубину 12 месяцев

        Значения переводятся в UNIX time

        :return:  Возвращает рандомное время в заданом диапазоне
        """

        # Генерируем сегодняшяшнюю дату-время
        end = datetime.now()

        # Ставим начало суток
        end = end.replace(hour=0, minute=0, second=0, microsecond=0)

        # Берем дельту времени
        last_year = int(end.year) - 1
        # После чего ее вычитаем
        start = end.replace(year=last_year, day=1)

        # Теперь переводим все это в юнекс тайм
        unix_start = time.mktime(start.timetuple())
        unix_end = time.mktime(end.timetuple())

        self.Timestamp = [{"start": int(unix_start), "end": int(unix_end)}]

    def __generate_ts_before_Month(self):
        """
        Функция для генерации двух отрезков времени - от текущей даты , на глубину 12 месяцев

        Значения переводятся в UNIX time

        :return:  Возвращает рандомное время в заданом диапазоне
        """

        # Генерируем сегодняшяшнюю дату-время
        end = datetime.now()

        # Ставим начало суток
        end = end.replace(hour=0, minute=0, second=0, microsecond=0)

        # Берем дельту времени
        last_year = int(end.year) - 1
        last_month = int(end.month) + 1
        if last_month > 12:
            last_month = 1
        # После чего ее вычитаем
        start = end.replace(year=last_year, day=1, month=last_month)

        # Теперь переводим все это в юнекс тайм
        unix_start = time.mktime(start.timetuple())
        unix_end = time.mktime(end.timetuple())

        self.Timestamp = [{"start": int(unix_start), "end": int(unix_end)}]


class GeneratorTimestampByParameters:
    """

        Генератор времени на указаную глубину

    """
    Timestamp = []

    def __init__(self, hour: int = 0, day: int = 0):
        self.hour = hour
        self.day = day
        self.__generate_ts()

    def __generate_ts(self):
        """
        Функция для генерации двух отрезков времени - от текущей даты , на указанную глубину

        Значения переводятся в UNIX time

        :return:  Возвращает рандомное время в заданом диапазоне
        """

        # Генерируем сегодняшяшнюю дату-время
        end = datetime.now()
        # Ставим начало суток
        end = end.replace(hour=0, minute=0, second=0, microsecond=0)
        # Берем дельту времени
        start = timedelta(days=self.day, hours=self.hour)
        # После чего ее вычитаем
        start = end - start
        # Теперь переводим все это в юнекс тайм
        unix_start = time.mktime(start.timetuple())
        unix_end = time.mktime(end.timetuple())
        self.Timestamp = [{"start": int(unix_start), "end": int(unix_end)}]
