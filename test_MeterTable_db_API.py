# Здесь расположим тесты на тестирование на работу нашей БД
from working_directory.Meter_device_API import VirtualMeter
from working_directory.Meter_data_base import ArchInfo
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from time import sleep
import pytest

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

all_tag = ElectricConfig_ArchType_name_list + PulseConfig_ArchType_name_list + DigitalConfig_ArchType_name_list + \
          ElecticEnergyValues_ArchType_name_list + ElectricQualityValues_ArchType_name_list + \
          ElectricPowerValues_ArchType_name_list + PulseValues_ArchType_name_list + DigitalValues_ArchType_name_list + \
          JournalValues_ArchType_name_list
# ---------------------------------------------------------------------------------------------------------------------
#                                                  ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ---------------------------------------------------------------------------------------------------------------------
template_parametrize = \
    [
        1, 3, 5, 10, 15
    ]


def get_parametrs(arch_type_name_list: list):
    '''
    Вспомогательная функция чтоб создать сет из тестовых данных
    '''
    parametrize_list = []

    for i in range(len(arch_type_name_list)):
        for x in range(len(template_parametrize)):
            element = [arch_type_name_list[i], template_parametrize[x]]

            element = tuple(element)
            parametrize_list.append(element)
    return parametrize_list


# ---------------------------------------------------------------------------------------------------------------------
parametr = get_parametrs(all_tag)


@pytest.mark.parametrize("measure ,count_records ", parametr)
def test_ArchInfo_field_records(type_connect, measure, count_records):
    sleep(1)

    meterdata = ArchInfo(type_connect=type_connect).RecordsCheckUp(ArchType_Name=measure,
                                                                   Count_records=count_records)
    assert meterdata == []
