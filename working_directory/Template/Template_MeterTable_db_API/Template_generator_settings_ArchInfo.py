# Здесь Находится генератор для Settings для таблицы ArchInfo
from random import randint
from working_directory import sqlite


class GeneratorForSettingsArchInfo():
    """
    генератор для Settings для таблицы ArchInfo
    """
    ArchTypesName_list = []
    total_settings_list = []
    total_settings_list_copy = []

    def __init__(self, count_settings: int = 3 ):
        self.total_settings_list = []

        #для генерации поля type все сложнее:
        # сначала селектим все возможные значения для этого поля
        ArchTypesName_dict = sqlite.readtable_return_dict(table_name='ArchTypes' , collum='Id, Name')
        ArchInfoRecords = sqlite.readtable_return_dict(table_name='ArchInfo' , collum='Records')
        self.ArchInfoRecords_list = []
        for i in range(len(ArchInfoRecords)):
            self.ArchInfoRecords_list.append(ArchInfoRecords[i]['Records'])
        # теперь формируем из всех значений этого поля массив
        # for i in range(len(ArchTypesName_dict)):
        #     self.ArchTypesName_list.append(ArchTypesName_dict[i]['Name'])
        # Здесь следим за руками - Максимальное число генераций НЕ ДОЛЖНО привышать количества устройств - это важно
        if count_settings <= len(ArchTypesName_dict):

            # а теперь генерируем поле что нам нужно
            for i in range(count_settings):

                ArchTypesName_list_index = randint(0, (len(ArchTypesName_dict)-1))
                # нам надо сгенерировать два поля
                settings_dict = {}
                # Поле records
                settings_dict['records'] = self.__generate_record()

                # Поле type
                settings_dict['type'] = ArchTypesName_dict[ArchTypesName_list_index]['Name']
                settings_dict['Id'] = ArchTypesName_dict[ArchTypesName_list_index]['Id']

                # Ну и в конце - добавляем в наш список
                self.total_settings_list.append(settings_dict)
                # после чего удаляем его во избежании повторения
                del ArchTypesName_dict[ArchTypesName_list_index]


        else:
            self.total_settings_list = None
        # Теперь Важный момент - отсортируем по ид наш список- это важно
        self.total_settings_list = sorted(self.total_settings_list,key= lambda k: k ['Id'], reverse=False)

            # НУЖНО БУДЕТ ПОТОМ ДЛЯ НЕГАТИВНЫХ ТЕСТОВ
        # self.total_settings_list.append({'records': 324, 'type': 'ElJrnlLimPwrQM', 'Id': 57})
        # self.total_settings_list.append({'type': 'ElConfig', 'records': 0, 'Id': 1})

    def __generate_record(self):
        """
        Здесь генерируем УНИКАЛЬНУЮ запись
        :return:
        """
        record = randint(1, 9999)
        if record in self.ArchInfoRecords_list:
            while record not in self.ArchInfoRecords_list:
                record = randint(1, 9999)
        return record

    def get_dict(self):
        """
        Получить список словарей чтоб можно было красиво с ними работать
        :return:
        """
        total_settings_list = self.total_settings_list.copy()
        return total_settings_list

    def get_dict_without_id(self):
        """
        Получить список сгенерированных словарей БЕЗ поля ID
        :return:
        """
        total_settings_list_copy = self.total_settings_list.copy()
        settings_list_without_id = []
        for i in range(len(total_settings_list_copy)):
            dict_without_id = {}
            dict_without_id['type']= total_settings_list_copy[i]['type']
            dict_without_id['records'] = total_settings_list_copy[i]['records']
            settings_list_without_id.append(dict_without_id)


        return settings_list_without_id


    def get_list_for_db(self):
        """
        Получить список списков чтоб можно было красиво с ними работать
        :return:
        """
        list_for_db = []
        for i in range(len(self.total_settings_list)):
            list_for_db.append([self.total_settings_list[i]['Id'] ,self.total_settings_list[i]['records']])

        return list_for_db

