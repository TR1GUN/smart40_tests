# Здесь Находится генератор для Settings для таблицы MeterTable
from random import randint
from working_directory import sqlite


class GeneratorForSettingsMeterTable():

    def __init__(self, count_settings:int = 3):
        """
        Генератор Конструктор для MeterTable
        В конструкторе Генерируем нужные поля

        :param count_settings: Сюда передавать сколько JSON мы хотим получить , по умолчанию получаем 3
        """

        self.InterfaceConfig = ['9600,8n1','qwe']
        self.total_settings_list =[]
        select_max = self.__select_max()
        if type(select_max) == int:
            select_max = self.__select_max() + 1
        else :
            select_max = 1000
        # мы генерируем n количесиво раз dict который будет содержать нужные поля
        for i in range(count_settings):
            settings_dict = {}
            # нам понадобится :
            Interface = self.__get_random_dict(self.__get_Interface())
            MeterTypes = self.__get_random_dict(self.__get_MeterTypes())
            # Индекс - Первичный ключ - не парсится
            settings_dict['index'] = 'None'
            # MeterId - уникальная
            settings_dict['id'] = select_max + i
            # ParentId
            settings_dict['pId'] = 0
            # Селектим
            settings_dict['type'] = MeterTypes['Id']
            # Селектим
            settings_dict['typeName'] = MeterTypes['Type']
            # Address -
            settings_dict['addr'] = 'asd'
            # ReadPassword
            settings_dict['passRd'] = 'asd'
            # WritePassword
            settings_dict['passWr'] = '432'
            # Name  - InterfaceID  Селектим
            settings_dict['InterfaceID'] = Interface['Id']
            settings_dict['ifaceName'] = Interface['Name']
            # Поле InterfaceConfig
            settings_dict['ifaceCfg'] = self.InterfaceConfig[randint(0,1)]
            # РТУ - НАдо потом допилить - пока выставляем значения по умолчанию
            settings_dict['rtuObjType'] = 1
            settings_dict['rtuFider'] = 0
            settings_dict['rtuObjNum'] = 0

        # И в самом конце берем - и добавляем нужное нам
            self.total_settings_list.append(settings_dict)

    def __get_Interface(self):
        # селектим всю базу
        MeterIfaces_dict  = sqlite.readtable_return_dict(table_name='MeterIfaces')
        return MeterIfaces_dict

    def __get_random_dict(self, Meter_list):
        '''
        Генерим из запроса нужный рандомной словарик из списка что выдает нам селект

        :param Meter_list: Сюда пихаем лист нашего запрса
        :return: получем рандомный жэлемент словаря
        '''

        Meter_list_len = len(Meter_list)-1
        # рандомим нужный нам dict
        Meter_dict = Meter_list[randint(0, Meter_list_len)]
        return Meter_dict

    def __get_MeterTypes(self):
        # селектим всю базу
        MeterTypes_dict  = sqlite.readtable_return_dict(table_name='MeterTypes')
        return MeterTypes_dict

    def get_dict(self):
        """
        Получить список словарей чтоб можно было красиво с ними работать
        :return:
        """
        # Проходимся по всему массиву и удаляем лишние ключи
        total_settings_list = self.total_settings_list
        settings_list =[]
        for i in range(len(total_settings_list)):
            settings_dict = {
                'id': total_settings_list[i]['id'],
                'pId': total_settings_list[i]['pId'],
                'type': total_settings_list[i]['type'],
                'typeName': total_settings_list[i]['typeName'],
                'addr': total_settings_list[i]['addr'],
                'passRd': total_settings_list[i]['passRd'],
                'passWr': total_settings_list[i]['passWr'],
                'ifaceName': total_settings_list[i]['ifaceName'],
                'ifaceCfg': total_settings_list[i]['ifaceCfg'],
                'rtuObjType': total_settings_list[i]['rtuObjType'],
                'rtuFider': total_settings_list[i]['rtuFider'],
                'rtuObjNum': total_settings_list[i]['rtuObjNum'],
                            }
            settings_list.append(settings_dict)

        return settings_list
    def get_tuple(self):
        """
        Получить список кортежей для того чтоб можно было инсертить в БД
        :return:
        """
        # Составляем наш кортеж для записи в БД
        total_settings_list = self.total_settings_list
        total_settings_list_new = []
        for i in range(len(total_settings_list)):
            total_settings_tuple = (total_settings_list[i]['id'],
                                    total_settings_list[i]['pId'],
                                    total_settings_list[i]['type'],
                                    total_settings_list[i]['addr'],
                                    total_settings_list[i]['passRd'],
                                    total_settings_list[i]['passWr'],
                                    total_settings_list[i]['InterfaceID'],
                                    total_settings_list[i]['ifaceCfg'],
                                    total_settings_list[i]['rtuObjType'],
                                    total_settings_list[i]['rtuFider'],
                                    total_settings_list[i]['rtuObjNum']
                                    )
            total_settings_list_new.append(total_settings_tuple)
        return total_settings_list_new

    def get_ids(self):
        """
        В этом методе получаем список IDS
        :return:
        """
        total_ids_list = self.total_settings_list
        total_ids_list_new = []
        for i in range(len(total_ids_list)):
            total_ids_list_new.append(total_ids_list[i]['id'])
        return total_ids_list_new

    def __select_max(self):
        max_value = sqlite.readtable_return_dict(collum='max(MeterId)' , table_name='MeterTable')
        if len(max_value) > 0:
            max_value = max_value[0]['max(MeterId)']
        else:
            max_value = 0
        return max_value

    def get_id_to_delete(self, count:int = 0):
        """
        Здесь мы делаем выборку из тех ID которые хотим удалить
        :param count: Кушает число ID которые летят в удаление
        :return: возвращает нужное колличество ID которые полетят в удаление
        """
        # сначала получаем список всех сгенерированных ID

        ids_set = self.get_ids()
        ids_set_len = len(ids_set)
        ids_list = []

        # Если мы поставили count = 0 , то возвращаем пустоту!
        if count == 0:
            return None
        else:
            # После чего проверяем на корректность значение
            if count <= ids_set_len:
                # теперь делаем из них рандомную выборку
                for i in range(count):
                    x = randint(0, (len(ids_set)-1))
                    element = ids_set.pop(x)
                    ids_list.append(element)

                return (ids_list)
            else:
                return None

    def get_JSON_setting_Format_to_DB(self):
        """
        здесь конструктор для передачи settings что в JSON в формате который кушает БД
        :return:
        """
        total_settings_list = self.total_settings_list
        total_settings_list_new = []
        for i in range(len(total_settings_list)):
            total_settings_dict = {
                                    'MeterId': total_settings_list[i]['id'],
                                    'ParentId': total_settings_list[i]['pId'],
                                    'TypeId': total_settings_list[i]['type'],

                                    'Type': total_settings_list[i]['typeName'],
                                    'Address': total_settings_list[i]['addr'],
                                    'ReadPassword': total_settings_list[i]['passRd'],
                                    'WritePassword': total_settings_list[i]['passWr'],

                                    'Name': total_settings_list[i]['ifaceName'],
                                    'InterfaceID': total_settings_list[i]['InterfaceID'],
                                    'InterfaceConfig': total_settings_list[i]['ifaceCfg'],
                                    'RTUObjType': total_settings_list[i]['rtuObjType'],
                                    'RTUFeederNum': total_settings_list[i]['rtuFider'],
                                    'RTUObjNum': total_settings_list[i]['rtuObjNum']

                                    }
            total_settings_list_new.append(total_settings_dict)
        return total_settings_list_new
