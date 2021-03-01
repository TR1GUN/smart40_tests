# Здесь расположим сборщик JSON который нужен для Meter DBиз всех тех объектов что есть

from working_directory.Template.Template_MeterTable_db_API import Template_settings_JSON
import json
from working_directory.Template.Template_MeterTable_db_API.Template_table_JSON import \
    Template_ArchTypes_JSON,\
    Template_MeterIfaces_JSON, \
    Template_MeterTable_JSON,\
    Template_ArchInfo_JSON,\
    Template_MeterTypes_JSON
from working_directory.Template.Template_MeterTable_db_API.Template_method_JSON import Template_GET_JSON,\
                                                            Template_POST_JSON,\
                                                            Template_PUT_JSON,\
                                                            Template_DELETE_JSON


# ----------------------------------------------------------------------------------------------------------------------
#                                                   GET
# ----------------------------------------------------------------------------------------------------------------------
class GET():
    """
    Класс для работы с методом GET
    """
    JSON = {"method":"get"}

    # Сборщик работает просто - Собираем нужный нам метод
    def __init__(self):
        self.JSON["method"] = Template_GET_JSON().TemplateJSON["method"]
    # Дёргаем таблицу ArchTypes
    def ArchTypes(self, setting = None, ids = None):
        """Дополнительных параметров не надо"""
        # Дергаем Нужную таблицу
        self.JSON["table"] = Template_ArchTypes_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            self.JSON["settings"] = Template_settings_JSON.settings_GET_all_table(setting = setting)
        # тоже самое делаем и с ids
        if ids != None:
            self.JSON["ids"] = None
        # Преобразовываем в JSON
        self.JSON = json.dumps(self.JSON)
        return self.JSON

    def MeterIfaces(self, setting=None, ids=None):
        """Дополнительных параметров не надо"""
        # Формируем массив

        # Дергаем Нужную таблицу
        self.JSON["table"] = Template_MeterIfaces_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            self.JSON["settings"] = Template_settings_JSON.settings_GET_all_table(setting = setting)
        # тоже самое делаем и с ids
        if ids != None:
            self.JSON["ids"] = None
        # Преобразовываем в JSON
        JSON = json.dumps(self.JSON)
        return JSON

    def MeterTypes(self, setting=None, ids=None):
        """Дополнительных параметров не надо"""
        # Дергаем Нужную таблицу
        self.JSON["table"] = Template_MeterTypes_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            self.JSON["settings"] = Template_settings_JSON.settings_GET_all_table(setting = setting)
        # тоже самое делаем и с ids
        if ids != None:
            self.JSON["ids"] = None
        # Преобразовываем в JSON
        self.JSON = json.dumps(self.JSON)
        return self.JSON

    def ArchInfo(self, setting=None, ids=None):
        """Дополнительных параметров не надо"""

        # Дергаем Нужную таблицу
        self.JSON["table"] = Template_ArchInfo_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            self.JSON["settings"] = Template_settings_JSON.settings_GET_all_table(setting = setting)
        # тоже самое делаем и с ids
        if ids != None:
            self.JSON["ids"] = None
        # Преобразовываем в JSON
        self.JSON = json.dumps(self.JSON)
        return self.JSON

    def MeterTable(self, setting=None, ids=None):
        """Дополнительных параметры можно выставить в ids"""

        # Дергаем Нужную таблицу
        self.JSON["table"] = Template_MeterTable_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            self.JSON["settings"] = Template_settings_JSON.settings_GET_all_table(setting=setting)
        # тоже самое делаем и с ids
        if ids != None:
            self.JSON["ids"] = Template_settings_JSON.ids_GET_MeterTable(ids=ids)
        # Преобразовываем в JSON
        self.JSON = json.dumps(self.JSON)
        return self.JSON


# ----------------------------------------------------------------------------------------------------------------------
#                                              POST
# ----------------------------------------------------------------------------------------------------------------------
class POST():
    """
    Класс для работы с методом POST
    """
    # Формируем массив
    JSON = {"method":'post'}
    def __init__(self):
        # Дергаем Метод
        self.JSON["method"] = Template_POST_JSON().TemplateJSON["method"]

    # Дёргаем таблицу ArchTypes
    def ArchTypes(self, setting = None, ids = None):
        """Здесь Ничего не происходит"""
        pass

    def MeterIfaces(self, setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    def MeterTypes(self, setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    def ArchInfo(self, setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    def MeterTable(self, setting, ids=None):
        """Дополнительных параметры НУЖНО выставить в setting"""

        # Дергаем Нужную таблицу
        self.JSON["table"] = Template_MeterTable_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            self.JSON["settings"] = Template_settings_JSON.settings_POST_MeterTable(settings=setting)
        # тоже самое делаем и с ids
        if ids != None:
            self.JSON["ids"] = Template_settings_JSON.ids_GET_MeterTable(ids=ids)
        # Преобразовываем в JSON
        self.JSON = json.dumps(self.JSON)
        return self.JSON


# ----------------------------------------------------------------------------------------------------------------------
#                                              PUT
# ----------------------------------------------------------------------------------------------------------------------
class PUT():
    """
    Класс для работы с методом PUT
    """
    # Формируем массив
    JSON = {}
    def __init__(self):
        # Дергаем Метод
        self.JSON["method"] = Template_PUT_JSON().TemplateJSON["method"]

    # Дёргаем таблицу ArchTypes
    def ArchTypes(self, setting = None, ids = None):
        """Здесь Ничего не происходит"""
        pass

    def MeterIfaces(self, setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    def MeterTypes(self, setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    def ArchInfo(self, setting, ids=None):
        """Дополнительных параметры НУЖНО выставить в setting"""

        # Дергаем Нужную таблицу
        self.JSON["table"] = Template_ArchInfo_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            self.JSON["settings"] = Template_settings_JSON.settings_PUT_ArchInfo(settings=setting)
        # тоже самое делаем и с ids
        if ids != None:
            self.JSON["ids"] = None
        # Преобразовываем в JSON
        self.JSON = json.dumps(self.JSON)
        return self.JSON

    def MeterTable(self, setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass


# ----------------------------------------------------------------------------------------------------------------------
#                                              DELETE
# ----------------------------------------------------------------------------------------------------------------------
class DELETE():
    """
    Класс для работы с методом DELETE
    """
    # Формируем массив
    JSON = {}
    def __init__(self):
        # Дергаем Метод
        self.JSON["method"] = Template_DELETE_JSON().TemplateJSON["method"]

    # Дёргаем таблицу ArchTypes
    def ArchTypes(self, setting = None, ids = None):
        """Здесь Ничего не происходит"""
        pass

    def MeterIfaces(self, setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    def MeterTypes(self, setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    def ArchInfo(self, setting=None, ids=None):
        """Здесь Ничего не происходит"""
        pass

    def MeterTable(self, setting=None, ids=None):
        """Дополнительных параметры можно выставить в ids"""

        # Дергаем Нужную таблицу
        self.JSON["table"] = Template_MeterTable_JSON().TemplateJSON["table"]
        # Если мы задали setting, исправляем это
        if setting != None:
            self.JSON["settings"] = Template_settings_JSON.settings_GET_all_table(setting=setting)
        # тоже самое делаем и с ids
        if ids != None:
            self.JSON["ids"] = Template_settings_JSON.ids_DELETE_MeterTable(ids=ids)
        # Преобразовываем в JSON
        self.JSON = json.dumps(self.JSON)
        return self.JSON