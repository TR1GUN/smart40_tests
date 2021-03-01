# Дочерние Классы для формирования начальных JSON с конкретными настройками поля table

# Используется родительский класс из Template_method_JSON, а для него нужен Template_empty_JSON

from working_directory.Template.Template_MeterTable_db_API.Template_empty_JSON import TemplateEmptyJSON

# Класс для таблицы ArchTypes
class Template_ArchTypes_JSON(TemplateEmptyJSON):
    """
    Класс сборщик для таблицы ArchTypes
    Наследник TemplateEmptyJSON

    Содержит единственное поле TemplateJSON

    Здесь переопределяется значение атрибута table

    Остальное - Пустое
    """
    TemplateJSON = {}
    TemplateJSON["table"] = 'ArchTypes'

    def __init__(self):
        self.TemplateJSON = {}
        self.TemplateJSON["table"] = 'ArchTypes'

# Класс для таблицы MeterIfaces
class Template_MeterIfaces_JSON(TemplateEmptyJSON):
    """
    Класс сборщик для таблицы MeterIfaces
    Наследник TemplateEmptyJSON

    Содержит единственное поле TemplateJSON

    Здесь переопределяется значение атрибута table

    Остальное - Пустое
    """
    TemplateJSON = {}
    TemplateJSON["table"] = 'MeterIfaces'

    def __init__(self):
        self.TemplateJSON = {}
        self.TemplateJSON["table"] = 'MeterIfaces'

# Класс для таблицы MeterTypes
class Template_MeterTypes_JSON(TemplateEmptyJSON):
    """
    Класс сборщик для таблицы MeterTypes
    Наследник TemplateEmptyJSON

    Содержит единственное поле TemplateJSON

    Здесь переопределяется значение атрибута table

    Остальное - Пустое
    """
    TemplateJSON = {}
    TemplateJSON["table"] = 'MeterTypes'

    def __init__(self):
        self.TemplateJSON = {}
        self.TemplateJSON["table"] = 'MeterTypes'

# Класс для таблицы ArchInfo
class Template_ArchInfo_JSON(TemplateEmptyJSON):
    """
    Класс сборщик для таблицы ArchInfo
    Наследник TemplateEmptyJSON

    Содержит единственное поле TemplateJSON

    Здесь переопределяется значение атрибута table

    Остальное - Пустое
    """
    TemplateJSON = {}
    TemplateJSON["table"] = 'ArchInfo'

    def __init__(self):
        self.TemplateJSON = {}
        self.TemplateJSON["table"] = 'ArchInfo'


# Класс для таблицы MeterTable
class Template_MeterTable_JSON(TemplateEmptyJSON):
    """
    Класс сборщик для таблицы MeterTable
    Наследник TemplateEmptyJSON

    Содержит единственное поле TemplateJSON

    Здесь переопределяется значение атрибута table

    Остальное - Пустое
    """
    TemplateJSON = {}
    TemplateJSON["table"] = 'MeterTable'

    def __init__(self):
        self.TemplateJSON = {}
        self.TemplateJSON["table"] = 'MeterTable'

