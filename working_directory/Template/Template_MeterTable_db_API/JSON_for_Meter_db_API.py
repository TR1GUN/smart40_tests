# Здесь расположим сборщик JSON из всех тех объектов что есть

from working_directory.Template.Template_MeterTable_db_API import Template_settings_JSON
import json
from working_directory.Template.Template_MeterTable_db_API.Template_table_JSON import \
    Template_ArchTypes_JSON,\
    Template_MeterIfaces_JSON, \
    Template_MeterTable_JSON,\
    Template_ArchInfo_JSON,\
    Template_MeterTypes_JSON
from working_directory.Template.Template_MeterTable_db_API.Template_method_JSON import Template_GET_JSON,Template_POST_JSON,Template_PUT_JSON,Template_DELETE_JSON


# ----------------------------------------------------------------------------------------------------------------------
#                                                   GET
# ----------------------------------------------------------------------------------------------------------------------
class GET():
    """
    Класс-cборщик JSON для работы с методом GET
    """

    def __init__(self):
        pass

    # Дёргаем таблицу ArchTypes
    @staticmethod
    def ArchTypes(setting = None, ids = None):
        """Дополнительных параметров не надо"""
        # Формируем массив
        JSON = {}
        # Дергаем Метод
        JSON["method"] = Template_GET_JSON().TemplateJSON["method"]
        # Дергаем Нужную таблицу
        JSON["table"] = Template_ArchTypes_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            JSON["settings"] = Template_settings_JSON.settings_GET_all_table(setting = setting)
        # тоже самое делаем и с ids
        if ids != None:
            JSON["ids"] = None
        # Преобразовываем в JSON
        JSON = json.dumps(JSON)
        return JSON

    @staticmethod
    def MeterIfaces(setting=None, ids=None):
        """Дополнительных параметров не надо"""
        # Формируем массив
        JSON = {}
        # Дергаем Метод
        JSON["method"] = Template_GET_JSON().TemplateJSON["method"]
        # Дергаем Нужную таблицу
        JSON["table"] = Template_MeterIfaces_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            JSON["settings"] = Template_settings_JSON.settings_GET_all_table(setting = setting)
        # тоже самое делаем и с ids
        if ids != None:
            JSON["ids"] = None
        # Преобразовываем в JSON
        JSON = json.dumps(JSON)
        return JSON

    @staticmethod
    def MeterTypes(setting=None, ids=None):
        """Дополнительных параметров не надо"""
        # Формируем массив
        JSON = {}
        # Дергаем Метод
        JSON["method"] = Template_GET_JSON().TemplateJSON["method"]
        # Дергаем Нужную таблицу
        JSON["table"] = Template_MeterTypes_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            JSON["settings"] = Template_settings_JSON.settings_GET_all_table(setting = setting)
        # тоже самое делаем и с ids
        if ids != None:
            JSON["ids"] = None
        # Преобразовываем в JSON
        JSON = json.dumps(JSON)
        return JSON

    @staticmethod
    def ArchInfo(setting=None, ids=None):
        """Дополнительных параметров не надо"""
        # Формируем массив
        JSON = {}
        # Дергаем Метод
        JSON["method"] = Template_GET_JSON().TemplateJSON["method"]
        # Дергаем Нужную таблицу
        JSON["table"] = Template_ArchInfo_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            JSON["settings"] = Template_settings_JSON.settings_GET_all_table(setting = setting)
        # тоже самое делаем и с ids
        if ids != None:
            JSON["ids"] = None
        # Преобразовываем в JSON
        JSON = json.dumps(JSON)
        return JSON

    @staticmethod
    def MeterTable(setting=None, ids=None):
        """Дополнительных параметры можно выставить в ids"""
        # Формируем массив
        JSON = {}
        # Дергаем Метод
        JSON["method"] = Template_GET_JSON().TemplateJSON["method"]
        # Дергаем Нужную таблицу
        JSON["table"] = Template_MeterTable_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            JSON["settings"] = Template_settings_JSON.settings_GET_all_table(setting=setting)
        # тоже самое делаем и с ids
        if ids != None:
            JSON["ids"] = Template_settings_JSON.ids_GET_MeterTable(ids=ids)
        # Преобразовываем в JSON
        JSON = json.dumps(JSON)
        return JSON


