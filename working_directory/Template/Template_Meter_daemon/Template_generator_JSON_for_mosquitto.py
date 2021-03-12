# Здесь Собираем наш JSON для задания в mosquitto
from working_directory.Template.Template_Meter_daemon.Template_Record_MeterTable import GenerateRecordMeterTable


class GenerateForMosquittoJSON:
    job_type = None
    generate_count = 1
    count_tree = None
    type_connect = None
    type_meter = None
    address_meter = None
    adress = None
    InterfaceConfig = None

    jobs = {}
    DeviceIdx_list = []
    def __init__(self,
                 job_type: list = ['ElConfig'],
                 # Количество добавляемых записей
                 generate_count: int = 1,
                 # Количество элементов в дереве подключения
                 count_tree: int = 2,
                 # тип конекта
                 type_connect: str = 'Ethernet',
                 # Имя счетчика - Берется из БД
                 type_meter: str = 'SE303',
                 # Серийник нашего счетчика
                 address_meter: str = "141227285",
                 # Первичный Адресс счетчика\Хаба
                 adress: str = "192.168.202.146:7777",
                 # uart_tag
                 InterfaceConfig: str = "9600,8n1"):
        # переопределяем тэги

        self.job_type = job_type
        self.generate_count = generate_count
        self.count_tree = count_tree
        self.type_connect = type_connect
        self.type_meter = type_meter
        self.address_meter = address_meter
        self.adress = adress
        self.InterfaceConfig = InterfaceConfig

        # Получаем нащ словарь JSON
        self.jobs = self.__generate_JSON()

    def __generate_JSON(self):
        '''Здесь генерируем наш JSON'''

        JSON_dict = \
            {
                "jobs": self.job_type,
                "meters": self.__generate_meter_list()
            }

        return JSON_dict

    def __generate_meter_list(self):
        """Здесь - Генерируем наши АЙДИШНИКИ СЧЕТЧИКОВ ЧТО НУЖНО ОПРОСИТЬ"""
        Generate_Record_Meter = GenerateRecordMeterTable(
                                                            generate_count=self.generate_count,
                                                            count_tree=self.count_tree,
                                                            type_connect=self.type_connect,
                                                            type_meter=self.type_meter,
                                                            address_meter=self.address_meter,
                                                            adress=self.adress,
                                                            InterfaceConfig=self.InterfaceConfig
                                                        )

        self.DeviceIdx_list = Generate_Record_Meter.DeviceIdx_list

        return Generate_Record_Meter.MeterId_list

# -------------------------------------------------------------------------------------------------------------------


