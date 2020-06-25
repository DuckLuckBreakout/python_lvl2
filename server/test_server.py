import time
from server.functions import *


def test_presence_response():
    # Нет ключа action
    assert presence_response({'one': 'two', 'time': time.time()}) == {'response': 400, 'error': 'Не верный запрос'}
    # Нет ключа time
    assert presence_response({'action': 'presence'}) == {'response': 400, 'error': 'Не верный запрос'}
    # Ключ не presence
    assert presence_response({'action': 'test_action', 'time': 1000.10}) == {'response': 400,
                                                                             'error': 'Не верный запрос'}
    # Кривое время
    assert presence_response({'action': 'presence', 'time': 'test_time'}) == {'response': 400,
                                                                              'error': 'Не верный запрос'}
    # Всё ок
    assert presence_response({'action': 'presence', 'time': 1000.10}) == {'response': 200}
