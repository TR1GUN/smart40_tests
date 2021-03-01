# Здесь расположим сборщик JSON из всех тех объектов что есть для соответсвуйющей API


from working_directory.Template.Template_MeterTable_db_API.Template_method_JSON import Template_GET_JSON, Template_POST_JSON
import json


# ----------------------------------------------------------------------------------------------------------------------
#                                                   GET
# ----------------------------------------------------------------------------------------------------------------------
class GET:
    """
    Класс-cборщик JSON для работы с методом GET
    """
    JSON = {}

    def __init__(self, measures=None):
        self.JSON = {}
        self.JSON_dict = {}
        self.JSON = self.collector(measures=measures)

    def collector(self, measures=None):
        """Дополнительных параметры НУЖНО выставить в measures"""
        JSON = {}
        if type(measures) == dict:
            # Формируем массив
            JSON = measures
            # Дергаем Метод
            JSON["method"] = Template_GET_JSON().TemplateJSON["method"]
            # проверям  measures
            self.JSON_dict = JSON
        # Преобразовываем в JSON
        JSON = json.dumps(JSON)
        return JSON

    def get_JSON_dict(self):

        return self.JSON_dict


# ----------------------------------------------------------------------------------------------------------------------
#                                              POST
# ----------------------------------------------------------------------------------------------------------------------
class POST:
    """
    Класс-cборщик JSON для работы с методом POST
    """

    JSON = {}
    JSON_dict = {}

    def __init__(self,measures=None):
        self.JSON = {}
        self.JSON_dict = {}
        self.JSON = self.collector(measures=measures)

    def collector(self, measures=None):
        """Дополнительных параметры НУЖНО выставить в measures"""
        # Формируем массив
        JSON = {}
        # Дергаем Метод
        JSON["method"] = Template_POST_JSON().TemplateJSON["method"]
        # проверям  measures
        if type(measures) == list:
            JSON["measures"] = measures
        # если не задан measures то ставим в ноль
        else:
            JSON["measures"] = None

        self.JSON_dict = JSON
        # Преобразовываем в JSON
        JSON = json.dumps(JSON)
        return JSON

    def get_JSON_dict(self):

        return self.JSON_dict