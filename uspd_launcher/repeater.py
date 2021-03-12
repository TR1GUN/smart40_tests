#
# import time
# import socket
# import sys
#
#
# input = sys.stdin
# line_full = ''
# for line in sys.stdin:
#     line_full = line_full + line
#
# a = open('/var/opt/uspd/meterdb/log.txt', 'w')
# a.write(line_full)
# a.close()
#
# json = sys.argv[0]
# output = sys.stdout
#
# output.write(json)
# output.write(input)
# print('lol')

# import asyncio
# import serial
#
# found = False
#
# for i in range(64):
#     try:
#         port = "/dev/ttyS%d" % i
#         ser = serial.Serial(port)
#         ser.close()
#         print
#         "Найден последовательный порт: ", port
#         found = True
#     except serial.serialutil.SerialException:
#         pass
#
# if not found:
#     print
#     "Последовательных портов не обнаружено"


import socket
import sys
import time


# Создаем Серверный сокет
def create_serv_sock(serv_port):
    serv_sock = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM,
                              proto=0)
    serv_sock.bind(('', serv_port))
    serv_sock.listen()
    return serv_sock


# Запускаем сервер
def run_server(port=777):
    # Создаем сокет сервера
    serv_sock = create_serv_sock(port)
    cid = 0
    # постоянно ожидает клиентские подключения
    while True:
        client_sock = accept_client_conn(serv_sock, cid)
        serve_client(client_sock, cid)
        cid += 1


# Отслеживаем Конект к сокету
def accept_client_conn(serv_sock, cid):
    client_sock, client_addr = serv_sock.accept()
    print(f'Client #{cid} connected '
          f'{client_addr[0]}:{client_addr[1]}')
    return client_sock

# Получив новое соединение, сервер вычитывает запрос
def serve_client(client_sock, cid):
    request = read_request(client_sock)
    if request is None:
        print(f'Client #{cid} unexpectedly disconnected')
    else:
        print('------------------------------')
        print('request',request)
        print('------------------------------')
        # Формируем ответ
        response = handle_request(request)

        print('ответ ',response )
        write_response(client_sock, response, cid)




# Читаем запрос
def read_request(client_sock, delimiter=b'!'):
    request = bytearray()
    try:
        while True:
            chunk = client_sock.recv(4)
            if not chunk:
                # Клиент преждевременно отключился.
                print(' Клиент преждевременно отключился.')
                return None
            request += chunk
            if delimiter in request:
                print('Успешно прочитали информацию с сокета')
                return request

    except ConnectionResetError:
        # Соединение было неожиданно разорвано.
        print('Соединение было неожиданно разорвано.')
        return None
    except:
        print('Неизвестная ошибка')
        return None


# обрабатывает Запрос
def handle_request(request):
    # time.sleep(5)
    return request[::-1]
    # return request


# отправляет клиенту ответ
def write_response(client_sock, response, cid):
    client_sock.sendall(response)
    client_sock.close()
    # print(f'Client #{cid} has been served')


# int(sys.argv[1])

# if __name__ == '__main__':
# run_server(port=777)

from working_directory.Template.Template_Meter_devices_API.Template_socket_in_meters import SocketMeters
server = SocketMeters(conect_port=7777)


