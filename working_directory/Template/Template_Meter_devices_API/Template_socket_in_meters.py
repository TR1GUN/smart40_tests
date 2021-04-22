# Итак - Здесь опишем имитатор счетчика сервера

import socket
import time
from Emulator.Simulator_meter import SimulatorMeterEnergomera

from working_directory.Template.Template_Meter_devices_API.hexdump import dump
import write_file
import datetime
import threading


class SocketMeters:
    """
    Здесь инициализируем сокет нашего эмулятора счетчика чтоб обращаться к нему по Ethernet
    """
    cid = None
    port = ''
    SimulatorMeter = None
    log_file = None

    def __init__(self, conect_port):

        # Создаем файл лога
        self.log_file = write_file.write_log_file(
            file_name='EmulatorMeter_' + str(time.mktime(datetime.datetime.now().timetuple())) + str('.txt'),
            writen_text='ЛОГ обмена :', folder='Meter/')
        # Задаем Порт
        self.serv_port = None
        self.port = conect_port

        # Создаем сокет сервера
        serv_sock = self.__create_serv_sock()

        self.cid = 0
        # -----
        self.SimulatorMeter = SimulatorMeterEnergomera()

        self.__connect_socket(serv_sock)

    def __connect_socket(self, serv_sock):
        # while True:
        #     if self.cid > 0 :
        #         break
        while True:
            try:
                self.client_socket = self.__accept_client_conn(serv_sock)
            except socket.timeout:
                break
            # Производим сессию обмена инфой
            self.__session_client()
            # Добавляем еще одного пользователя
            self.cid += 1

    def __create_serv_sock(self):

        # self.SimulatorMeter = SimulatorMeterEnergomera()

        serv_sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM,
                                  proto=0)
        serv_sock.bind(('', self.port))

        serv_sock.settimeout(20.0)

        serv_sock.listen()

        return serv_sock

    # Отслеживаем Конект к сокету
    def __accept_client_conn(self, serv_sock):

        self.client_sock, client_addr = serv_sock.accept()

        # print(f'Client #{self.cid} connected '
        #       f'{client_addr[0]}:{client_addr[1]}')

        client_sock = self.client_sock
        return client_sock

    def __session_client(self):
        # Читаем запрос
        session = True
        while session:
            request = self.__read_request()

            if request is None:
                # print(f'Client #{self.cid} unexpectedly disconnected')
                session = False

            else:
                # Формируем ответ
                response = self.__handle_request(request)
                self.__write_response(response)

    # Читаем запрос

    def __read_request(self):

        request = bytearray()
        try:
            # итак что делаем - считываем Первый Пакет с сокета
            request = self.client_socket.recv(1024)

            # ЕСЛИ У НАС В ПАКЕТЕ 1
            # - 2 БАЙТА
            if len(request) == 2:
                while True:
                    chunk = self.client_socket.recv(1024)
                    request = request + chunk
                    # ЕСЛИ У НАС КОНЕЦ ПЕРЕДАЧИ
                    if len(chunk) < 1:
                        break
                    # Клиент преждевременно отключился.
                    if not chunk:
                        # print(' Клиент преждевременно отключился.')
                        break
                    break
            # ЕСЛИ У НАС ОДИН БАЙТ
            if len(request) == 1:
                chunk = self.client_socket.recv(1024)
                request = request + chunk

            # ЕСЛИ У НАС ПУСТОТА
            if len(request) < 1:
                # print(' От клиента пришло пустое значение.')
                request = None
            if not request:
                # print(' От клиента не пришло никакой информации.')
                request = None

            # Логируем
            # print('------------------------------- ЧИТАЕМ ДАННЫЕ -----------------------------------')
            self.log(chunk=request, type_packet=' Полученный ')

            # Возвращаем
            return request


        except ConnectionResetError:
            # Соединение было неожиданно разорвано.
            # print('Соединение было неожиданно разорвано.')
            return None
        except:

            # print('Неизвестная ошибка')
            #
            # print('ЧТО ПРОЧИТАЛИ\n', request)
            return None

    # обрабатывает Запрос
    def __handle_request(self, request):

        # Здесь Формируем ответ в зависимости от запроса

        response = self.SimulatorMeter.command(request)

        # response = SimulatorMeter(request=request).response
        # print('--------------------------------ОТПРАВЛЯЕМ ОТВЕТ-------------------------')
        self.log(chunk=response, type_packet=' Отправленный ')
        # return request[::-1]
        return response

    # отправляет клиенту ответ
    def __write_response(self, response):
        # Сделаем так что ответ идет массивом

        #

        self.client_socket.sendall(response)
        time.sleep(1)

    # -----------------------------------------------
    def close_socket(self):
        # Если ответа нет, закрываем сокет
        self.client_socket.close()

    def log(self, chunk, type_packet: str):
        print('\n!!!!!!!!!!', '!!!!!!!!!!!\n')
        print(type_packet + 'пакет : ', chunk, ' ')
        print(' Его длина : ', len(chunk), '')
        print('Байт код\n', chunk.hex(), '\n')
        print('ДАМП : ', dump(chunk), '')

        try:
            print('Расшифровка :', chunk.decode('ascii'), '\n')
        except UnicodeDecodeError:
            print('Не Удалось расшифровать :', chunk, '\n')

        print1 = str(type_packet) + 'пакет : ' + str(chunk) + '\n'
        print2 = ' Его длина : ' + str(len(chunk)) + '\n'

        print3 = 'ДАМП : ' + str(dump(chunk)) + '\n'

        try:
            print4 = 'Расшифровка : ' + str(chunk.decode('ascii')) + '\n'
        except UnicodeDecodeError:
            print4 = 'Не Удалось расшифровать : ' + str(chunk) + '\n'
        # логируем через файл -
        writen_text = '---------------------------------------------------------\n' + \
                      str(datetime.datetime.now()) + '\n' + \
                      print1 + print2 + print3 + print4

        write_file.append_write_log_file(file_name=self.log_file, writen_text=writen_text)

