# Здесь расположим тесты на MeterData для None значений
from working_directory.Meter_db_data_API import POST, GET
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes

from time import sleep
import pytest
# Загружаем тестовые данные
import write_file

# Итак здесь расположим наши тестовые вызовы

ElectricConfig_ArchType_name_list = Template_list_ArchTypes.ElectricConfig_ArchType_name_list
PulseConfig_ArchType_name_list = Template_list_ArchTypes.PulseConfig_ArchType_name_list
DigitalConfig_ArchType_name_list = Template_list_ArchTypes.DigitalConfig_ArchType_name_list
ElecticEnergyValues_ArchType_name_list = Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list
ElectricQualityValues_ArchType_name_list = Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list
ElectricPowerValues_ArchType_name_list = Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list
PulseValues_ArchType_name_list = Template_list_ArchTypes.PulseValues_ArchType_name_list
DigitalValues_ArchType_name_list = Template_list_ArchTypes.DigitalValues_ArchType_name_list
JournalValues_ArchType_name_list = Template_list_ArchTypes.JournalValues_ArchType_name_list


# ---------------------------------------------------------------------------------------------------------------------
#                                                  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ---------------------------------------------------------------------------------------------------------------------
def parametrize_by_element(Adding_Tags: list, ArchType_name_list: list):
    parametrize_list = []
    # Если у нас гет запрос
    template_parametrize = [
        [1, 1],
        [2, 3],
        [3, 1],
        [1, 1],
        [2, 3],
        [3, 1]
    ]
    for i in range(len(ArchType_name_list)):
        ArchType_name = [ArchType_name_list[i]]
        for x in range(len(template_parametrize)):
            for y in range(len(Adding_Tags)):
                element = [ArchType_name] + template_parametrize[x] + [Adding_Tags[y]]
                element = tuple(element)
                parametrize_list.append(element)

    return parametrize_list


# ---------------------------------------------------------------------------------------------------------------------
#                                                  POST
# ---------------------------------------------------------------------------------------------------------------------
# list_measure - Список из Тэгов
# count_id - Количество айдишников
# count_ts колличество времени
# generate_unicale_id - сгенерировать уникальные айдишник
# generate_unicale_ts - Сгенерирвоать уникальный таймштамп

# ------------------------------------- ElecticEnergyValues ----------------------------------------------------------
adding_tag_ElecticEnergyValues = [

    {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
        'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
        'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
        'A+3': None, 'A-3': None, 'R+3': None, 'R-3': None,
        'A+4': None, 'A-4': None, 'R+4': None, 'R-4': None,
    },

    {
        'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
        'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
        'A+3': None, 'A-3': None, 'R+3': None, 'R-3': None,
        'A+4': None, 'A-4': None, 'R+4': None, 'R-4': None,
    },
    {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
        'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
        'A+3': None, 'A-3': None, 'R+3': None, 'R-3': None,
        'A+4': None, 'A-4': None, 'R+4': None, 'R-4': None,
    },

    {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
        'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
        'A+3': None, 'A-3': None, 'R+3': None, 'R-3': None,
        'A+4': None, 'A-4': None, 'R+4': None, 'R-4': None,
    },

    {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
        'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
        'A+4': None, 'A-4': None, 'R+4': None, 'R-4': None,
    },

    {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
        'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
        'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
        'A+3': None, 'A-3': None, 'R+3': None, 'R-3': None,
    },

    {
        'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
        'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
        'A+3': None, 'A-3': None, 'R+3': None, 'R-3': None,
    },

    {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
        'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
        'A+3': None, 'A-3': None, 'R+3': None, 'R-3': None,
    },

    {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
        'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
        'A+3': None, 'A-3': None, 'R+3': None, 'R-3': None,
    },

    {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
        'A+3': None, 'A-3': None, 'R+3': None, 'R-3': None,
    },

    {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
        'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
        'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
    },

    {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
        'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
    },

    {
        'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
        'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
    },

    {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
        'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
    },

    {
        'A+4': None, 'A-4': None, 'R+4': None, 'R-4': None,
    },

    {
        'A+3': None, 'A-3': None, 'R+3': None, 'R-3': None,
    },

    {
        'A+2': None, 'A-2': None, 'R+2': None, 'R-2': None,
    },

    {
        'A-1': None, 'R+1': None, 'A+1': None, 'R-1': None,
    },

    {
        'A-0': None, 'R+0': None, 'R-0': None, 'A+0': None,
    },

]

parametrize_ElecticEnergyValues_ArchType_name_list = parametrize_by_element(
    ArchType_name_list=ElecticEnergyValues_ArchType_name_list,
    Adding_Tags=adding_tag_ElecticEnergyValues)


