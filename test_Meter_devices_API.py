# Итак , здесь расположим тестовый прогон для пайтеста для MeterDev
from working_directory.Meter_device_API import VirtualMeter
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from working_directory.Template.Template_Meter_devices_API import Template_list_job
from time import sleep
import pytest

job_type_list = \
    Template_list_job.JournalValues_list + \
    Template_list_ArchTypes.ElectricConfig_ArchType_name_list + \
    Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list + \
    Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list + \
    Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list + \
    [Template_list_job.SyncTime_list[0]] + [Template_list_job.SyncTime_list[2]] + \
    [Template_list_job.GetSerial_list[0]] + [Template_list_job.GetSerial_list[2]]

@pytest.mark.parametrize("job_type", job_type_list)
def test_JOB_Meter_devices(type_connect, job_type):
    sleep(1)
    test = VirtualMeter(type_connect=type_connect).iface_Ethernet(job_type=job_type)
    assert test == []