"""
Функции ​​сервера:​
- принимает ​с​ообщение ​к​лиента;
- формирует ​​ответ ​к​лиенту;
- отправляет ​​ответ ​к​лиенту;
- имеет ​​параметры ​к​омандной ​с​троки:
- -p ​​<port> ​-​ ​​TCP-порт ​​для ​​работы ​(​по ​у​молчанию ​​использует ​​порт ​​7777);
- -a ​​<addr> ​-​ ​I​P-адрес ​​для ​​прослушивания ​(​по ​у​молчанию ​с​лушает ​​все ​​доступные ​​адреса).
"""
import sys
import socket
import json
from jim.config import *
from jim.utils import dict_to_bytes, bytes_to_dict, send_message, get_message


def presence_response(presence_message):
    """
    Формирование ответа клиенту
    :param presence_message: Словарь presence запроса
    :return: Словарь ответа
    """

    # Проверки
    if ACTION in presence_message and presence_message[ACTION] == PRESENCE and \
            TIME in presence_message and isinstance(presence_message[TIME], float):
        return {RESPONSE: 200}
    else:
        return {RESPONSE: 400, ERROR: 'Неверный запрос'}


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        addr = sys.argv[1]
    except IndexError:
        addr = ''

    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        print('Порт должен быть целым числом')
        sys.exit(0)

    server.bind((addr, port))
    server.listen(5)
    while True:
        client, addr = server.accept()

        presence = get_message(client)
        print(presence)

        response = presence_response(presence)
        send_message(client, response)

        client.close()