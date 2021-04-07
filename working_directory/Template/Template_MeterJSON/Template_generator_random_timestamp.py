from random import randint

# --------------------------------------------------------------------------------------------------------------------
#                                 Генератор времени
# --------------------------------------------------------------------------------------------------------------------
# Выведем отдельным классом генерацию времени


class GeneratorTimestamp:
    Timestamp = []
    "Генератор времени"
    start = 1500000000
    finis = 1609459200

    def __init__(self, count_ts):

        self.Timestamp = self.__generate_ts(count=count_ts)

    #     Сам генератор времени:
    def __generate_ts(self, count: int):
        """
        Функция для генерации рандомного времени в Unix-time от Jul 14 2017 05:40:00 до Nov 15 2023 01:13:20

        :return:  Возвращает рандомное время в заданом диапазоне
        """
        unixtime_set = set()
        # генерируем нужное колличество :
        for i in range(count):
            # генерим нужное число
            unixtime = randint(self.start, self.finis)
            # если оно есть - то генерим до тех пор пока не получим нужное
            if unixtime in unixtime_set:
                while unixtime not in unixtime_set:
                    unixtime = randint(self.start, self.finis)
            unixtime_set.add(unixtime)

        return list(unixtime_set)

    def get_Timestamp(self):
        return self.Timestamp
# --------------------------------------------------------------------------------------------------------------------