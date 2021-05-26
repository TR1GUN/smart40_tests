from working_directory.Template.Template_MeterJSON.Template_generate_meter_device_JSON import GeneratorJSON


# # -------------------------------------------------------------------------------------------------------------------
#                             Класс для Генерации нужного JSON для MeterDEV
# # -------------------------------------------------------------------------------------------------------------------


class GenerateDataForMeterDev:
    """
    этот класс нужен для генерации
    """
    job_type = []
    JSON_Meter_Dev = {}

    def __init__(self, measure_list: list = ['ElConfig', "ElMomentEnergy", 'ElArr1ConsPower']):
        self.JSON_Meter_Dev = {}
        self.job_type = measure_list
        # Получаем наш сгенерированый JSON
        self.JSON_Meter_Dev = self.__generate_data_for_Meter_Device()

    def __generate_data_for_Meter_Device(self):
        """Здесь Генерируем наши данные для MeterDev"""

        # для начала генерируем JSON который мы ожидаем
        # Для начала формируем  JSON, с которого будем считывать
        job_type = self.job_type
        JSON_answer_normal_list = []
        # Теперь что делаем - по очереди генерируем наши JSON для счетчика
        for i in range(len(job_type)):
            Answer = GeneratorJSON(measure=job_type[i]).JSON
            # Берем сам JSON
            JSON_answer_normal_list.append(Answer)

        return JSON_answer_normal_list



