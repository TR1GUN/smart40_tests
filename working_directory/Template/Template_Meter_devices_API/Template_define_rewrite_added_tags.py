from copy import deepcopy
from working_directory.Template.Template_Meter_devices_API.Template_list_job import Journal_dict
# //----------------------------------------------------------------------------------------------------------------
#                                             КЛАСС ДЛЯ ПЕРЕОПРЕДЕЛЕНИЯ ТЭГОВ
# //----------------------------------------------------------------------------------------------------------------


class DefineKeysTag:
    '''
    Данный класс нужен чтоб получить наши переопределенные ТЭГИ , да
    '''
    measure = ''
    Settings = None
    tags = {}

    def __init__(self, measure, Settings):

        # ПЕРЕОПРЕДЕЛЯЕМ
        self.measure = measure
        self.Settings = Settings
        self.tags = self.__define_keys_tag()

    # //---------------------------ПЕРЕОПРЕДЕЛЕНИЕ ТЭГОВ------------------------------------------------------
    def __define_keys_tag(self):
        """
        В ЭТОМ МЕТОДЕ ОПРЕДЕЛЯЕМ СРАЗУ ПЕРЕОПРЕДЕЛЕННЫЕ ТЭГИ , ЧТОБ ПОТОМ ИХ НЕ МЕНЯТЬ
        :return:
        """

        all_tags = \
            {
                'ElMomentQuality':
                    {
                        'CE303':
                            {
                                'SA': None,
                                'SB': None,
                                'SC': None,
                                'SS': None,
                            }

                    },

                'ElArr1ConsPower':
                    {
                        'CE303':
                            {
                                "isPart": False,
                                "isOvfl": False,
                                "isSummer": False,
                                # ПЕРИОД ИНТЕГРАЦИИ
                                'cTime': deepcopy(int(self.Settings.cTime))
                            }

                    },

                'ElConfig':
                    {
                        'CE303':
                            {
                                # Модель и серийник счетчика
                                'serial': self.Settings.snumber,
                                'model': self.Settings.name,
                                # cArrays - количество архивов профилей мощности (на данный момент -  всегда 1)
                                'cArrays': 1,
                                'const': 1.0,
                                # значение тэга isDst - разрешение перехода на летнее время -
                                # берется из Кучи параметров -
                                'isDst': False,
                                # наличие часов (есть всегда для энергомеры)
                                'isClock': True,
                                # isTrf - наличие тарификатора (есть всегда для энергомеры)
                                'isTrf': True,
                                # наличие обратной реактивной энергии и наличие прямой реактивной энергии
                                'isRm': True,
                                'isAm': True,
                                'isRp': True,
                                # ПЕРИОД ИНТЕГРАЦИИ
                                'cTime': deepcopy(int(self.Settings.cTime))
                            }
                    }
            }

        # ПОУЛЧАЕМ НАШИ ТЭГИ
        tags = all_tags.get(self.measure)
        if tags is not None:
            tags = tags.get(self.Settings.name)
            if tags is None:
                tags = {}
        else:
            tags = {}
        return tags


# //-------------------------------------------------------------------------------------------------------------
#                                          КЛАСС ДЛЯ ДОБАВЛЕНИя НОВЫХ ТЭГОВ
# //-------------------------------------------------------------------------------------------------------------
class AddedKeysTag:
    """
        Данный класс нужен чтоб получить наши ДОБАВЛЕНЫЕ ТЭГИ , да
    """
    measure = ''
    Settings = None
    tags = {}

    def __init__(self, measure, Settings):
        # ПЕРЕОПРЕДЕЛЯЕМ
        self.measure = measure
        self.Settings = Settings
        self.tags = self.__added_keys_tag()

    def __added_keys_tag(self):
        """
        ЗДЕСЬ ОПРЕДЕЛЯЕМ КАКИЕ ТЭГИ ДОЛЖНЫ ДОБАВИТЬ
        :return:
        """

        all_tags = \
            {
                'ElConfig':
                    {
                        'CE303': [
                            {
                                "tag": "VarConsDepth",
                                "val": 4752
                            },
                            {
                                "tag": "MonDepth",
                                "val": 12
                            },
                            {
                                "tag": "MonConsDepth",
                                "val": 13
                            },
                            {
                                "tag": "DayDepth",
                                "val": 44
                            },
                            {
                                "tag": "DayConsDepth",
                                "val": 44
                            },
                            {
                                "tag": "cTime",
                                "val": deepcopy(int(self.Settings.cTime))
                            },
                            {
                                "tag": "isCons",
                                "val": True
                            }
                        ]

                    },
                "ElArr1ConsPower":
                    {
                        'CE303': [
                            {
                                "tag": "isMeas",
                                "val": False
                            }
                        ]
                    },
                "Journal":
                    {
                        'CE303': [
                            {
                                "tag": "journalId",
                                "val": Journal_dict.get(self.measure)
                            }
                        ]
                    },

            }


        # ПОУЛЧАЕМ НАШИ ТЭГИ
        if self.measure in ['ElJrnlLimUAMax', 'ElJrnlLimUAMin',
                            'ElJrnlLimUBMax', 'ElJrnlLimUBMin',
                            'ElJrnlLimUCMax', 'ElJrnlLimUCMin',
                            'ElJrnlPwrC', 'ElJrnlPwrB', 'ElJrnlPwrA',
                            'ElJrnlPwr', 'ElJrnlTimeCorr', 'ElJrnlReset', 'ElJrnlTrfCorr', 'ElJrnlOpen', 'ElJrnlUnAyth'
                            ]:

            tags = all_tags.get("Journal")
        else:

            tags = all_tags.get(self.measure)

        if tags is not None:
            tags = tags.get(self.Settings.name)
            if tags is None:
                tags = []
        else:
            tags = []
        return tags
