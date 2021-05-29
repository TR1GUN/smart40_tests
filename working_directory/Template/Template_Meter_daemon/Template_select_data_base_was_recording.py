# ---------------------------------------------------------------------------------------------------------------------
#                         Здесь расположем главный класс Для ПОЛУЧЕНИЯ НАБОРА ДАННЫХ
#                             КОТОРЫЕ ОТОБРАЖАЮТ ЧТО ПО ФАКТУ БЫЛО ЗАПИСАННО В БД
# ---------------------------------------------------------------------------------------------------------------------

class DataBaseWasRecordingInFact:
    """
    Здесь расположим класс который Смотрит что было запсианно по факту - ЭТО ВАЖНО

    """
    database_before = []
    database_after = []
    DataBase_was_recording = []

    def __init__(self,
                 # БД ДО ЗАПИСИ
                 database_before: list,
                 # БД ПОСЛЕ ЗАПИСИ
                 database_after: list):

        self.database_before = database_before
        self.database_after = database_after

        self.DataBase_was_recording = self.__getting_recording_record_after_fact(DataBase_after=self.database_after,
                                                                                 DataBase_before=self.database_before)

        # self.DataBase_was_recording = DeleteValidToZero(self.DataBase_was_recording).database
    # //---------------------------------------------------------------------------------------------------
    # ///--------------------------      ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ    ---------------------------------------
    # //---------------------------------------------------------------------------------------------------

    def __getting_recording_record_after_fact(self, DataBase_after, DataBase_before):
        """Здесь получаем то, что записали по факту в ТАблицу"""

        import copy
        # копируем нащу БД после записи
        DataBase_after_the_fact = copy.deepcopy(DataBase_after)
        # print('DataBase_after', DataBase_after)
        # print('DataBase_before', DataBase_before)

        # Теперь удаляем все то что было записанно ДО тог как прогнали тесты
        for i in range(len(DataBase_after)):
            for x in range(len(DataBase_after[i])):
                if DataBase_after[i][x] in DataBase_before[i]:
                    DataBase_after_the_fact[i].remove(DataBase_after[i][x])
        # Получаем БД что записали
        # ТЕПЕРЬ ОЧИЩАЕМ ЕЕ ОТ НЕВАЛИДНЫХ ЗАПИСЕЙ

        return DataBase_after_the_fact


class DeleteValidToZero:
    """
    В Этом классе удаляем все записи у которых VALID = 0
    """
    database = []

    def __init__(self, DataBase: list):
        self.database = self._delete_to_valid(DataBase)

    def _delete_to_valid(self, database):

        collector = []
        # ПЕРЕБИРАЕМ КАЖДЫЙ ЭЛЕМЕНТ

        for i in range(len(database)):
            for x in range(len(database[i])):
                if database[i][x].get('Valid') == 0:
                    collector.append({'x': x, 'i': i})
                    print(database[i][x])
        # ТЕПЕРЬ УДАЛЯЕМ ВСЕ ЭЛЕМЕНТЫ
        print('collector', collector)
        print('database', database)
        for element in collector:

            database[element.get('i')].pop(element.get('x'))

        return database
