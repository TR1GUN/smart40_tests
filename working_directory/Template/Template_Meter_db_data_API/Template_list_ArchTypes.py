# Создадим отдельный скрипт в котором будут хранится только значения для ArchTypes



ElectricConfig_ArchType_name_list = ['ElConfig']

PulseConfig_ArchType_name_list = ['PlsConfig']

DigitalConfig_ArchType_name_list = ['DigConfig']

ElecticEnergyValues_ArchType_name_list = ['ElMomentEnergy', 'ElDayEnergy', 'ElMonthEnergy', 'ElDayConsEnergy', 'ElMonthConsEnergy']

ElectricQualityValues_ArchType_name_list = ['ElMomentQuality']

ElectricPowerValues_ArchType_name_list = ['ElArr1ConsPower']

PulseValues_ArchType_name_list = ['PlsMomentPulse','PlsDayPulse','PlsMonthPulse','PlsHourPulse']


DigitalValues_ArchType_name_list = ['DigMomentState', 'DigJournalState']


JournalValues_ArchType_name_list = [
            'ElJrnlPwr', 'ElJrnlTimeCorr', 'ElJrnlReset', 'ElJrnlC1Init', 'ElJrnlC2Init', 'ElJrnlTrfCorr', 'ElJrnlOpen',
            'ElJrnlUnAyth', 'ElJrnlPwrA', 'ElJrnlPwrB', 'ElJrnlPwrC', 'ElJrnlProg', 'ElJrnlRelay', 'ElJrnlLimESumm',
            'ElJrnlLimETrf', 'ElJrnlLimETrf1', 'ElJrnlLimETrf2', 'ElJrnlLimETrf3', 'ElJrnlLimETrf4', 'ElJrnlLimUAMax',
            'ElJrnlLimUAMin', 'ElJrnlLimUBMax', 'ElJrnlLimUBMin', 'ElJrnlLimUCMax', 'ElJrnlLimUCMin', 'ElJrnlLimUABMax',
            'ElJrnlLimUABMin', 'ElJrnlLimUBCMax', 'ElJrnlLimUBCMin', 'ElJrnlLimUCAMax', 'ElJrnlLimUCAMin',
            'ElJrnlLimIAMax', 'ElJrnlLimIBMax', 'ElJrnlLimICMax', 'ElJrnlLimFreqMax', 'ElJrnlLimFreqMin', 'ElJrnlLimPwr',
            'ElJrnlLimPwrPP', 'ElJrnlLimPwrPM', 'ElJrnlLimPwrQP', 'ElJrnlLimPwrQM', 'ElJrnlReverce', 'PlsJrnlTimeCorr'
                        ]



# А теперь пропишем нужные тэги значений этим замечательным людям
ElectricConfig_tag = ['serial', 'model', 'cArrays', 'isDst', 'isClock', 'isTrf', 'isAm', 'isRm', 'isRp', 'kI', 'kU', 'const']


# ВЫРЕЗАНО 'isClock'
PulseConfig_tag = [ 'serial','model', 'chnl', 'isDst']

# ВЫРЕЗАНО 'isClock'
DigitalConfig_tag = ['serial', 'model', 'chnlIn', 'chnlOut', 'isDst']

ElecticEnergyValues_tag = ['A+0', 'A+1', 'A+2', 'A+3', 'A+4', 'A-0', 'A-1', 'A-2', 'A-3', 'A-4',
                    'R+0', 'R+1', 'R+2', 'R+3', 'R+4', 'R-0', 'R-1', 'R-2', 'R-3', 'R-4']

ElectricQualityValues_tag = ['UA', 'UB', 'UC', 'IA', 'IB', 'IC', 'PS', 'PA', 'PB', 'PC' , 'QS', 'QA',
                    'QB', 'QC', 'SS', 'SA', 'SB', 'SC', 'AngAB', 'AngBC', 'AngAC', 'kPS', 'kPA', 'kPB', 'kPC', 'Freq']

ElectricPowerValues_tag = ['cTime', 'P+', 'Q+', 'P-', 'Q-',  'isPart', 'isOvfl','isSummer']


PulseValues_tag = ['Pls1', 'Pls2', 'Pls3', 'Pls4', 'Pls5', 'Pls6', 'Pls7', 'Pls8', 'Pls9', 'Pls10', 'Pls11', 'Pls12',
                    'Pls13', 'Pls14', 'Pls15', 'Pls16', 'Pls17', 'Pls18', 'Pls19', 'Pls20', 'Pls21', 'Pls22', 'Pls23',
                    'Pls24', 'Pls25', 'Pls26', 'Pls27', 'Pls28', 'Pls29', 'Pls30', 'Pls31', 'Pls32']

DigitalValues_tag = ['Chnl1', 'Chnl2', 'Chnl3', 'Chnl4', 'Chnl5', 'Chnl6', 'Chnl7', 'Chnl8', 'Chnl9', 'Chnl10',
                    'Chnl11', 'Chnl12', 'Chnl13', 'Chnl14', 'Chnl15', 'Chnl16', 'Chnl17', 'Chnl18', 'Chnl19', 'Chnl20',
                    'Chnl21', 'Chnl22', 'Chnl23', 'Chnl24', 'Chnl25', 'Chnl26', 'Chnl27', 'Chnl28', 'Chnl29', 'Chnl30',
                    'Chnl31', 'Chnl32']

JournalValues_tag = ['event', 'eventId']