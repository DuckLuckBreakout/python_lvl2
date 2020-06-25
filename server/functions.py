from jim.config import *


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