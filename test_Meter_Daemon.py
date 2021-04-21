# Итак - Здесь расположим тестовый прогон на наш MeterDaemon


from working_directory.Meter_daemon import MeterDaemonSingleMeter ,MeterDaemonManyMeter
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from working_directory.Template.Template_Meter_devices_API import Template_list_job
from time import sleep
import pytest
from working_directory.sqlite import deleteMeterTable

# //----------------------------------------------------------------------------------------------------------------
# //------------------------------  Подготовка тестовых данных -----------------------------------------------------
# //----------------------------------------------------------------------------------------------------------------
job_type_list = \
    Template_list_job.JournalValues_list + \
    Template_list_ArchTypes.ElectricConfig_ArchType_name_list + \
    Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list + \
    Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list + \
    Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list


# Набор из тестовых данных для ОДНОГО счетчика
# БД заполнена
def data_for_Single_Meter_DataBase_filled(list_measure, template_parametrize):
    parametrize_list = []
    for i in range(len(list_measure)):
        measure = [list_measure[i]]
        for x in range(len(template_parametrize)):
            element = [measure , template_parametrize[x], 2]
            element = tuple(element)
            parametrize_list.append(element)
    return parametrize_list

# БД чистая
def data_for_Single_Meter_DataBase_clear(list_measure):
    parametrize_list = []
    for i in range(len(list_measure)):
        measure = [list_measure[i]]
        element = [measure, 2]
        element = tuple(element)
        parametrize_list.append(element)

    return parametrize_list

# Набор из тестовых данных для НЕСКОЛЬКИХ СЧЕТЧИКОВ

# Набор Количества счетчиков
meters = [1, 2, 5, 10]
# БД чистая
def data_for_Many_Meter_DataBase_clear(list_measure,meters):
    parametrize_list = []
    for i in range(len(list_measure)):
        measure = [list_measure[i]]
        for y in range(len(meters)):
            element = [measure,2, meters[y]]
            element = tuple(element)
            parametrize_list.append(element)
    return parametrize_list


# БД заполнена
def data_for_Many_Meter_DataBase_filled(list_measure, template_parametrize,meters):
    parametrize_list = []
    for i in range(len(list_measure)):
        measure = [list_measure[i]]
        for x in range(len(template_parametrize)):
            for y in range(len(meters)):
                element = [measure , template_parametrize[x], 2, meters[y]]
                element = tuple(element)
            parametrize_list.append(element)
    return parametrize_list