@pytest.mark.parametrize("list_measure, count_id, count_ts, tags",
                         parametrize_ElecticEnergyValues_ArchType_name_list)
def test_POST_ElecticEnergyValues_meterdata_db_by_element(type_connect, list_measure,
                                                          count_id,
                                                          count_ts,
                                                          tags):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                tags=tags)

    assert meterdata == []


# ------------------------------------- ElectricQualityValues ---------------------------------------------------------
adding_tag_ElectricQualityValues = [
    {
        'UA': None, 'IA': None, 'PA': None, 'QA': None, 'SA': None, 'kPA': None, 'AngAB': None,
        'UB': None, 'IB': None, 'PB': None, 'QB': None, 'SB': None, 'kPB': None, 'AngBC': None,
        'UC': None, 'IC': None, 'PC': None, 'QC': None, 'SC': None, 'kPC': None, 'AngAC': None,
        'PS': None, 'QS': None, 'SS': None, 'kPS': None, 'Freq': None,
    },
    {
        'UA': None, 'IA': None, 'PA': None, 'QA': None, 'SA': None, 'kPA': None, 'AngAB': None,
        'UB': None, 'IB': None, 'PB': None, 'QB': None, 'SB': None, 'kPB': None, 'AngBC': None,
        'UC': None, 'IC': None, 'PC': None, 'QC': None, 'SC': None, 'kPC': None, 'AngAC': None,

    },
    {
        'UA': None, 'IA': None, 'PA': None, 'QA': None, 'SA': None, 'kPA': None, 'AngAB': None,
        'UB': None, 'IB': None, 'PB': None, 'QB': None, 'SB': None, 'kPB': None, 'AngBC': None,
        'PS': None, 'QS': None, 'SS': None, 'kPS': None, 'Freq': None,
    },
    {
        'UA': None, 'IA': None, 'PA': None, 'QA': None, 'SA': None, 'kPA': None, 'AngAB': None,
        'UC': None, 'IC': None, 'PC': None, 'QC': None, 'SC': None, 'kPC': None, 'AngAC': None,
        'PS': None, 'QS': None, 'SS': None, 'kPS': None, 'Freq': None,
    },
    {
        'UB': None, 'IB': None, 'PB': None, 'QB': None, 'SB': None, 'kPB': None, 'AngBC': None,
        'UC': None, 'IC': None, 'PC': None, 'QC': None, 'SC': None, 'kPC': None, 'AngAC': None,
        'PS': None, 'QS': None, 'SS': None, 'kPS': None, 'Freq': None,
    },
    {
        'UC': None, 'IC': None, 'PC': None, 'QC': None, 'SC': None, 'kPC': None, 'AngAC': None,
        'PS': None, 'QS': None, 'SS': None, 'kPS': None, 'Freq': None,
    },
    {
        'UA': None, 'IA': None, 'PA': None, 'QA': None, 'SA': None, 'kPA': None, 'AngAB': None,
        'UB': None, 'IB': None, 'PB': None, 'QB': None, 'SB': None, 'kPB': None, 'AngBC': None,
    },
    {
        'UA': None, 'IA': None, 'PA': None, 'QA': None, 'SA': None, 'kPA': None, 'AngAB': None,
        'UC': None, 'IC': None, 'PC': None, 'QC': None, 'SC': None, 'kPC': None, 'AngAC': None,
    },
    {
        'UB': None, 'IB': None, 'PB': None, 'QB': None, 'SB': None, 'kPB': None, 'AngBC': None,
        'PS': None, 'QS': None, 'SS': None, 'kPS': None, 'Freq': None,
    },
    {
        'UA': None, 'IA': None, 'PA': None, 'QA': None, 'SA': None, 'kPA': None, 'AngAB': None,
    },
    {
        'UB': None, 'IB': None, 'PB': None, 'QB': None, 'SB': None, 'kPB': None, 'AngBC': None,
    },
    {
        'UC': None, 'IC': None, 'PC': None, 'QC': None, 'SC': None, 'kPC': None, 'AngAC': None,
    },
    {
        'PS': None, 'QS': None, 'SS': None, 'kPS': None, 'Freq': None,
    }
]

parametrize_ElectricQualityValues_ArchType_name_list = parametrize_by_element(
    ArchType_name_list=ElectricQualityValues_ArchType_name_list,
    Adding_Tags=adding_tag_ElectricQualityValues)


