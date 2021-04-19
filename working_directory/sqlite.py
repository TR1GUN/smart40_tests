import sqlite3
import configparser
from working_directory.ConfigParser import dbpath
# from ConfigParser import dbpath

# print(dbpath)

def readtable(table):
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    # c.execute("SELECT * FROM " + table)
    c.execute("SELECT DataType, MeterType, Name FROM " + table)
    table = c.fetchall()
    return table

def readArchInfo(TypeName):
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    if TypeName != '':
        c.execute("SELECT ArchInfo.Records, ArchTypes.Name AS Arch "
                  "FROM ArchInfo JOIN ArchTypes "
                  "ON ArchInfo.RecordTypeId == ArchTypes.Id "
                  "WHERE Arch = " + TypeName)
    else:
        c.execute("SELECT ArchInfo.Records, ArchTypes.Name AS Arch "
                  "FROM ArchInfo JOIN ArchTypes "
                  "ON ArchInfo.RecordTypeId == ArchTypes.Id")
    table = c.fetchall()
    return table

def readMeterTable():
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    c.execute("SELECT MeterTable.DeviceIdx, "
              "MeterTable.MeterId, "
              "MeterTable.ParentId, "
              "MeterTable.TypeId, "
              "MeterTypes.Type, "
              "MeterTable.Address, "
              "MeterTable.ReadPassword, "
              "MeterTable.WritePassword,"
              "MeterIfaces.Name, "
              "MeterTable.InterfaceConfig, "
              "MeterTable.RTUObjType, "
              "MeterTable.RTUFeederNum, "
              "MeterTable.RTUObjNum "
			  "FROM MeterTable, MeterIfaces, MeterTypes "
			  "WHERE MeterTypes.Id = MeterTable.TypeId AND MeterIfaces.Id = MeterTable.InterfaceId"
            )
    table = c.fetchall()
    return table


# ---------------------------------------------------------------------------------------------------------------
#                             Новые Функции from Belic Nico
# ---------------------------------------------------------------------------------------------------------------

#Вспомогательная функция

def dict_factory(cursor, row):
    """
    Вспомогательная функция для получения значений из таблицы ввиде dict
    ОЧЕНЬ УДОБНО ,ага

    Принимает - а хз как это обьяснить

    возвращает - даные запроса но только ввиде Dict
    :param cursor:
    :param row:
    :return:
    """
    dict = {}
    for idx, col in enumerate(cursor.description):
        dict[col[0]] = row[idx]
    return dict


def readtable_return_dict(table_name:str, collum= '*'):
    """
    функция для чтения таблиц, и выдачи результата в dict
    Таблица прописывается ручками ,
    По умолчанию извлекаются все поля
    Кушает только значения str - Имена полей перчесляем через запятую
    :param collum: - Имена полей - перечеслляем через запятую
    :param table_name: Имя Таблицы
    :return: Возвращаем результата запроса массивом в котором содержится dict
    """
    conn = sqlite3.connect(dbpath)
    conn.row_factory = dict_factory
    c = conn.cursor()
    command = 'SELECT ' + str(collum) + ' FROM ' + str(table_name)
    c.execute(command)
    table = c.fetchall()
    return table

def readtable_return_list(table_name:str, collum= '*'):
    """
    функция для чтения таблиц, и выдачи результата в tuple
    Таблица прописывается ручками ,
    По умолчанию извлекаются все поля
    Кушает только значения str - Имена полей перчесляем через запятую
    :param collum: - Имена полей - перечеслляем через запятую
    :param table_name: Имя Таблицы
    :return: Возвращаем результата запроса массивом в котором содержится dict
    """
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    command = 'SELECT ' + str(collum) + ' FROM ' + str(table_name)
    c.execute(command)
    table = c.fetchall()
    return table

