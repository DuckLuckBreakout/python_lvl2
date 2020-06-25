import time
from pytest import raises
from client.main import create_presence, translate_message
from errors.errors import UsernameTooLongError, ResponseCodeLenError, MandatoryKeyError, ResponseCodeError


# МОДУЛЬНЫЕ ТЕСТЫ
def test_create_presence():
    # без параметров
    message = create_presence()
    assert message['action'] == "presence"
    # берем разницу во времени
    assert abs(message['time'] - time.time()) < 0.1
    assert message["user"]["account_name"] == 'Guest'
    # с именем
    message = create_presence('test_user_name')
    assert message["user"]["account_name"] == 'test_user_name'
    # неверный тип
    with raises(TypeError):
        create_presence(200)
    with raises(TypeError):
        create_presence(None)
    # Имя пользователя слишком длинное
    with raises(UsernameTooLongError):
        create_presence('11111111111111111111111111')


def test_translate_message():
    # неправильный тип
    with raises(TypeError):
        translate_message(100)
    # неверная длина кода ответа
    with raises(ResponseCodeLenError):
        translate_message({'response': '5'})
    # нет ключа response
    with raises(MandatoryKeyError):
        translate_message({'one': 'two'})
    # неверный код ответа
    with raises(ResponseCodeError):
        translate_message({'response': 700})
    # все правильно
    assert translate_message({'response': 200}) == {'response': 200}