# # =========================================
# print('Полученный Пакет\n', request)
# print(' Его длина\n', len(request))
# print('ДАМП\n ', dump(request))
# try:
#     print('Расшифровка \n', request.decode('ascii'))
# except:
#     print('Не Удалось расшифровать \n', request)
# # =========================================

# import socket
# import time
# from Emulator.Simulator_meter import SimulatorMeterEnergomera
#
# from working_directory.Template.Template_Meter_devices_API.hexdump import dump
# import write_file
# import datetime
#
#
# class SocketMeters:
#     """
#     Здесь инициализируем сокет нашего эмулятора счетчика чтоб обращаться к нему по Ethernet
#     """
#     cid = None
#     port = ''
#     SimulatorMeter = None
#     log_file = None
#
#     def __init__(self, conect_port):
#
#         # Создаем файл лога
#         self.log_file = write_file.write_log_file(file_name='EmulatorMeter_' + str(time.mktime(datetime.datetime.now().timetuple())) + str('.txt'),
#                                                   writen_text='ЛОГ обмена :', folder='Meter/')
#         # Задаем Порт
#         self.serv_port = None
#         self.port = conect_port
#
#         # Создаем сокет сервера
#         serv_sock = self.__create_serv_sock()
#
#
#         self.cid = 0
#         # -----
#         self.SimulatorMeter = SimulatorMeterEnergomera()
#
#         self.__connect_socket(serv_sock)
#
#     def __connect_socket(self, serv_sock):
#         # while True:
#         #     if self.cid > 0 :
#         #         break
#
#         self.client_socket = self.__accept_client_conn(serv_sock)
#         # Производим сессию обмена инфой
#         self.__session_client()
#         # Добавляем еще одного пользователя
#         # self.cid += 1
#
#     def __create_serv_sock(self):
#
#         serv_sock = socket.socket(socket.AF_INET,
#                                   socket.SOCK_STREAM,
#                                   proto=0)
#         serv_sock.bind(('', self.port))
#
#         serv_sock.listen()
#         return serv_sock
#
#     # Отслеживаем Конект к сокету
#     def __accept_client_conn(self, serv_sock):
#
#         client_sock, client_addr = serv_sock.accept()
#
#         # print(f'Client #{self.cid} connected '
#         #       f'{client_addr[0]}:{client_addr[1]}')
#         return client_sock
#
#     def __session_client(self):
#         # Читаем запрос
#         session = True
#         while session:
#             request = self.__read_request()
#
#             if request is None:
#                 # print(f'Client #{self.cid} unexpectedly disconnected')
#                 session = False
#
#             else:
#                 # Формируем ответ
#                 response = self.__handle_request(request)
#                 self.__write_response(response)
#
#     # Читаем запрос
#
#     def __read_request(self):
#
#         request = bytearray()
#         try:
#             # итак что делаем - считываем Первый Пакет с сокета
#             request = self.client_socket.recv(1024)
#
#             # ЕСЛИ У НАС В ПАКЕТЕ 1
#             # - 2 БАЙТА
#             if len(request) == 2:
#                 while True:
#                     chunk = self.client_socket.recv(1024)
#                     request = request + chunk
#                     # ЕСЛИ У НАС КОНЕЦ ПЕРЕДАЧИ
#                     if len(chunk) < 1:
#                         break
#                     # Клиент преждевременно отключился.
#                     if not chunk:
#                         # print(' Клиент преждевременно отключился.')
#                         break
#                     break
#             # ЕСЛИ У НАС ОДИН БАЙТ
#             if len(request) == 1:
#                 chunk = self.client_socket.recv(1024)
#                 request = request + chunk
#
#             # ЕСЛИ У НАС ПУСТОТА
#             if len(request) < 1:
#                 # print(' От клиента пришло пустое значение.')
#                 request = None
#             if not request:
#                 # print(' От клиента не пришло никакой информации.')
#                 request = None
#
#             # Логируем
#             # print('------------------------------- ЧИТАЕМ ДАННЫЕ -----------------------------------')
#             self.log(chunk=request, type_packet=' Полученный ')
#
#             # Возвращаем
#             return request
#
#
#         except ConnectionResetError:
#             # Соединение было неожиданно разорвано.
#             # print('Соединение было неожиданно разорвано.')
#             return None
#         except:
#
#             # print('Неизвестная ошибка')
#             #
#             # print('ЧТО ПРОЧИТАЛИ\n', request)
#             return None
#
#     # обрабатывает Запрос
#     def __handle_request(self, request):
#
#         # Здесь Формируем ответ в зависимости от запроса
#
#         response = self.SimulatorMeter.command(request)
#
#         # response = SimulatorMeter(request=request).response
#         # print('--------------------------------ОТПРАВЛЯЕМ ОТВЕТ-------------------------')
#         self.log(chunk=response, type_packet=' Отправленный ')
#         # return request[::-1]
#         return response
#
#     # отправляет клиенту ответ
#     def __write_response(self, response):
#         # Сделаем так что ответ идет массивом
#
#         #
#
#         self.client_socket.sendall(response)
#         time.sleep(1)
#
#     # -----------------------------------------------
#     def close_socket(self):
#         # Если ответа нет, закрываем сокет
#         self.client_socket.close()
#
#     def log(self, chunk, type_packet: str):
#         print('\n!!!!!!!!!!', '!!!!!!!!!!!\n')
#         print(type_packet + 'пакет : ', chunk, ' ')
#         print(' Его длина : ', len(chunk), '')
#         print('Байт код\n', chunk.hex(), '\n')
#         print('ДАМП : ', dump(chunk), '')
#
#         try:
#             print('Расшифровка :', chunk.decode('ascii'), '\n')
#         except UnicodeDecodeError:
#             print('Не Удалось расшифровать :', chunk, '\n')
#
#         print1 = str(type_packet) + 'пакет : ' + str(chunk) + '\n'
#         print2 = ' Его длина : ' + str(len(chunk)) + '\n'
#
#         print3 = 'ДАМП : ' + str(dump(chunk)) + '\n'
#
#         try:
#             print4 = 'Расшифровка : ' + str(chunk.decode('ascii')) + '\n'
#         except UnicodeDecodeError:
#             print4 = 'Не Удалось расшифровать : ' + str(chunk) + '\n'
#         # логируем через файл -
#         writen_text = '---------------------------------------------------------\n' + \
#                       str(datetime.datetime.now()) + '\n'  + \
#                       print1 + print2 + print3 + print4
#
#         write_file.append_write_log_file(file_name=self.log_file, writen_text=writen_text)
#
# # # =========================================
# # print('Полученный Пакет\n', request)
# # print(' Его длина\n', len(request))
# # print('ДАМП\n ', dump(request))
# # try:
# #     print('Расшифровка \n', request.decode('ascii'))
# # except:
# #     print('Не Удалось расшифровать \n', request)
# # # =========================================
