# Здесь расположим обработчик ошибок
from working_directory.Template.Template_Meter_db_data_API import Template_list_ArchTypes
from working_directory.Template.Template_Meter_devices_API import Template_list_job
from working_directory.Template.Template_Meter_devices_API import Template_deconstruct_json
from working_directory.Template.Template_Meter_devices_API import Template_CheckUp_JSON_from_MeterDev
from working_directory.Template.Template_Meter_devices_API.Template_generator_answer_for_meterdev_job import \
    CompletionSupposedAnswer


class ErrorHeandler:
    """
    Класс обработчик ошибок , чо б нет
    """

    JSON = None
    error_collector = None
    JSON_deconstruct = None
    JSON_answer_normal = None
    job_type = None
    JSON_etalon_deconstruct = None

    # Все типы данных из айрч тип нейм
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

    # ВСЕ типы данных которые добавлены в этой апи
    Set_job_list = Template_list_job.GetTime_list + \
                   Template_list_job.SetTime_list + \
                   Template_list_job.SyncTime_list + \
                   Template_list_job.GetRelay_list + \
                   Template_list_job.SetRelay_list + \
                   Template_list_job.GetSerial_list

    # Тип данных в которых нет таймштампа
    Job_not_time_list = Template_list_job.GetSerial_list

    # Список типов работ котоые считывают поля time
    Get_job_not_key_ts_list = \
        Template_list_job.GetTime_list + \
        Template_list_job.GetRelay_list

    # все типы данных которые имеют
    # Set_job_not_key_ts_list = \
    #     Template_list_job.SetTime_list + Template_list_job.SetRelay_list

    # Все типы данных которые не имеют поля дата
    Job_not_data_list = Template_list_job.SyncTime_list

    def __init__(self, JSON, job_type: str, JSON_answer_normal=None):

        self.job_type = job_type
        self.JSON = JSON
        self.error_collector = []
        self.JSON_deconstruct = []
        self.JSON_etalon = JSON_answer_normal

        # Итак - Сначла опускаем на валидацию\деконструкцию наш основной JSON

        self.JSON_deconstruct = self.__deconstruct_JSON(self.JSON)

        # Если у нас есть эталонный JSON , то опускаем его сравнивать с ним
        if JSON_answer_normal is not None:
            # Теперь проверяем есть ли ошибки при валидации
            if len(self.error_collector) == 0:
                # Достраиваем наш JSON эталонный JSON ответа
                JSON_answer_normal = CompletionSupposedAnswer(measure=job_type,
                                                              JSON_answer=JSON,
                                                              JSON_supposed=JSON_answer_normal).JSON_normal
                # Опускаем его в деконструктор

                self.JSON_etalon_deconstruct = self.__deconstruct_JSON(JSON_answer_normal)

                # А теперь очень важный момент - для моментных показателей - ставим все в нулину
                # А теперь отправляем в сравниватель
                self.error_collector = Template_CheckUp_JSON_from_MeterDev.CheckUp(
                    JSON_Normal=self.JSON_etalon_deconstruct,
                    JSON_answer=self.JSON_deconstruct
                ).Error_collector
            # Если есть ошибки при валидации - возвращаем ее

    def __deconstruct_JSON(self, JSON):

        """
        Наш метод для хорошей деконструкции JSON

        :return:
        """

        # Определянем тип JSON и если надо производим его деконструкцию
        job_type = self.job_type

        error_collector = []
        JSON_deconstruct = []

        # Если У нас archtype
        if job_type in self.ArchTypes_full_list:
            # Проводим деконструкцию
            Deconstruct = Template_deconstruct_json.Deconstruct(JSON=JSON)
            # Если валидация успешна
            if Deconstruct.Valid:
                JSON_deconstruct = Deconstruct.JSON_deconstruct
            else:
                error_collector = Deconstruct.error
            del Deconstruct

        # Если у нас джоб с полем дата , но без таймштампа
        if job_type in self.Job_not_time_list:
            # Проводим деконструкцию по дочернему классу без определения времени
            Deconstruct = Template_deconstruct_json.DeconstructGetSerial(JSON=JSON)
            # Если валидация успешна
            if Deconstruct.Valid:
                JSON_deconstruct = Deconstruct.JSON_deconstruct
            else:
                error_collector = Deconstruct.error
            del Deconstruct

        # if job_type in Get_job_not_key_ts_list:
        #     # Проводим деконструкцию по дочернему классу без определения времени
        #     Deconstruct = Template_deconstruct_json.Deconstruct(JSON=JSON)
        #     # Если валидация успешна
        #     if Deconstruct.Valid:
        #         JSON_deconstruct = Deconstruct.JSON_deconstruct
        #     else:
        #         error_collector = Deconstruct.error

        # if job_type in Set_job_not_key_ts_list:
        #     Deconstruct = Template_deconstruct_json.DecostructSetType(JSON=JSON)
        #     # Если валидация успешна
        #     if Deconstruct.Valid:
        #         JSON_deconstruct = Deconstruct.JSON_deconstruct
        #     else:
        #         error_collector = Deconstruct.error

        # Если у нас data по умолчанию none - например синхронизация времени
        if job_type in self.Job_not_data_list:
            # не производим деконструкцию , а сразу можно проверить
            JSON_deconstruct = [JSON]

        self.error_collector = error_collector

        return JSON_deconstruct