def readArchInfo_return_dict(TypeName:str = ''):
    conn = sqlite3.connect(dbpath)
    conn.row_factory = dict_factory
    c = conn.cursor()
    if TypeName != '':
        c.execute("SELECT ArchInfo.Records, ArchTypes.Name AS Arch "
                  "FROM ArchInfo JOIN ArchTypes "
                  "ON ArchInfo.RecordTypeId == ArchTypes.Id "
                  "WHERE Arch = " + TypeName)
    else:
        c.execute("SELECT ArchInfo.Records, ArchTypes.Name AS Arch "
                  "FROM ArchInfo JOIN ArchTypes "
                  "ON ArchInfo.RecordTypeId == ArchTypes.Id")
    table = c.fetchall()
    return table


def readMeterTable_return_dict(ids=None):
    conn = sqlite3.connect(dbpath)
    conn.row_factory = dict_factory
    c = conn.cursor()
    if ids == None:
        c.execute('''SELECT MeterTable.DeviceIdx,
              MeterTable.MeterId, 
              MeterTable.ParentId, 
              MeterTable.TypeId, 
              MeterTypes.Type, 
              MeterTable.Address, 
              MeterTable.ReadPassword, 
              MeterTable.WritePassword,
              MeterIfaces.Name, 
              MeterTable.InterfaceConfig, 
              MeterTable.RTUObjType, 
              MeterTable.RTUFeederNum, 
              MeterTable.RTUObjNum FROM MeterTable, MeterIfaces, MeterTypes WHERE MeterTypes.Id = MeterTable.TypeId AND 
              MeterIfaces.Id = MeterTable.InterfaceId AND MeterTable.DeviceIdx;''')

    else:
        ids = tuple(ids)
        if len(ids) == 1 :
            ids = '( ' + str(ids[0]) + ' )'

        execute = '''
              SELECT MeterTable.DeviceIdx,
              MeterTable.MeterId, 
              MeterTable.ParentId, 
              MeterTable.TypeId, 
              MeterTypes.Type, 
              MeterTable.Address, 
              MeterTable.ReadPassword, 
              MeterTable.WritePassword,
              MeterIfaces.Name, 
              MeterTable.InterfaceConfig, 
              MeterTable.RTUObjType, 
              MeterTable.RTUFeederNum, 
              MeterTable.RTUObjNum FROM MeterTable, MeterIfaces, MeterTypes WHERE MeterTypes.Id = MeterTable.TypeId AND 
              MeterIfaces.Id = MeterTable.InterfaceId AND MeterTable.MeterId 
                ''' + ' IN ' + str(ids) + ''
        c.execute(execute)

    table = c.fetchall()
    c.close()
    return table

# метод который удаляет все наше творчество из MeterTable в том числе выборочно по id
def deleteMeterTable(ids = None):
    """
    Удаление из MeterTable
    :param ids: Если выставить этот параметр то будет удаленно только то , что здесь указанно
    :return:
    """

    conn = sqlite3.connect(dbpath)
    conn.isolation_level = None
    c = conn.cursor()


    # Удаляем все из БД
    execute = '''DELETE FROM MeterTable WHERE  MeterTable.MeterId'''
    if ids != None :
        ids = tuple(ids)
        execute = execute + ' IN ' + str(ids)
    elif ids == 0:
        execute = '''DELETE FROM MeterTable'''
    else:
        'PRAGMA foreign_keys = ON;'
        execute = '''DELETE FROM MeterTable  '''
        c.execute('PRAGMA foreign_keys = ON;')
        conn.commit()
        table = c.fetchall()
    c.execute(execute)
    conn.commit()
    table = c.fetchall()
    return table

# метод для записи в MeterTable

def recording_MeterTable(settings_field:list):

    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    # Теперь надо сформировать
    # Здесь прописываем нашу команду
    command = """INSERT INTO MeterTable (
                                        MeterId,     
                                        ParentId,
                                        TypeId,
                                        Address,
                                        ReadPassword,
                                        WritePassword,
                                        InterfaceId,
                                        InterfaceConfig, 
                                        RTUObjType, 
                                        RTUFeederNum, 
                                        RTUObjNum )
                                                VALUES """
    command_field = ''
    for i in range(len(settings_field)):
        settings_field[i] = tuple(settings_field[i])
        command_field = command_field + str(settings_field[i]) + ' , '
    command = command + command_field[:-2]
    c.execute(command)
    conn.commit()
    table = c.fetchall()

