# Здесь прописываем Классы и конструкторы отдельных настроек settings для JSON


# Добавил пока функциями - стоит ли делать из этого составной конструктор - покажет время

# ----------------------------------------------------------------------------------------------------------------------
#                                                   GET
# ----------------------------------------------------------------------------------------------------------------------
# Голый сетинкс - нужен для GET
def form_settings_request_empty(setting):
    """
    Используется:
    в запросах GET
    ArchTypes-
    MeterIfaces
    MeterTypes
    ArchInfo
    :return:Возвращает пустое значение
    """
    if setting == None:
        return None
    else:
        settings = {}
        return dict(settings)
# ----------------------------------------------------------------------------------------------------------------------
#                                                   DELETE or GET from MeterTable
# ----------------------------------------------------------------------------------------------------------------------

# Для запроса get для MeterTable необходимо ids
def form_ids_request_MeterTable(ids):
    """
    Функция для обработки запроса IDS в таблицу MeterTable
    :param ids: Кушает любой тип - но лучше списки и кортежи
    :return: Возвращает список
    """
    if (type(ids) == list) or (type(ids) == tuple):
        return ids
    else:
        ids_list = []
        ids_list.append(ids)
        return ids_list

# ----------------------------------------------------------------------------------------------------------------------
#                                                   PUT ArchInfo
# ----------------------------------------------------------------------------------------------------------------------
# для запроса пут:
# Сначала делаем вспомогательные функции:

# Заполнение Словаря пустотой
def assembly_settings_dict_emptiness_by_PUT_ArchInfo():
    """
    Получить Пустой словарь settings для PUT_ArchInfo
    :return:отдаем пустой словарик
    """
    settings_dict = {
                    "records": None,
                     "type": None
                     }
    return settings_dict



# Сборщик dict для dict
def assembly_settings_dict_to_dict_by_PUT_ArchInfo(settings_dict:dict):
    """
    Сборщик коректного словаря для settings для PUT_ArchInfo из словаря
    Проверяет его коректность , если нет каких то полей заполянет их None
    :param settings_dict: Кушает Только словарь
    :return: отдает корректный по структуре словарь
    """
    # Делаем проверку на наличие всех коректных ключей
    actual_key = ["records", "type"]
    for i in range(len(actual_key)):
        # Если ключа не существует - делаем его
        if (actual_key[i] in settings_dict) == False:
            settings_dict[actual_key[i]] = None
    return settings_dict

# Сборщик dict для list
def assembly_settings_list_to_dict_by_PUT_ArchInfo(settings_list:list):
    """
        Сборщик коректного словаря для settings для PUT_ArchInfo из массива
        Проверяет его коректность , если нет каких то полей заполянет их None
        :param settings_list: Кушает Только list
        :return: отдает корректный по структуре словарь
        """
    # для начала проверяем длинну массива
    # если у нас массив из 2 и более элементов то первые 2 отправляются с соответсвующие значения
    if len(settings_list) > 1:
        settings_dict = {
                        "records": settings_list[0],
                        "type": settings_list[1]
                        }
    # Иначе - заполняем все пустотой
    else:
        settings_dict = assembly_settings_dict_emptiness_by_PUT_ArchInfo()
    return settings_dict


# В этой функции смотрим что нам делать, если у нас все таки массив в settings
def review_list_by_PUT_ArchInfo(settings:list):
    """
    Если ты вызываешь эту функцию - то скорее всего ты проходишься по элементам массива который содержится в setting
    Логика проста - Мы смотрим .ю содержит ли наш массив словари или массивы
    после этого - два пути -
    если есть массив или словарь, то заполянем массив словарями
    если нет - генерим словарь с первыми двумя элементами

    :param settings: Это массив по которому мы проходимся
    :return: Возвращаем тот же массив только с корректными значениями
    """
    # проходимся по всему массиву в поисках словарей и массивов. если их находим , стопаем поиск.
    presenge = False
    for i in range(len(settings)):
        # Если находим массив , то стопаем цикл
        if (type(settings[i]) == dict) or (type(settings[i]) == list) or (type(settings[i]) == tuple) :
            presenge = True
            break
    # дальше два пути - Если у нас нет массивов - берем и формируем из того что есть словарь.
    # Если есть - то из элементов формируем словарь
    if (presenge==True) :
        # Проходимся снова
        for i in range(len(settings)):
            # Если нам попадается словарь - Собираем корректный словарь
            if (type(settings[i]) == dict) :
                settings[i] = assembly_settings_dict_to_dict_by_PUT_ArchInfo(settings[i])
            # Если попадается массив, то собираем из него
            elif (type(settings[i]) == list) or (type(settings[i]) == tuple):
                settings[i] = assembly_settings_list_to_dict_by_PUT_ArchInfo(list(settings[i]))
            # Иначе - делаем пустой словарь
            else:
                settings[i] = assembly_settings_dict_emptiness_by_PUT_ArchInfo()

    else:
        # ТУт очень важно - оборачиваем все это в массив
        settings = [assembly_settings_list_to_dict_by_PUT_ArchInfo(settings)]
    return settings

