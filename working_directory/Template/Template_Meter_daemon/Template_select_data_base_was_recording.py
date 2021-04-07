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
        return DataBase_after_the_fact
