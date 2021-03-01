from working_directory.Connect import Byte_coding_decoding, Connection
from working_directory.Template.Config import path_to_API

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