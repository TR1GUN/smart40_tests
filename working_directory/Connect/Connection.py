import socket
import time
from working_directory import ConfigParser
# from sys import getsizeof
# -----------------------------------------------------------------------


class ConnectSocket:
    """
    Класс подключения к нашей виртуалке
    для конструктора обязательно нужен адресс
    в конструкторе по умолчанию прописан адрес из Конфига
    после чего производится подключение - Если подключение неудачно, то выдается FALSE
    """
    connection_socket = None;

    def __init__(self, address = ConfigParser.targetimage):
        self.connection_socket = self.__socket_connection(address)

    # функция коннекта
    def __socket_connection(self, address):
        # открываем сокет
        self.socket_connect = socket.socket()
        # self.socket_connect.settimeout(10)
        # Конектимся по указанному адресу - принимает только коректное значение - кортежи, строки , байты - аккуратнее
        try:
            self.socket_connect.connect(address)
            # Сделал обработчиком - если не удается подключится - выбрасываем значение false

        except:
            print('Неправильно задан порт')
            self.socket_connect = False

        finally:
            if self.socket_connect == False:
                print('Не удалось подключится')
            else:
                return self.socket_connect
# -----------------------------------------------------------------------

class JSON_SendingReceiving:
    """
    Класс который отвечает за отправку-получение данных по сокету.
    Использует сокет который подключает из класса ConnectSocket
    -
    Для работы необходимо выдать байтовый JSON!!!
    """

    # Информация чистым JSON в байтовом виде. Доступна после инициализации класса
    socket_data = None

    def __init__(self, json_byte):
        self.socket_data = self.__JSON_sending_receive(json_byte)

    # Метод для вызова открытия порта
    def __connect(self):
        # Делаем Экземпляр класса
        socket = ConnectSocket()
        return socket.connection_socket

    # Метод для отправки-Приёма JSON
    def __JSON_sending_receive(self, json_byte):
        # для начала открываем сокет
        socket_sending_receive = self.__connect()


        # оправляем пакет
        socket_sending_receive.sendall(json_byte)
        # получаем пакет
        socket_sending_receive.shutdown(socket.SHUT_WR)

        # немного ждем перед чтением всех данных. по возможности сделать умнее
        time.sleep(1)
        data_full = b''
        while True:

            data = socket_sending_receive.recv(1024)

            data_full += data


            if not data:
            # избегаем RST.
            # https://stackoverflow.com/questions/42611333/why-is-there-tcp-rst-packet-after-sending-a-string-and-closing-a-socket
                socket_sending_receive.close()
                break
        # Получаем размер нашей переменой в байтах
        # lol = getsizeof(data_full)
        # time.sleep(1)
        # print('bytes',lol)
        return data_full
