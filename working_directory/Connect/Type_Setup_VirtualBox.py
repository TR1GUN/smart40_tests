from virtualbox.library import IVirtualBox

from working_directory.Connect import Byte_coding_decoding, Connection
from working_directory.Template.Config import path_to_API

# Здесь распишем класс Работы если наша система запущена в виртуальной машине
class SetupVirtualBox:
    """
     Класс для работы с виртуальной машиной Virtual BOX

     Пока что работает ТОЛЬКО С ЗАПУЩЕНЫМ ЛОКАЛЬНО виртуальной тачкой

     Принцип такой - Ищем все запущенные докер контейнеры - Иначе - Ошибка
     """
    __filters_containers = None

    cmd = None
    JSON = '{}'
    API = None
    answer_JSON = None

    def __init__(self, JSON: str, API: str):

        """
        Класс для работы с виртуальной машиной Virtual BOX

        Пока что работает ТОЛЬКО С ЗАПУЩЕНЫМ ЛОКАЛЬНО виртуальной тачкой

        Принцип такой - Ищем все запущенные докер контейнеры - Иначе - Ошибка

        :param JSON: Принимает JSON который надо отправлять
        :param API: А сюда надо пихать апиху в стринге - ВАЖНО - используется стринга для названия самого компонента
        как он называется в самом линухе!!!!
        """


        # Запускаем апи работы с виртуальным контейнером
        import virtualbox
        self.JSON = JSON
        # Инициализируемся
        self.API = API
        # Теперь получаем наши виртуальные машины
        vbox: IVirtualBox = virtualbox.VirtualBox()

        # Ищем нашу машину
        from working_directory.ConfigParser import machine_name

        vm = vbox.find_machine(machine_name)

        # инициализируем ссесиию

        self.session = vm.create_session()

        # после чего проверяем ее статус - если она выключена  - включаем ее
        # Надо доделать - пока  отбрасываем ошибку
        if str(vm.state) in ['PoweredOff', 'Aborted']:
            __result = ('Нет запущенных контейнеров')
            # Декодируем его в байты - это важно
            byte_result_tuple = [Byte_coding_decoding.to_bytes(content=__result)]
            byte_result_tuple = tuple(byte_result_tuple)


        # Иначе - подключаемся -
        else:
            # Конектимся к нашей виртуальной тачке
            # ПОЛУЧАЕМ ЧЕРЕЗ БАЙТОВЫЙ РЕЗУЛЬТАТ ВЫПОЛНЕНИЯ КОМАНДЫ ЭХО
            byte_result = self.__connect_to_virtual_machine()

        # Получаем Наш байтовый массив на выход
        self.answer_JSON = byte_result

    def __connect_to_virtual_machine(self):

        # получаем нашу машину , и инициализируем ссесию гостевого доступа к ней
        print('lol')
        guest_session = self.session.console.guest.create_session(user="smart", password="root",
                                                                  domain='smart-VirtualBox')

        # Получаем команду что дожны отправить
        cmd = self.JSON
        # Получаем апи в которую должны отправить
        api_path = path_to_API[self.API]

        # Собираем это все
        cmd = """ echo ' """ + cmd + """   ' | """ + api_path

        # А теперь это отправляем в нашу виртуальную тачку
        process, stdout, stderr = guest_session.execute('/bin/sh', ['-c', cmd])

        result = stdout

        # Закрываем сессию - ЭТО ВАЖНО
        guest_session.close()

        # Теперь возвращаем результат

        return result