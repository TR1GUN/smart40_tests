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

    def __init__(self, measure_list: list = ['ElConfig', "ElMomentEnergy", 'ElArr1ConsPower'], count_timestamp=None):
        self.JSON_Meter_Dev = {}
        self.job_type = measure_list
        # Получаем наш сгенерированый JSON
        self.JSON_Meter_Dev = self.__generate_data_for_Meter_Device(count_timestamp=count_timestamp)

    def __generate_data_for_Meter_Device(self, count_timestamp):
        """Здесь Генерируем наши данные для MeterDev"""

        # для начала генерируем JSON который мы ожидаем
        # Для начала формируем  JSON, с которого будем считывать
        job_type = self.job_type
        JSON_answer_normal_list = []
        # Теперь что делаем - по очереди генерируем наши JSON для счетчика

        for i in range(len(job_type)):

            Answer = GeneratorJSON(measure=job_type[i], count_timestamp=count_timestamp.get(i)).JSON
            # Берем сам JSON
            JSON_answer_normal_list.append(Answer)

        return JSON_answer_normal_list

    def _get_count_timestamp(self, job_type):
        """
        Здесь ищем Нужное колисчетво таймштампов
        :param job_type:
        :return:
        """
        pass