def updateArchInfo_for_stoc():
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    c.execute("""UPDATE ArchInfo
                                SET Records = 10000 """)
    table = c.fetchall()

def execute_list_command_to_read_return_dict(command:list):
    """
    Универсальная Функция для чтения
    Выполняет какую то команду
    Это важно !!!

    :param command: Собсна переменная команды которую надо исполнить
    :return: Сюда результат выполнения этой команды , только в словаре
    """
    conn = sqlite3.connect(dbpath)
    conn.row_factory = dict_factory
    c = conn.cursor()
    table_list = []
    for i in range(len(command)):
        c.execute(command[i])
        table_list.append(c.fetchall())
    # table = c.fetchall()
    c.close()
    return table_list


def execute_command_to_read_return_dict(command:str):
    """
    Универсальная Функция для чтения
    Выполняет какую то команду
    Это важно !!!

    :param command: Собсна переменная команды которую надо исполнить - пихать в str
    :return: Сюда результат выполнения этой команды , только в словаре
    """
    conn = sqlite3.connect(dbpath)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(command)
    table = c.fetchall()
    c.close()
    return table


def execute_selected_to_view_return_dict(command_create_view:list,command_delete_view:list,command_select :str or list):
    """
    Специальная функция для того чтоб создавать прелставления , затем селектить нужные данные из нее ,
    а после этого удалять представления и возвращать результат селекта

    :param command_create_view:  Сюда список из команд создания представления
    :param command_delete_view: Сюда список чтоб их дропать
    :param command_select: сюда стрингу чтоб селектить.
    :return: возвращает результат селекта
    """
    conn = sqlite3.connect(dbpath)
    conn.row_factory = dict_factory
    c = conn.cursor()
    table = []
    table_list = []
    # # Удаляем если что то есть
    try:
        for i in range(len(command_delete_view)):
            c.execute(command_delete_view[i])
            table_list.append(c.fetchall())
    except:
        # print('Временные таблицы не создавались')
        pass

    for i in range(len(command_create_view)):
        print('Команда', command_create_view[i])
        c.execute(command_create_view[i])
        table_list.append(c.fetchall())
        print(table_list)

    if len(table_list) != 0:
        # Отрабатываем для стринговой команды
        if type(command_select) == str:
            c.execute(command_select)
            table = c.fetchall()
        # а теперь отрабатываем для списка команд
        else:
            table = []
            for i in range(len(command_select)):
                # print('Команда', command_select[i])
                c.execute(command_select[i])
                table_element = c.fetchall()
                # print('Результат ',table_element)
                table = table + table_element

    for i in range(len(command_delete_view)):
        c.execute(command_delete_view[i])
        table_list.append(c.fetchall())
        conn.commit()
    c.close()
    return table


def execute_command_to_write_return_dict(command:str):
    """
    Универсальная Функция для Записи нужнйо комнате
    Выполняет какую то команду
    Это важно !!!

    :param command: Собсна переменная команды которую надо исполнить - пихать в str
    :return: Сюда результат выполнения этой команды , только в словаре
    """

    conn = sqlite3.connect(dbpath)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(command)
    conn.commit()
    table = c.fetchall()
    c.close()
    return table

def execute_command_values_to_write_return_dict(command:str, values:tuple):
    """
    Универсальная Функция для Записи нужнйо комнате
    Выполняет какую то команду
    Это важно !!!

    :param command: Собсна переменная команды которую надо исполнить - пихать в str
    :return: Сюда результат выполнения этой команды , только в словаре
    """
    conn = sqlite3.connect(dbpath)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute(command, values)
    conn.commit()
    table = c.fetchall()
    c.close()
    return table


def execute_selected_to_try_except(command:str):
    """
    Эксперементальная функция для создания временных таблиц и последующего удаленния онной.
    Вот атк бывает в жизни.

    :param command:
    :return:
    """
    conn = sqlite3.connect(dbpath)
    conn.row_factory = dict_factory
    c = conn.cursor()
    try:
        c.execute(command)
        conn.commit()
        table = c.fetchall()
    except:
        table = []
    finally:
        return table