# # //----------------------------------------------------------------------------------------------------------------
# # //---------------------------------   Тестовые Прогоны  ----------------------------------------------------------
# # //----------------------------------------------------------------------------------------------------------------
#
# # # //------------------------------------   ОДИН СЧЕТЧИК   ----------------------------------------------------------
#
# parametrize_list = data_for_Single_Meter_DataBase_clear(job_type_list)
# # //--------- БД ЧИСТАЯ
# @pytest.mark.parametrize("list_measure , count_tree", parametrize_list)
# def test_MeterDaemonSingleMeter_DataBase_clear(type_connect,
#                                                 # НАШ тип данных
#                                                 list_measure,
#                                                 # Количество элементов в дереве подключения
#                                                 count_tree
#                                                ):
#
#     # Чистим БД
#     sleep(2)
#     deleteMeterTable()
#     sleep(1)
#     MeterDaemon_result = MeterDaemonSingleMeter(type_connect=type_connect).DataBase_clear(list_measure=list_measure,
#                                                                                             count_tree=count_tree)
#     assert MeterDaemon_result == []
#
# # //--------- БД ЗАПОЛНЕНА
# job_type_list = \
#     Template_list_job.JournalValues_list + \
#     Template_list_ArchTypes.ElectricConfig_ArchType_name_list + \
#     Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list + \
#     Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list + \
#     Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list
#
# measure_list = [
#
#                 ]
#
#
# # Памерметры журналов
# JournalValues_count_ts_to_record = [0 , 1 ,5,1000]
# JournalValues_parametrize_list = data_for_Single_Meter_DataBase_filled(Template_list_job.JournalValues_list ,
#                                                                        JournalValues_count_ts_to_record)
# # Параметры Конфигов
# ElectricConfig_count_ts_to_record = [0 , 1]
# ElectricConfig_parametrize_list = data_for_Single_Meter_DataBase_filled(Template_list_ArchTypes.ElectricConfig_ArchType_name_list ,
#                                                                         ElectricConfig_count_ts_to_record)
# # Параметры Энергии
# ElecticEnergyValues_count_ts_to_record = [0 , 1,5,10,30,100]
# ElecticEnergyValues_parametrize_list = data_for_Single_Meter_DataBase_filled(Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list ,
#                                                                         ElecticEnergyValues_count_ts_to_record)
#
#
# @pytest.mark.parametrize("list_measure , count_ts_to_record , count_tree", parametrize_list)
# def test_JOB_MeterDaemonSingleMeter_DataBase_filled(type_connect,
#                                                         # НАШ тип данных
#                                                         list_measure,
#                                                         # количество записей в БД
#                                                         count_ts_to_record,
#                                                         # Количество элементов в дереве подключения
#                                                         count_tree
#                                                     ):
#     # Чистим БД
#     sleep(2)
#     deleteMeterTable()
#     sleep(1)
#     MeterDaemon_result = MeterDaemonSingleMeter(type_connect=type_connect).DataBase_filled(
#                                                                              list_measure=list_measure,
#                                                                              count_ts_to_record=count_ts_to_record,
#                                                                              count_tree=count_tree
#                                                                             )
#     assert MeterDaemon_result == []
#
#
#
# # # //------------------------------------   МНОГО СЧЕТЧИКОВ  -----------------------------------------------------
# # Для начала создадим список из всех возможных тэгов
#
#
#
# parametrize_list = data_for_Many_Meter_DataBase_clear(list_measure=
#                                                       )
# # //--------- БД ЧИСТАЯ
# @pytest.mark.parametrize("list_measure , count_tree, count_meter", parametrize_list)
# def test_MeterDaemonManyMeter_DataBase_clear(type_connect,
#                                                 # НАШ тип данных
#                                                 list_measure,
#                                                 # Количество элементов в дереве подключения
#                                                 count_tree,
#                                                 # Количество добавляемых счетчиков
#                                                 count_meter
#                                              ):
#
#     # Чистим БД
#     sleep(2)
#     deleteMeterTable()
#     sleep(1)
#     MeterDaemon_result = MeterDaemonManyMeter(type_connect=type_connect).DataBase_clear(list_measure=list_measure,
#                                                                                         count_tree=count_tree,
#                                                                                         count_meter=count_meter)
#     assert MeterDaemon_result == []
#
# # //--------- БД ЗАПОЛНЕНА
#
# parametrize_list =
# @pytest.mark.parametrize("list_measure , count_ts_to_record , count_tree", parametrize_list)
# def test_JOB_MeterDaemonManyMeter_DataBase_filled(type_connect,
#                                                     # НАШ тип данных
#                                                     list_measure,
#                                                     # количество записей в БД
#                                                     count_ts_to_record,
#                                                     # Количество элементов в дереве подключения
#                                                     count_tree,
#                                                    # Количество добавляемых счетчиков
#                                                     count_meter
#                                                   ):
#     # Чистим БД
#     sleep(2)
#     deleteMeterTable()
#     sleep(1)
#     MeterDaemon_result = MeterDaemonManyMeter(type_connect=type_connect).DataBase_filled(
#                                                                                         list_measure=list_measure,
#                                                                                         count_ts_to_record=count_ts_to_record,
#                                                                                         count_tree=count_tree,
#                                                                                         count_meter=count_meter
#                                                                                         )
#     assert MeterDaemon_result == []
#