# Главная функция которая собирает settings для ArchInfo
def form_settings_request_PUT_ArchInfo(settings):
    """
    Функция для обработки массива для метода PUT в таблицу ArchInfo
    :param settings: Лучше передавать массив из словарей , однако можно передать массив из других элементов
    :return: Возвращает массив из словарей
    """
    # Итак погнали: сначала делаем проверку на то - массив это или нет
    if (type(settings) == tuple) or (type(settings) == list):
        # Переводим это все в массив
        settings = list(settings)
        settings_list = review_list_by_PUT_ArchInfo(settings)
        return settings_list
    # Если у нас один словарь - проверяем его корректность и отправляем обратно в массиве -
    elif type(settings) == dict:
        settings_dict = assembly_settings_dict_to_dict_by_PUT_ArchInfo(settings)
        # Заворачиваем это в массив и возвращаем обратно
        settings_list = [settings_dict]
        return settings_list
    # Остальное - возвращает пустой массив словарей
    else:
        # делаем пустоту
        settings_dict = assembly_settings_dict_emptiness_by_PUT_ArchInfo()
        # Заворачиваем это в массив и возвращаем обратно
        settings_list = [settings_dict]
        return settings_list

# ----------------------------------------------------------------------------------------------------------------------
#                                                   POST MeterTable
# ----------------------------------------------------------------------------------------------------------------------
# Заполнение Словаря пустотой
def assembly_settings_dict_emptiness_by_POST_MeterTable():
    """
    Получить Пустой словарь settings для POST MeterTable
    :return:отдаем пустой словарик
    """
    settings_dict = {
                            "addr": None,
                            "id": None,
                            "ifaceCfg": None,
                            "ifaceName": None,
                            "pId": None,
                            "passRd": None,
                            "passWr": None,
                            "rtuFider": None,
                            "rtuObjNum": None,
                            "rtuObjType": None,
                            "type": None,
                            "typeName": None
                    }
    return settings_dict



# Сборщик dict для dict
def assembly_settings_dict_to_dict_by_POST_MeterTable(settings_dict:dict):
    """
    Сборщик коректного словаря для settings для POST MeterTable из словаря
    Проверяет его коректность , если нет каких то полей заполянет их None
    :param settings_dict: Кушает Только словарь
    :return: отдает корректный по структуре словарь
    """
    # Делаем проверку на наличие всех коректных ключей
    actual_key = [
                            "addr",
                            "id",
                            "ifaceCfg",
                            "ifaceName",
                            "pId",
                            "passRd",
                            "passWr",
                            "rtuFider",
                            "rtuObjNum",
                            "rtuObjType",
                            "type",
                            "typeName"
                    ]
    for i in range(len(actual_key)):
        # Если ключа не существует - делаем его
        if (actual_key[i] in settings_dict) == False:
            settings_dict[actual_key[i]] = None
    return settings_dict

# Сборщик dict для list
def assembly_settings_list_to_dict_by_POST_MeterTable(settings_list:list):
    """
        Сборщик коректного словаря для settings для POST MeterTable из массива
        Проверяет его коректность , если нет каких то полей заполянет их None
        :param settings_list: Кушает Только list
        :return: отдает корректный по структуре словарь
        """
    # для начала проверяем длинну массива - и если надо - удлиняем его
    while len(settings_list) < 12:
        settings_list.append(None)
    # если у нас массив из 12 и более элементов то первые 12 отправляются с соответсвующие значения
    if len(settings_list) > 11:
        settings_dict = {
                                    "addr": settings_list[0],
                                    "id": settings_list[1],
                                    "ifaceCfg":settings_list[2],
                                    "ifaceName": settings_list[3],
                                    "pId": settings_list[4],
                                    "passRd": settings_list[5],
                                    "passWr": settings_list[6],
                                    "rtuFider": settings_list[7],
                                    "rtuObjNum": settings_list[8],
                                    "rtuObjType": settings_list[9],
                                    "type": settings_list[10],
                                    "typeName": settings_list[11]
                        }
    # Иначе - заполняем все пустотой
    else:
        settings_dict = assembly_settings_dict_emptiness_by_POST_MeterTable()
    return settings_dict


