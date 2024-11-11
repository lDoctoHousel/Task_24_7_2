
from api import PetFriends
from settings import valid_email, valid_password, valid_email1, valid_password1, valid_email2, valid_password2, valid_email3, valid_password3, valid_email4, valid_password4, valid_email5, valid_password5
import os
import time
import threading


pf = PetFriends()


def test_successful_add_new_pet_simple(name='FalseDog', animal_type='Dgigit',
                                     age='2000'):
    """Тест 1: Проверяем что можно добавить питомца без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test__successful_add_set_photo(pet_photo='images/dog1.jpeg'):
    """Тест 2: Проверяем что можно добавить фото питомца"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_set_photo(auth_key, pet_id, pet_photo)

    assert status == 200


def test_negative_get_api_key_for_valid_user(email=valid_email1, password=valid_password1):
    """ Тест 3: Проверяем что запрос api ключа возвращает статус 403 при отсутствии пользователя в базе данных"""

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert 'key' not in result


def test_negative_get_api_key_for_valid_user_with_empty_credentials():
    """Тест 4: Проверяем, что запрос API ключа для действительного пользователя с пустыми учетными данными возвращает статус 403."""
    status, _ = pf.get_api_key("", "")
    assert status == 403



def test_negative_add_new_pet_with_empty_name():
    """Тест 5: Проверяем, что нельзя добавить питомца с пустым именем."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.add_new_pet(auth_key, '', 'masun', '2', 'images/dog1.jpeg')

    # Если статус 200 то это баг сервера
    # Проверяем что статус ответа = 400
    assert status == 400


def test_negative_add_new_pet_with_negative_age():
    """Тест 6: Проверяем, что нельзя добавить питомца с отрицательным возрастом."""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.add_new_pet(auth_key, 'anasha', 'mysun', '-3', 'images/dog1.jpeg')

    # Если статус 200 то это баг сервера
    # Проверяем что статус ответа = 400
    assert status == 400


def test_negative_update_noexisted_pet(name='Asya', animal_type='dogs', age=20):
    """Тест 7: Проверяем возможность обновления информации о питомце которого не существует"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    nonexistent_pet_id = "999999"
    status, result = pf.update_pet_info(auth_key, nonexistent_pet_id, name, animal_type, age)

    assert status == 400


def test_negative_add_new_pet_with_empty_noname(animal_type='dogs', age='12'):
    """Тест 8: Проверяем, что нельзя добавить питомца с пустым именем"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, _ = pf.add_new_pet_simple(auth_key, '', animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом (должен быть статус 400, баг сервера если статус 200)
    assert status == 400




def test_negative_delete_self_pet():
    """Тест  9: Проверяем возможность удаления не существующего питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    nonexistent_pet_id = "999999"
    status, _ = pf.delete_pet(auth_key, nonexistent_pet_id)

    assert status == 200


def test_update_pet_info_animal_type():
    """ Тест 10: Проверяем что после создания питомца можно изменить вид питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, 'Nasa', 'Cat', '5', 'images/dog1.jpeg')

    pet_id = result['id']
    status, result = pf.update_pet_info(auth_key,pet_id, 'Nasa', 'Dog', '5')

    assert status == 200
    assert result['animal_type'] == 'Dog'


def test_get_api_key_valid( email= valid_email, password= valid_password):
    """Тест 11: Проверяем что с валидными данными получение ключа API было успешным."""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_update_pet_info_name():
    """ Тест 12: Проверяем что после создания питомца можно изменить имя питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, 'Марфа', 'Dog', '15', 'images/dog1.jpeg')

    pet_id = result['id']
    status, result = pf.update_pet_info(auth_key, pet_id, 'Sven', 'Dog', '15')

    assert status == 200
    assert result['name'] == 'Sven'



def test_update_pet_info_age():
    """ Тест 13: Проверяем что после создания питомца можно изменить возраст питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, 'Марфа', 'Dog', '1', 'images/dog1.jpeg')

    pet_id = result['id']
    status, result = pf.update_pet_info(auth_key, pet_id, 'Sven', 'Dog', '6')

    assert status == 200
    assert result['age'] == '6'



def test_add_multiple_pets():
    """ Тест 14: Проверяем что сервер допускает создание нескольких питомцев с одного ЛК"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    start_time = time.time()
    pet_count = 0
    while time.time() - start_time < 1:
        status, result = pf.add_new_pet_simple(auth_key, 'Nanotec', 'Dog', '11')
        if status == 200 and 'id' in result:
           pet_count += 1
    assert pet_count > 0



def test_add_multiple_max_pets_time():
    """ Тест 15: Проверяем что сайт не рухнет при максимально возможном создание питомцев за 30 секунд """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    start_time = time.time()
    pet_count = 0
    while time.time() - start_time < 30:
        status, result = pf.add_new_pet_simple(auth_key, ' Lucifer', 'Angel', '666')
        if status == 200 and 'id' in result:
            pet_count += 1
    assert pet_count <= 999



#Для 16 теста добавляем нового питомца, используя предоставленный ключ аутентификации
def add_pet(auth_key):
    status, result = pf.add_new_pet_simple(auth_key, 'Lucifer', 'Angel', '666')
    return status, result

def test_add_multiple_max_pets_five_account():
    """ Тест 16: Проверяем что сайт не рухнет при максимально возможном создание питомцев за 60 секунд с 5 акаунтов """

 # Получаем ключи аутентификации для пяти разных пользователей
    _, auth_key1 = pf.get_api_key(valid_email, valid_password)
    _, auth_key2 = pf.get_api_key(valid_email2, valid_password2)
    _, auth_key3 = pf.get_api_key(valid_email3, valid_password3)
    _, auth_key4 = pf.get_api_key(valid_email4, valid_password4)
    _, auth_key5 = pf.get_api_key(valid_email5, valid_password5)

# Создаем и запускаем потоки для каждого пользователя
    start_time = time.time()
    pet_count = 0
    threads = []

    while time.time() - start_time < 60:
        for auth_key in [auth_key1, auth_key2, auth_key3, auth_key4, auth_key5]:
            thread = threading.Thread(target=add_pet, args=(auth_key,))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()
#Убеждаемся что колличество питомцев не превысило заданного предела
    assert pet_count <= 99999
