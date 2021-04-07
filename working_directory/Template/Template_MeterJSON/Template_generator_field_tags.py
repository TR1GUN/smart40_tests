import random
from random import randint
from working_directory.Template.Template_Meter_db_data_API.Template_list_ArchTypes import \
    ElectricConfig_ArchType_name_list, \
    PulseConfig_ArchType_name_list, \
    DigitalConfig_ArchType_name_list, \
    ElecticEnergyValues_ArchType_name_list, \
    ElectricQualityValues_ArchType_name_list, \
    ElectricPowerValues_ArchType_name_list, \
    PulseValues_ArchType_name_list, \
    DigitalValues_ArchType_name_list, \
    JournalValues_ArchType_name_list, \
    ElecticEnergyValues_tag
from working_directory.Template.Template_Meter_db_data_API.Template_define_tags_by_measure import DefineTagsByMeasure

# ----------------------------------------------------------------------------------------------------------------------
#                                         ГЕНЕРАТОР МАССИВА ДЛЯ TAGS
# ----------------------------------------------------------------------------------------------------------------------
# Здесь зададим Класс генератор для настроек


class GeneratorTagsByDevices:
    """
    Класс для генерации массива tags
    """
    measure = ''
    tags = []

    # Конструктор для генерации тэгов - очень важно - принимает строковые значения
    def __init__(self, measure: str):

        self.measure = measure

        self.tags = self.__generate_list_tags_by_devices(measure)

    # А это очень важная штука - генерирует список тэгов относительно поля measure - Следовательно - подавать его
    def __generate_list_tags_by_devices(self, measure):
        # Получаем нужный набор всех тэгов из специального класса
        tags = DefineTagsByMeasure(measure).tag
        # После того как Мы определились с тэгами - пропускаем их через генератор значений
        tags_list = self.__filling_tags(tags=tags)

        return tags_list

    # конструктор для заполнения списка тэгов- ето ваажно
    def __filling_tags(self, tags):
        """
        Конструктор для заполнения тэгов , кушает массив для доступных тэгов

        :param tags: сюда пихаем массив тэгов
        :return: возвращает нормальный список из словарей имени и значений
        """
        # тэги которые нужно заполнить

        # Наш участок JSON
        tags_json_list = []
        if tags is None:
            return None
        for i in range(len(tags)):

            template_tags = {"tag": tags[i], "val": self.__definion_type_val(tags[i])}

            # по умолчанию ставим в double - 0.0

            tags_json_list.append(template_tags)

        return tags_json_list

    # Здесь определяем тип переменной - Это важно !!!
    def __definion_type_val(self, tag):
        """
        Функция для определения значения тэга - определяет тип переменной

        :param tag: принимает имя тэга
        :return:  возвращает значение для этого тэга
        """
        # Определяем булевы значения
        if tag in ['Chnl1', 'Chnl2', 'Chnl3', 'Chnl4', 'Chnl5', 'Chnl6', 'Chnl7', 'Chnl8', 'Chnl9', 'Chnl10',
                   'Chnl11', 'Chnl12', 'Chnl13', 'Chnl14', 'Chnl15', 'Chnl16', 'Chnl17', 'Chnl18', 'Chnl19', 'Chnl20',
                   'Chnl21', 'Chnl22', 'Chnl23', 'Chnl24', 'Chnl25', 'Chnl26', 'Chnl27', 'Chnl28', 'Chnl29', 'Chnl30',
                   'Chnl31', 'Chnl32',
                   'isSummer', 'isOvfl', 'isPart', 'isRm', 'isAm', 'isRp', 'isDst', 'isClock', 'isTrf']:
            generate = randint(0, 1)
            if generate == 0:
                val = False
            else:
                val = True

        # Определяем значения для журналов
        elif tag in ['eventId', 'event']:
            # Итак - тут очень важно начнем витвление
            if self.measure in ['ElJrnlLimUAMax', 'ElJrnlLimUAMin', 'ElJrnlLimUBMax', 'ElJrnlLimUBMin',
                                'ElJrnlLimUCMax', 'ElJrnlLimUCMin', 'ElJrnlPwrC', 'ElJrnlPwrB', 'ElJrnlPwrA',
                                "ElJrnlPwr", ]:
                # Если у нас действительно этот тип значений , тогда что делаем - мы ставим либо 1 либо 0
                # val = int(randint(0, 1))
                val = 1

            elif self.measure in ['ElJrnlUnAyth',"ElJrnlTrfCorr", 'ElJrnlReset', 'ElJrnlTimeCorr']:
                val = 0

            # Иначе -  действуем по обычной схеме
            else:
                val = int(randint(0, 100))

        # определяем значения интовые
        elif tag in [
            'chnl', 'chnlIn', 'chnlOut',
            'cTime', 'cArrays']:
            val = int(randint(0, 100))

        # опрелеляем значения стринговые
        elif tag in ['serial']:
            val = str(randint(1000000000, 1999999999))

        elif tag in ['model']:
            val = 'Test model Your ad could be here'

        # Значения показателей энергии
        elif tag in ['Freq']:
            val = float(random.uniform(11.11, 99.99))
            val = float('{:.2f}'.format(val))

        elif tag in ['kI', 'kU']:
            val = float(random.uniform(11.11, 99.99))
            val = float('{:.0f}'.format(val))

        # Значения показателей энергии
        elif tag in ElecticEnergyValues_tag:
            val = float(random.uniform(111.111, 999.999))
            val = float('{:.3f}'.format(val))
        # иначе - ставим в дабл
        else:
            val = float(random.uniform(-99.99, 99.99))
            val = float('{:.4f}'.format(val))
        return val

    def get_tags(self):
        """
        Функция которая возвращает результат генерации

        :return:
        """
        return self.tags

    def get_Castrom_Value(self, Castrom_Value:dict):
        # Сюда спускаем и перезаписываем ТЭГИ которые были заранее Определены - ЭТО ВАЖНО
        # Перебираем все возможные комбинации
        for tag_castrom_value in Castrom_Value:
            for i in range(len(self.tags)):
                if tag_castrom_value == self.tags[i].get('tag'):
                    # Если совпадают - То его перезаписываем
                    self.tags[i]['val'] = Castrom_Value[tag_castrom_value]

