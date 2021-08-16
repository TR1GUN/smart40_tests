# Итак - здесь генерируем job
from working_directory.Template.Template_Meter_devices_API import Template_list_job
from working_directory.Template.Template_Meter_devices_API.Template_generator_relay import GeneratorRelay
from working_directory.Template.Template_Meter_devices_API.Template_generator_time import GeneratorTime
from working_directory.Template.Template_Meter_devices_API.Template_generator_meters import GenerateMeters
# ---------------------------------------------------------------------------------------------------------------------
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes

# Сделаем список из всех возможных ArchType

ArchTypes_full_list = \
    Template_list_ArchTypes.JournalValues_ArchType_name_list + \
    Template_list_ArchTypes.DigitalValues_ArchType_name_list + \
    Template_list_ArchTypes.PulseValues_ArchType_name_list + \
    Template_list_ArchTypes.ElectricPowerValues_ArchType_name_list + \
    Template_list_ArchTypes.ElectricQualityValues_ArchType_name_list + \
    Template_list_ArchTypes.ElecticEnergyValues_ArchType_name_list + \
    Template_list_ArchTypes.DigitalConfig_ArchType_name_list + \
    Template_list_ArchTypes.PulseConfig_ArchType_name_list + \
    Template_list_ArchTypes.ElectricConfig_ArchType_name_list


# ---------------------------------------------------------------------------------------------------------------------

class GeneratorJob:
    """
    Класс Генератор нашего JSON для работы с meterdev
    """
    job = {}

    def __init__(self,
                 # Тип работы - Тип данных что считываем
                 job: str,
                 # интерфейс взаимодействия
                 iface: str,
                 # Переключение реле
                 relay_state: bool = True,
                 count_time: int = 1,
                 generate_random_meter_type: bool = False,
                 address_settings: str = '192.168.202.167:777',
                 start: int = 0,
                 end: int = 0,
                 set_castrom_time=False,
                 address = "134256651"):
        self.job = {'job': job}

        # Добавляем тэг отключения реле - включения реле
        if job in Template_list_job.SetRelay_list:
            self.job["relay"] = GeneratorRelay(state=relay_state).relay

        # Теперь смотрим временные рамки
        if job in ArchTypes_full_list:
            # Если мы задаем свое время -
            if set_castrom_time:
                self.job["time"] = [{"start": start, "end": end}]
                # self.job["time"] = [{"start": start, "end": end}]
            # Если нет - то генерируем рандомно его
            else:
                self.job["time"] = GeneratorTime(count_time=count_time, measure=job).time
        # Теперь генерируем meters

        self.job["meters"] = GenerateMeters(job=job,
                                            generate_random_meter_type=generate_random_meter_type,
                                            iface=iface,
                                            port=address_settings,
                                            address=address).meters

    def get_job(self):

        return self.job
