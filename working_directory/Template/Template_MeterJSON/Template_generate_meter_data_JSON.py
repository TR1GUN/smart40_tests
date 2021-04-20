# Здесь Продублируем классы генерации различных вариаций наших JSON
from working_directory.Template.Template_MeterJSON.Template_generator_field_measures import GeneratorMeasures
from copy import deepcopy


# # -----------------------------------------------------------------------------------------------------
#                             Наш великий и ужасный Генератор JSON
# # -----------------------------------------------------------------------------------------------------


class GeneratorJSON:
    '''
    Великий и Ужасный генератор JSON для всех возможных комбинаций
    '''

    JSON_Meter_data_POST = {}
    JSON_Meter_data_GET = {}

    JSON = {}

    measure = []
    count_ts = 0
    count_id = 0
    Castrom_Value = {}

    def __init__(self,
                 # ТИП ДАННЫХ ПОД КОТОРЫЙ ПРОВОДИМ ГЕНЕРАЦИЮ
                 measure: list,
                 # ОЧЕНЬ ВАЖНЫЙ ЭЛЕМЕНТ -УКАЗАТЕЛЬ ГЕНЕРАЦИИ УНИКАЛЬНОГО ВРЕМЕНИ
                 #  ЕСЛИ У НАС БУЛЕВЫЙ МАРКЕР - ТО ЛИБО ДА ЛИБО НЕТ ГЕНЕРАЦИЯ УНИКАЛЬНОГО РАНДОМНОГО TS
                 # КОЛИЧЕСТВО МОМЕНТОВ ВРЕМЕНИ - ЕТО ВАЖНА- В ПОСЛЕДВСТВИИ ВЛИЯЕТ НА ДЛИНУ JSON
                 # ЕСЛИ У НАС СПИСОК , ТО ПОДСТАВЛЯЕМ ВСЕ ЗНАЧЕНИЯ ИЗ ЭТОГО СПИСКА,
                 count_ts: int = 3 or list,

                 # КОЛИЧЕСТВО АЙДИШНИКОВ - ЕТО ВАЖНА- В ПОСЛЕДВСТВИИ ВЛИЯЕТ НА ДЛИНУ JSON -
                 # ИЛИ КОСТРОМНЫЕ АЙДИШНИКИ ЧТО СПУЦСКАЕМ СВЕРХУ
                 count_id: int = 3 or list,

                 # КАСТРОМНЫЕ ТЭГИ
                 Castrom_Value: dict = {}):
        # Переопределяем тэги
        self.JSON_Meter_data_POST = {}
        self.JSON_Meter_data_GET = {}
        self.JSON = {}
        self.measure = 0
        self.count_ts = 0
        self.count_id = 0



        self.measure = measure
        self.count_ts = count_ts
        self.count_id = count_id
        self.Castrom_Value = Castrom_Value



        # Теперь берем и генерируем ЭТАЛОННЫЙ JSON ,без всякой шушеры

        self.JSON = GeneratorMeasures(measure=self.measure,
                                      count_ts=self.count_ts,
                                      count_id=self.count_id,
                                      Castrom_Value=self.Castrom_Value).json

        # Теперь взависимости от ТЭГОВ - Собираем наш JSON

    def Generator_JSON_for_Meter_data_POST(self):
        """
        Генератор для выстраивания нашего замечательного post запроса к Meter data
        :return:

        """

        # Импортируем наш миноукладчик
        from working_directory.Template.Template_Meter_db_data_API.JSON_for_Meter_db_data_API import POST

        # Производим генерицаю по копии
        self.JSON_Meter_data_POST = POST(measures=deepcopy(self.JSON)).get_JSON_dict()

        return deepcopy(self.JSON_Meter_data_POST)

    def Generator_JSON_for_Meter_data_GET(self,
                                          count_tags: int or list,

                                          select_device_idx: bool = True,

                                          select_meter_id: bool = True,

                                          select_id_all: bool = False,

                                          select_last_time: bool = False,

                                          out_of_bounds: bool = False,

                                          serial: bool = False,

                                          select_count_ts: int = 1,

                                          select_count_id: int = 1):
        """
        Генератор для get запроса

        :param JSON: - JSON с помощью которого вставили данные в БД
        :param count_tags: - int, list  Количество тэгов или список тэгов которые попадут в JSON
        :param select_device_idx: - bool Маркер селекта по device_idx - внутрений айдишник -
        :param select_meter_id: - bool Маркер селекта по meter_id - внешний айдишник
        :param select_id_all: - bool Маркер селекта всего что есть.
                                    Взаимоисключающий с select_meter_id, select_device_idx и serial
        :param select_last_time: -bool Маркер селекта последнего времени.
                                        Взаимоисключающий с select_count_ts и out_of_bounds
        :param out_of_bounds: -bool Маркер выхода за границы существующего времени - Важен для настройки лимита времени
        :param serial: -bool Маркер селекта по serial - серийный номер в config
        :param select_count_ts: -int Количество отрезков времени , которые запрашиваем
        :param select_count_id: -int Количество Id которые запрашиваем

        """

        # Импортируем наш миноукладчик
        from working_directory.Template.Template_Meter_db_data_API.JSON_for_Meter_db_data_API import GET
        from working_directory.Template.Template_Meter_db_data_API.Template_generator_get_by_meansures import \
            GeneratorGetRequest
        # После чего генерируем JSON запроса
        JSON_Meter_data_GET = GeneratorGetRequest(JSON=self.JSON,
                                                  count_tags=count_tags,
                                                  select_device_idx=select_device_idx,
                                                  select_meter_id=select_meter_id,
                                                  select_id_all=select_id_all,
                                                  select_last_time=select_last_time,
                                                  out_of_bounds=out_of_bounds,
                                                  serial=serial,
                                                  select_count_ts=select_count_ts,
                                                  select_count_id=select_count_id).JSON

        # Производим генерицаю по копии
        self.JSON_Meter_data_GET = GET(measures=deepcopy(JSON_Meter_data_GET)).get_JSON_dict()

        return deepcopy(self.JSON_Meter_data_GET)
