
from working_directory.Template.Template_MeterJSON.Template_generator_field_ts import GeneratorValsByDevices
from working_directory.Template.Template_MeterJSON.Template_generator_random_device_idx import GeneratorDeviceIdx
from copy import deepcopy

# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
#                                 ГЕНЕРАТОР МАССИВА ДЛЯ IDx
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
class GeneratorIdDevices:
    """
    Конструктор для генерации id в готовое json представление.
    """
    # НАШ Генерируемый массив
    devices = []
    # Число сколько генерируем айдишников или готовые айдишники
    count_id = 0,
    # Тип переменной для которой генерируем
    measure = 'measure',
    # Количество таймстампов или готовые таймстампы
    count_ts = 0,
    # КАСТРОМНЫЕ ТЭГИ
    Castrom_Value = {}

    # Конструктор для генерации тэгов - очень важно - принимает строковые значения
    def __init__(self,
                 # ОЧЕНЬ ВАЖНЫЙ ЭЛЕМЕНТ -УКАЗАТЕЛЬ ГЕНЕРАЦИИ УНИКАЛЬНОГО ВРЕМЕНИ
                 #  ЕСЛИ У НАС БУЛЕВЫЙ МАРКЕР - ТО ЛИБО ДА ЛИБО НЕТ ГЕНЕРАЦИЯ УНИКАЛЬНОГО РАНДОМНОГО TS
                 #  ЕСЛИ У НАС СПИСОК , ТО ПОДСТАВЛЯЕМ ВСЕ ЗНАЧЕНИЯ ИЗ ЭТОГО СПИСКА,

                 # ТИП ДАННЫХ ПОД КОТОРЫЙ ПРОВОДИМ ГЕНЕРАЦИЮ
                 measure: str,

                 # КОЛИЧЕСТВО МОМЕНТОВ ВРЕМЕНИ - ЕТО ВАЖНА- В ПОСЛЕДВСТВИИ ВЛИЯЕТ НА ДЛИНУ JSON
                 count_ts: int = 2 or list,

                 # КОЛИЧЕСТВО АЙДИШНИКОВ - ЕТО ВАЖНА- В ПОСЛЕДВСТВИИ ВЛИЯЕТ НА ДЛИНУ JSON
                 count_id: int = 3 or list,

                 # КАСТРОМНЫЕ ТЭГИ
                 Castrom_Value: dict = {}
                 ):

        # Переопределяем
        self.measure = measure
        self.count_ts = count_ts
        self.count_id = count_id
        self.Castrom_Value = Castrom_Value

        self.devices = self.__generate_ids()

    #     здесь пропишем генератор для айдишников - ОЧЕЕЕНЬ ВАЖНОЕ, ДА

    def __generate_ids(self):

        count_id = self.count_id
        measure = self.measure
        count_ts = self.count_ts

        # для начала мы должны определиться - мы генерируем уникальные id или используем уже сгенерированные
        # После чего Включачем наш генератор
        # Теперь это вставляем в генератор

        # ЕСЛИ У НАС ДАНЫ АЙДИШНИКИ
        value_id_list = []
        if type(count_id) == list:
            # ДЕЛАЕМ ИЗ НИХ СПИСОК ТАК СЛОВНО ИХ МЫ ЗАСЕЛЕКТИЛИ , ЛОЛ
            for i in range(len(count_id)):
                value_id_list.append({'DeviceIdx': count_id[i]})

        elif type(count_id) == int:
            value_id_list = GeneratorDeviceIdx(count_id=count_id).id

        # Генерируем время
        devices_ids_list = []
        # Если список пустои - То мы берем и делаем его ноном
        if len(value_id_list) == 0:
            devices_ids_list = None
        # Иначе - Генерируем айдишники
        else:
            # Теперь тут генируруем айдишники отталкиваясь от заданного максимального значения
            for i in range(len(value_id_list)):
                devices = {}
                vals = GeneratorValsByDevices(measure=measure,
                                              count_ts=count_ts,
                                              Castrom_Value=self.Castrom_Value)


                # Сюда пихаем ID
                devices['id'] = value_id_list[i]['DeviceIdx']
                devices['vals'] = deepcopy(vals.vals)
                devices_ids_list.append(devices)

        return devices_ids_list
