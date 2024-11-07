import requests
from api import PetFriends
from settings import valid_email, valid_password
from settings import invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Бульдог', animal_type='Французский', age='3',
                                     pet_photo='images/бульдог.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Бульдог", "Французский", "3", "images/бульдог.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Панда', animal_type='Китайская', age=2):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_add_new_pet_without_photo(name='Рэй', animal_type='чих',
                                   age='4'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_photo_of_pet(pet_photo='images/симба.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if pet_photo is None:
        pf.add_photo_of_pet(auth_key, "Рэй", "чих", "4")
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        assert status == 200


def test_failed_get_api_key_in(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key_in(email, password)
    assert status != 200
    assert result
    print("\n" "Пользователь не существует")


def test_failed__get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key_in(invalid_email, invalid_password)
    status, result = pf.get_list_of_pets_in(auth_key, filter)


def test_get_api_key_for_invalid_user(email="rtesd@gmail.com", password="12345"):
    '''Проверяем что запрос api ключа с неверными данными пользователя возвращает статус 403 и в тезультате не содержится слово key'''

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result


def test_add_new_pet_with_incorrect_name(name='', animal_type='мышь', age='1'):
    '''Проверяем что можно добавить питомца без имени'''

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_update_pet_with_incorrect_data(name='', animal_type='', age=""):
    """Проверяем возможность изменения информации о питомце на пустые значения"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_new_pet_with_long_name(name='jkdl[a[q;qssuehnckxlpa;ww.mJA9WNXMM,l;a;am', animal_type='rjn', age='3'):
    '''Проверяем что можно добавить питомца с некорректным именем большой длины'''

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
