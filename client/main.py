"""
Функции ​к​лиента:​
- сформировать ​​presence-сообщение;
- отправить ​с​ообщение ​с​ерверу;
- получить ​​ответ ​с​ервера;
- разобрать ​с​ообщение ​с​ервера;
- параметры ​к​омандной ​с​троки ​с​крипта ​c​lient.py ​​<addr> ​[​<port>]:
- addr ​-​ ​i​p-адрес ​с​ервера;
- port ​-​ ​t​cp-порт ​​на ​с​ервере, ​​по ​у​молчанию ​​7777.
"""

import sys
import socket
import time
from jim.config import *
from jim.utils import send_message, get_message
from errors.errors import UsernameTooLongError, ResponseCodeLenError, MandatoryKeyError, ResponseCodeError


def create_presence(account_name='Guest'):
    """
    Сформировать presence-сообщение
    :param account_name: Имя пользователя
    :return: Словарь сообщения
    """

    # Если имя не строка
    if not isinstance(account_name, str):
        raise TypeError
    # Если длина имени пользователя больше 25 символов
    if len(account_name) > 25:
        raise UsernameTooLongError(account_name)

    msg = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }

    return msg


def translate_message(response):
    """
    Разбор сообщения
    :param response: Словарь ответа от сервера
    :return: корректный словарь ответа
    """

    # Передали не словарь
    if not isinstance(response, dict):
        raise TypeError
    # Нету ключа response
    if RESPONSE not in response:
        raise MandatoryKeyError(RESPONSE)

    code = response[RESPONSE]

    # длина кода не 3 символа
    if len(str(code)) != 3:
        # Ошибка неверная длина кода ошибки
        raise ResponseCodeLenError(code)
    # неправильные коды символов
    if code not in RESPONSE_CODES:
        # ошибка неверный код ответа
        raise ResponseCodeError(code)

    return response


if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = 'localhost'

    try:
        port = int(sys.argv[2])
    except IndexError:
        port = 7777
    except ValueError:
        print('Порт должен быть целым числом')
        sys.exit(0)

    client.connect((addr, port))

    presence = create_presence()
    send_message(client, presence)

    response = get_message(client)
    response = translate_message(response)

    print(response)