# В этой функции смотрим что нам делать, если у нас все таки массив в settings
def review_list_by_POST_MeterTable(settings:list):
    """
    Если ты вызываешь эту функцию - то скорее всего ты проходишься по элементам массива который содержится в setting
    Логика проста - Мы смотрим .ю содержит ли наш массив словари или массивы
    после этого - два пути -
    если есть массив или словарь, то заполянем массив словарями
    если нет - генерим словарь с первыми двумя элементами

    :param settings: Это массив по которому мы проходимся
    :return: Возвращаем тот же массив только с корректными значениями
    """
    # проходимся по всему массиву в поисках словарей и массивов. если их находим , стопаем поиск.
    presenge = False
    for i in range(len(settings)):
        # Если находим массив , то стопаем цикл
        if (type(settings[i]) == dict) or (type(settings[i]) == list) or (type(settings[i]) == tuple) :
            presenge = True
            break
    # дальше два пути - Если у нас нет массивов - берем и формируем из того что есть словарь.
    # Если есть - то из элементов формируем словарь
    if (presenge==True) :
        # Проходимся снова
        for i in range(len(settings)):
            # Если нам попадается словарь - Собираем корректный словарь
            if (type(settings[i]) == dict) :
                settings[i] = assembly_settings_dict_to_dict_by_POST_MeterTable(settings[i])
            # Если попадается массив, то собираем из него
            elif (type(settings[i]) == list) or (type(settings[i]) == tuple):
                settings[i] = assembly_settings_list_to_dict_by_POST_MeterTable(list(settings[i]))
            # Иначе - делаем пустой словарь
            else:
                settings[i] = assembly_settings_dict_emptiness_by_POST_MeterTable()

    else:
        settings = [assembly_settings_list_to_dict_by_POST_MeterTable(settings)]
    return settings

# Главная функция которая собирает settings для MeterTable
def form_settings_request_POST_MeterTable(settings):
    """
    Функция для обработки массива для метода POST в таблицу MeterTable
    :param settings: Лучше передавать массив из словарей , однако можно передать массив из других элементов
    :return: Возвращает массив из словарей
    """
    # Итак погнали: сначала делаем проверку на то - массив это или нет
    if (type(settings) == tuple) or (type(settings) == list):
        # Переводим это все в массив
        settings = list(settings)
        settings_list = review_list_by_POST_MeterTable(settings)
        return settings_list
    # Если у нас один словарь - проверяем его корректность и отправляем обратно в массиве -
    elif type(settings) == dict:
        settings_dict = assembly_settings_dict_to_dict_by_POST_MeterTable(settings)
        # Заворачиваем это в массив и возвращаем обратно
        settings_list = [settings_dict]
        return settings_list
    # Остальное - возвращает пустой массив словарей
    else:
        # делаем пустоту
        settings_dict = assembly_settings_dict_emptiness_by_POST_MeterTable()
        # Заворачиваем это в массив и возвращаем обратно
        settings_list = [settings_dict]
        return settings_list

# ----------------------------------------------------------------------------------------------------------------------


# для запроса пост - Старая
def form_settingsrequest_POST_MeterTable(addr, id, ifaceCfg, ifaceName, pId, passRd, passWr, rtuFider,
                                         rtuObjNum, rtuObjType, type, typeName):


    settings = {"addr": addr,
                  "id": id,
                  "ifaceCfg": ifaceCfg,
                  "ifaceName": ifaceName,
                  "pId": pId,
                  "passRd": passRd,
                  "passWr": passWr,
                  "rtuFider": rtuFider,
                  "rtuObjNum": rtuObjNum,
                  "rtuObjType": rtuObjType,
                  "type": type,
                  "typeName": typeName}
    return dict(settings)

# для запроса пут
# def form_settings_request_PUT_ArchInfo(records, type):
#     settings = {"id": id
#                 }
#     return dict(settings)