# Итак - Здесь расположим тестовый прогон на наш MeterDaemon


from working_directory.Meter_daemon import MeterDaemon
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from working_directory.Template.Template_Meter_devices_API import Template_list_job
from time import sleep
import pytest

# //----------------------------------------------------------------------------------------------------------------
# //------------------------------  Подготовка тестовых данных -----------------------------------------------------
# //----------------------------------------------------------------------------------------------------------------
job_type_list = \
    Template_list_job.JournalValues_list + \
    Template_list_ArchTypes.ElectricConfig_ArchType_name_list + \
    Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list + \
    Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list + \
    Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list + \
    [Template_list_job.SyncTime_list[0]] + [Template_list_job.SyncTime_list[2]] + \
    [Template_list_job.GetSerial_list[0]] + [Template_list_job.GetSerial_list[2]]

# //----------------------------------------------------------------------------------------------------------------
# //---------------------------------   Тестовые Прогоны  ----------------------------------------------------------
# //----------------------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("job_type", job_type_list)
def test_JOB_Meter_devices(type_connect, job_type):
    sleep(1)
    test = MeterDaemon(type_connect=type_connect).DataBase_filled()
    assert test == []