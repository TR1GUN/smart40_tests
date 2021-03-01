# Здесь расположим класс который определяет набор тэгов по значению measure

from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes


class DefineTagsByMeasure:
    """
    Класс определитель тэгов по значению Measure

    Пихаем  Measure в конструктор , и тут же считываем из поля его сюда tag правильный набор тэгов

    Так же можно получить с помощью метода get_tags

    """
    tag = []

    def __init__(self, measure):
        self.measure = measure
        self.tag = self.__define_tags_by_measure(measure=measure)

    def __define_tags_by_measure(self, measure):
        # Для ElConfig
        if measure in Template_list_ArchTypes.ElectricConfig_ArchType_name_list :

            tags = Template_list_ArchTypes.ElectricConfig_tag

        # PlsConfig
        elif measure in Template_list_ArchTypes.PulseConfig_ArchType_name_list:
            tags = Template_list_ArchTypes.PulseConfig_tag

        # DigConfig
        elif measure in Template_list_ArchTypes.DigitalConfig_ArchType_name_list:
            tags = Template_list_ArchTypes.DigitalConfig_tag

            # ElMomentEnergy, ElDayEnergy, ElMonthEnergy, ElDayConsEnergy, ElMonthConsEnergy
        elif measure in Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list:
            tags = Template_list_ArchTypes.ElecticEnergyValues_tag

            # ElMomentQuality
        elif measure in Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list:

            tags = Template_list_ArchTypes.ElectricQualityValues_tag

        # ElArr1ConsPower
        elif measure in Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list:

            tags = Template_list_ArchTypes.ElectricPowerValues_tag

        # 'PlsMomentPulse'  'PlsDayPulse' 'PlsMonthPulse' 'PlsHourPulse'
        elif measure in Template_list_ArchTypes.PulseValues_ArchType_name_list:

            tags = Template_list_ArchTypes.PulseValues_tag

        # 'DigMomentState', 'DigJournalState'
        elif measure in Template_list_ArchTypes.DigitalValues_ArchType_name_list:

            tags = Template_list_ArchTypes.DigitalValues_tag


        # ElJrnlPwr  ElJrnlTimeCorr  ElJrnlReset  ElJrnlC1Init  ElJrnlC2Init  ElJrnlTrfCorr  ElJrnlOpen  ElJrnlUnAyth
        # ElJrnlPwrA  ElJrnlPwrB  ElJrnlPwrC  ElJrnlProg  ElJrnlRelay  ElJrnlLimESumm  ElJrnlLimETrf  ElJrnlLimETrf1
        # ElJrnlLimETrf2  ElJrnlLimETrf3  ElJrnlLimETrf4  ElJrnlLimUAMax  ElJrnlLimUAMin  ElJrnlLimUBMax  ElJrnlLimUBMin
        # ElJrnlLimUCMax  ElJrnlLimUCMin  ElJrnlLimUABMax  ElJrnlLimUABMin  ElJrnlLimUBCMax  ElJrnlLimUBCMin
        # ElJrnlLimUCAMax  ElJrnlLimUCAMin  ElJrnlLimIAMax  ElJrnlLimIBMax   ElJrnlLimICMax  ElJrnlLimFreqMax
        # ElJrnlLimFreqMin  ElJrnlLimPwr  ElJrnlLimPwrPP  ElJrnlLimPwrPM  ElJrnlLimPwrQP  ElJrnlLimPwrQM  ElJrnlReverce
        # PlsJrnlTimeCorr

        elif measure in Template_list_ArchTypes.JournalValues_ArchType_name_list:

            tags = Template_list_ArchTypes.JournalValues_tag

            # Здесь же получаем список тех полей что нам нужны по селекту

        # Иначе - Ставим тэг пустым
        else:
            tags = None

        return tags

    def get_tags(self):
        return self.__define_tags_by_measure(measure=self.measure)