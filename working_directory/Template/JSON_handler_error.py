# Здесь будет располагаться обработчик ошибок для JSON которые нам могут встречтатся при получении JSON

# Функция обработчик
def error_handler(JSON_dict:dict):
    """
    Функция обработчик ошибок

    Пока что возвращает только settings если res = 0

    Добавлена обработка значения None вместо массива settings
    :param JSON_dict:
    :return:
    """
    res = JSON_dict['res']
    if res == 0:
        # Если не содержит settings
        if 'settings' not in JSON_dict.keys():
            JSON_dict['settings'] = []
        # добавляем проверку на None
        if JSON_dict['settings'] == None:
            JSON_dict['settings'] = []
        return JSON_dict['settings']
    else:
        return JSON_dict['res'];

def parse_id_from_json(JSON):
    # для таблицы MeterTable:
    if JSON['table'] == 'MeterTable':
        settings_list = JSON['settings']
        id_list = []
        for i in range(len(settings_list)):
               # добавляем массив
            id_list.append(settings_list[i]["id"])
        return tuple(id_list)