# ----------------------------------------------------------------------------------------------------------------------
#                                              POST
# ----------------------------------------------------------------------------------------------------------------------
class POST():
    """
    Класс-cборщик JSON для работы с методом POST
    """

    def __init__(self):
        pass

    # Дёргаем таблицу ArchTypes
    @staticmethod
    def ArchTypes(setting = None, ids = None):
        """Здесь Ничего не происходит"""
        pass

    @staticmethod
    def MeterIfaces(setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    @staticmethod
    def MeterTypes(setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    @staticmethod
    def ArchInfo(setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    @staticmethod
    def MeterTable(setting, ids=None):
        """Дополнительных параметры НУЖНО выставить в setting"""
        # Формируем массив
        JSON = {}
        # Дергаем Метод
        JSON["method"] = Template_POST_JSON().TemplateJSON["method"]
        # Дергаем Нужную таблицу
        JSON["table"] = Template_MeterTable_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            JSON["settings"] = Template_settings_JSON.settings_POST_MeterTable(settings=setting)
        # тоже самое делаем и с ids
        if ids != None:
            JSON["ids"] = Template_settings_JSON.ids_GET_MeterTable(ids=ids)
        # Преобразовываем в JSON
        JSON = json.dumps(JSON)
        return JSON


# ----------------------------------------------------------------------------------------------------------------------
#                                              PUT
# ----------------------------------------------------------------------------------------------------------------------
class PUT():
    """
    Класс-cборщик JSON для работы с методом PUT
    """

    def __init__(self):
        pass

    # Дёргаем таблицу ArchTypes
    @staticmethod
    def ArchTypes(setting = None, ids = None):
        """Здесь Ничего не происходит"""
        pass

    @staticmethod
    def MeterIfaces(setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    @staticmethod
    def MeterTypes(setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    @staticmethod
    def ArchInfo(setting, ids=None):
        """Дополнительных параметры НУЖНО выставить в setting"""
        # Формируем массив
        JSON = {}
        # Дергаем Метод
        JSON["method"] = Template_PUT_JSON().TemplateJSON["method"]
        # Дергаем Нужную таблицу
        JSON["table"] = Template_ArchInfo_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            JSON["settings"] = Template_settings_JSON.settings_PUT_ArchInfo(settings=setting)
        # тоже самое делаем и с ids
        if ids != None:
            JSON["ids"] = None
        # Преобразовываем в JSON
        JSON = json.dumps(JSON)
        return JSON

    @staticmethod
    def MeterTable(setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass


# ----------------------------------------------------------------------------------------------------------------------
#                                              DELETE
# ----------------------------------------------------------------------------------------------------------------------
class DELETE():
    """
    Класс-cборщик JSON для работы с методом DELETE
    """

    def __init__(self):
        pass

    # Дёргаем таблицу ArchTypes
    @staticmethod
    def ArchTypes(setting = None, ids = None):
        """Здесь Ничего не происходит"""
        pass

    @staticmethod
    def MeterIfaces(setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    @staticmethod
    def MeterTypes(setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    @staticmethod
    def ArchInfo(setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    @staticmethod
    def MeterTable(setting=None, ids=None):
        """Дополнительных параметры можно выставить в ids"""
        # Формируем массив
        JSON = {}
        # Дергаем Метод
        JSON["method"] = Template_DELETE_JSON().TemplateJSON["method"]
        # Дергаем Нужную таблицу
        JSON["table"] = Template_MeterTable_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            JSON["settings"] = Template_settings_JSON.settings_GET_all_table(setting=setting)
        # тоже самое делаем и с ids
        if ids != None:
            JSON["ids"] = Template_settings_JSON.ids_DELETE_MeterTable(ids=ids)
        # Преобразовываем в JSON
        JSON = json.dumps(JSON)
        return JSON
