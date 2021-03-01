
# Родительский Класс для формирования начальных JSON с конкретными настройками


# Класс для формирования Пустого JSON - от него все наследуется
class TemplateEmptyJSON:
    """
    Шаблон ПУСТОГО JSON - От него Все пляшем.

    Структура JSON -
    "method": выполянемый метод ,
    "table": таблица к которой обращаются,
    "settings": настройки ,
    "ids": ид - нужно для запросов к некоторым таблицам
    """
    # Сама переменная с которой будем работать - здесь оставляем пустыми значения

    TemplateJSON = {"method": None, "table": None, "settings": None, "ids": None }

    # Конструктор - понадобится чуть позже
    def __init__(self):
        self.TemplateJSON = {"method": None, "table": None, "settings": None, "ids": None }
