import time
from jim.config import *
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
