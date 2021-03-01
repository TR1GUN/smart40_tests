# Здесь расположим Классы для разлиных запусков


# Для начала - Класс запуска через TCP\IP
# Импортируем необходимые классы Конекта
from virtualbox.library import IVirtualBox

from working_directory.Connect import Byte_coding_decoding, Connection
from working_directory.Template.Config import path_to_API

class SetupTCPIP:
    """
    Класс для работы по TCP IP

    Отдает БАЙТОВУЮ СТРОКУ который является JSON Который МЫ получиили

    ПОКА РАБОТА С ПОЛЕМ API не предусмотрена

    """

    JSON = '{}'
    API = None
    answer_JSON = None

    def __init__(self, JSON, API: str = 'test_api'):
        """
        Класс для работы по TCP IP

        Отдает БАЙТОВУЮ СТРОКУ который является JSON Который МЫ получиили

        ПОКА РАБОТА С ПОЛЕМ API не предусмотрена

        :param JSON:  Сюда пихаем наш JSON
        :param API:  ПОКА НЕ РАБОТАЕТ. ПОЛЕ НЕ ЗАПОЛНЯЕТСЯ
        """
        # Переопределяем Поля
        self.API = API
        self.JSON = JSON

        # Отправляем JSON , получаем ответ
        self.answer_JSON = self.__setup_TCP_IP()

    def __setup_TCP_IP(self):
        # Читаем наш JSON
        JSON = self.JSON
        # Переводим наш JSON в байты

        jsoninbytes = Byte_coding_decoding.to_bytes(JSON)
        # Отправляем нащ байтовый JSON на порт

        response = Connection.JSON_SendingReceiving(jsoninbytes)
        # Получаем ответ - Здесь это байтовая строка
        JSON_answer_byte = response.socket_data
        return JSON_answer_byte


# Теперь распишем класс Работы напрямую через докер
class SetupDocker:
    """
    Класс для работы с докером

    Пока что работает ТОЛЬКО С ЗАПУЩЕНЫМ ЛОКАЛЬНО докер контейнером

    Принцип такой - Ищем все запущенные докер контейнеры - Иначе - Ошибка
    """
    __filters_containers = None

    cmd = None
    JSON = '{}'
    API = None
    answer_JSON = None

    def __init__(self, JSON: str, API: str):

        """
        Класс для работы с докером

        Пока что работает ТОЛЬКО С ЗАПУЩЕНЫМ ЛОКАЛЬНО докер контейнером

        Принцип такой - Ищем все запущенные докер контейнеры - Иначе - Ошибка

        :param JSON: Принимает JSON который надо отправлять
        :param API: А сюда надо пихать апиху в стринге - ВАЖНО - используется стринга для названия самого компонента
        как он называется в самом линухе!!!!
        """

        # Запускаем Докер
        import docker

        self.JSON = JSON
        # Инициализируемся

        self.API = API

        # Инициализируем сам контейнер
        self.DockerClient = docker.from_env()

        # Получаем ВСЕ работающие контейнеры
        self.containers_running = self.__find_runinig_conteiners()

        # Чтоб не выстрелить себе в ногу проверяем - работают ли они- продолжаем только в случае если длина больше чем 0

        if len(self.containers_running) > 0:

            # Проваливаемся в первый запущенный контейнер
            self.DockerContainer = self.containers_running[0]

            # ПОЛУЧАЕМ ЧЕРЕЗ БАЙТОВЫЙ РЕЗУЛЬТАТ ВЫПОЛНЕНИЯ КОМАНДЫ ЭХО
            byte_result_tuple = self.__docker_exec(self.DockerContainer)

        # Иначе - выбрасываем ошибку подключения
        else:
            __result = ('Нет запущенных контейнеров')
            # Декодируем его в байты - это важно
            byte_result_tuple = [Byte_coding_decoding.to_bytes(content=__result)]
            byte_result_tuple = tuple(byte_result_tuple)

        # Получаем Наш байтовый массив на выход

        self.answer_JSON = byte_result_tuple[0]

    def __find_runinig_conteiners(self):

        """
        Поиск запущенных контейнеров

        :return: Возвращает список всех звапущеных контейнеров

        """
        # Смотрим Контейнеры
        DockerClient_containers = self.DockerClient.containers
        # Получаем ВСЕ работающие контейнеры

        self.__filters_containers = {'status': 'running'}
        containers_running = DockerClient_containers.list(all, filters=self.__filters_containers)

        return containers_running

    def __docker_exec(self, DockerContainer):
        """
        Метод чтоб проваливаться в контейнер

        :param DockerContainer: - Сам контейнер который у нас есть
        :return: Возвращает результат выполнения JSON
        """

        # Переназначаем команду
        cmd = self.JSON
        # Экранируем наш jSON - необходимо чтоб кавычки не пропадали
        cmd = cmd.replace('"', '\\"').strip()

        # Теперь берем и наращиваем ЭХО
        # cmd = """ echo ' """ + cmd + """   ' | etc/opt/uspd/meterdev/meterdev """
        # Сначала Получаем Ту апиху , по которой находим ее путь
        api_path = path_to_API[self.API]

        # И генерируем эту команду
        cmd = """ echo ' """ + cmd + """   ' | """ + api_path

        # Немного перенделываем команду - чтоб запускать в баше
        '/bin/sh'
        cmd2 = """ bash -c " """ + cmd + """ " """

        # Для лучшего дебага вынесем саму команду для провала в поле класса

        self.cmd = cmd2

        # print(cmd2)
        # Отправляем все в докер контейнер
        DockerContainer_exec = DockerContainer.exec_run(cmd2, stdout=True, stderr=True, stdin=False, demux=True,
                                                        tty=True, privileged=True)

        # Вытаскиваем результат
        result = DockerContainer_exec.output

        return result


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


# здесь расположим класс для работы с запуском тестов внутри линукс машины путем запуска самого компонента
class SetupInsideLauncher:
    """
     Класс для работы с запуском прямиком из линукс машины

     Работает только если запускать тесты ВНУТРИ самой машины
     """

    __filters_containers = None

    cmd = None
    JSON = '{}'
    API = None
    answer_JSON = None

    def __init__(self, JSON: str, API: str):

        """
        Класс для работы с запуском прямиком из линукс машины

        Работает только если запускать тесты ВНУТРИ самой машины

        :param JSON: Принимает JSON который надо отправлять
        :param API: А сюда надо пихать апиху в стринге - ВАЖНО - используется стринга для названия самого компонента
        как он называется в самом линухе!!!!
        """

        # импортируем нужные библиотеки для запуска

        import subprocess
        self.JSON = JSON
        # Инициализируемся
        self.API = API

        # Получаем путь до нашей АПИ
        # Сначала Получаем Ту апиху , по которой находим ее путь
        api_path = '/' + path_to_API[self.API]
        # запускаем
        process = subprocess.Popen(api_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        process.stdin.write(str.encode(self.JSON))

        data, error = process.communicate()

        self.answer_JSON = data
