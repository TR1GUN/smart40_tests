# Дочерние Классы для формирования начальных JSON с конкретными настройками поля method

# Используется родительский класс из Template_empty_JSON

# наследуются от пустого JSON
from working_directory.Template.Template_MeterTable_db_API.Template_empty_JSON import TemplateEmptyJSON


# Класс для GET запроса
class Template_GET_JSON(TemplateEmptyJSON):
    """
    Класс сборщик GET запроса
    Наследник TemplateEmptyJSON

    Содержит единственное поле _TemplateJSON

    Здесь переопределяется значение атрибута method

    Остальное - Пустое

    """
    TemplateJSON = {}
    TemplateJSON["method"] = 'get'

    def __init__(self):
        self.TemplateJSON = {}
        self.TemplateJSON["method"] = 'get'


# Класс для POST запроса
class Template_POST_JSON(TemplateEmptyJSON):
    """
    Класс сборщик POST запроса
    Наследник TemplateEmptyJSON

    Содержит единственное поле _TemplateJSON

    Здесь переопределяется значение атрибута method

    Остальное - Пустое


    """
    TemplateJSON = {}
    TemplateJSON["method"] = 'post'

    def __init__(self):
        self.TemplateJSON = {}
        self.TemplateJSON["method"] = 'post'


# Класс для PUT запроса
class Template_PUT_JSON(TemplateEmptyJSON):
    """
    Класс сборщик PUT запроса
    Наследник TemplateEmptyJSON

    Содержит единственное поле _TemplateJSON

    Здесь переопределяется значение атрибута method

    Остальное - Пустое


    """
    TemplateJSON = {}
    TemplateJSON["method"] = 'put'

    def __init__(self):
        self.TemplateJSON = {}
        self.TemplateJSON["method"] = 'put'


# Класс для DELETE запроса
class Template_DELETE_JSON(TemplateEmptyJSON):
    """
    Класс сборщик DELETE запроса
    Наследник TemplateEmptyJSON

    Содержит единственное поле _TemplateJSON

    Здесь переопределяется значение атрибута method

    Остальное - Пустое


    """
    TemplateJSON = {}
    TemplateJSON["method"] = 'delete'

    def __init__(self):
        self.TemplateJSON = {}
        self.TemplateJSON["method"] = 'delete'