@pytest.mark.parametrize("list_measure, count_id, count_ts, tags",
                         parametrize_ElectricQualityValues_ArchType_name_list)
def test_POST_ElectricQualityValues_meterdata_db(type_connect, list_measure,
                                                 count_id,
                                                 count_ts,
                                                 tags):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                tags=tags)

    assert meterdata == []


# ------------------------------------- ElectricPowerValues -----------------------------------------------------------
adding_tag_ElectricPowerValues = \
    [
        {
            'cTime': None, 'P+': None, 'Q+': None, 'P-': None, 'Q-': None, 'isPart': None, 'isOvfl': None,
            'isSummer': None
        },
        {
            'cTime': None, 'isPart': None, 'isOvfl': None, 'isSummer': None
        },
        {
            'P+': None, 'Q+': None, 'P-': None, 'Q-': None
        }
    ]

parametrize_ElectricPowerValues_ArchType_name_list = parametrize_by_element(
    ArchType_name_list=ElectricPowerValues_ArchType_name_list,
    Adding_Tags=adding_tag_ElectricPowerValues)


@pytest.mark.parametrize("list_measure, count_id, count_ts, tags",
                         parametrize_ElectricPowerValues_ArchType_name_list)
def test_POST_ElectricPowerValues_meterdata_db_by_element(type_connect,
                                                          list_measure,
                                                          count_id,
                                                          count_ts,
                                                          tags):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                tags=tags
                                                                )

    assert meterdata == []


# ------------------------------------- PulseValues -----------------------------------------------------------------

adding_tag_PulseValues = [
    {
        'Pls1': None, 'Pls2': None, 'Pls3': None, 'Pls4': None, 'Pls5': None, 'Pls6': None, 'Pls7': None,
        'Pls8': None, 'Pls9': None, 'Pls10': None, 'Pls11': None, 'Pls12': None,
        'Pls13': None, 'Pls14': None, 'Pls15': None, 'Pls16': None, 'Pls17': None, 'Pls18': None,
        'Pls19': None, 'Pls20': None, 'Pls21': None, 'Pls22': None, 'Pls23': None,
        'Pls24': None, 'Pls25': None, 'Pls26': None, 'Pls27': None, 'Pls28': None, 'Pls29': None,
        'Pls30': None, 'Pls31': None, 'Pls32': None},
    {}

]

parametrize_PulseValues_ArchType_name = parametrize_by_element(
    ArchType_name_list=PulseValues_ArchType_name_list,
    Adding_Tags=adding_tag_PulseValues)


@pytest.mark.parametrize("list_measure, count_id, count_ts, tags",
                         parametrize_PulseValues_ArchType_name
                         )
def test_POST_PulseValues_meterdata_db_by_element(type_connect,
                                                  list_measure,
                                                  count_id,
                                                  count_ts,
                                                  tags):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                tags=tags)

    assert meterdata == []


# ------------------------------------- DigitalValues -----------------------------------------------------------------

adding_tag_DigitalValues = [
    {
        'Chnl1': None, 'Chnl2': None, 'Chnl3': None, 'Chnl4': None, 'Chnl5': None, 'Chnl6': None,
        'Chnl7': None, 'Chnl8': None, 'Chnl9': None,
        'Chnl10': None,
        'Chnl11': None, 'Chnl12': None, 'Chnl13': None, 'Chnl14': None, 'Chnl15': None, 'Chnl16': None,
        'Chnl17': None, 'Chnl18': None,
        'Chnl19': None, 'Chnl20': None,
        'Chnl21': None, 'Chnl22': None, 'Chnl23': None, 'Chnl24': None, 'Chnl25': None, 'Chnl26': None,
        'Chnl27': None, 'Chnl28': None,
        'Chnl29': None, 'Chnl30': None,
        'Chnl31': None, 'Chnl32': None,
    }
]

parametrize_DigitalValues_ArchType_name = parametrize_by_element(
    ArchType_name_list=DigitalValues_ArchType_name_list,
    Adding_Tags=adding_tag_DigitalValues)


@pytest.mark.parametrize("list_measure, count_id, count_ts,tags",
                         parametrize_DigitalValues_ArchType_name
                         )
def test_POST_DigitalValues_meterdata_db_by_element(type_connect,
                                                    list_measure,
                                                    count_id,
                                                    count_ts,
                                                    tags):
    sleep(1)
    meterdata = POST(type_connect=type_connect).Сustom_measures(list_measure=list_measure,
                                                                count_id=count_id,
                                                                count_ts=count_ts,
                                                                tags=tags)

    assert meterdata == []


# ---------------------------------------------------------------------------------------------------------------------