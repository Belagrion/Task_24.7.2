import os.path

from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_post_new_pet_with_valid_key(name='Barsik', animal_type='Kot', age='5', pet_photo='images/pet1.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_information_about_new_pet(auth_key, name, animal_type, age, pet_photo)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_pet_from_database():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.post_information_about_new_pet(auth_key, "Vasya", "Dog", "3", "images/pet1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet_from_database(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

def test_change_information_about_my_pet_with_valid_key(name='Bobik', animal_type='Pes', age='8'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.change_information_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('There is no my pets')


"""10 тестов по заданию"""


def test_create_pet_simple_valid_key(name='Barsik', animal_type='Kot', age='6'):
    """Проверяем создания питомца в упрощенной форме, без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_photo_of_my_pet_valid_key(pet_photo='images/pet1.jpg'):
    '''Проверяем добавление фото к уже созданному питомцу'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_for_my_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert result['pet_photo'] != ""
    else:
        raise Exception('There is no my pets')

def test_create_pet_with_text_age_valid_key(name='Vitya', animal_type='Popyg', age='six'):
    '''Проверяем возможность указания вораста питомца буквами. В API указано требование ввода цифр'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_create_pet_with_special_symbol_in_name_valid_key(name='Vitya!@#$%^&*(', animal_type='Popyg', age='4'):
    '''Проверяем возможность отправки специальных символов в поле Имя'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_create_pet_with_special_symbol_in_age_valid_key(name='Tolya', animal_type='Svin', age='!@#$%^&*('):
    '''Проверяем возможность отправки специальных символов в поле Возраст'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_change_information_about_not_my_pet_valid_key(name='Bobik', animal_type='Pes', age='8'):
    '''Проверяем возможность изменить информацию о питомце, созданном другим пользователем'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "")

    status, result = pf.change_information_about_pet(auth_key, pets['pets'][6]['id'], name, animal_type, age)

    assert status == 200
    assert result['name'] == name

def test_delete_not_my_pet_valid_key():
    '''Проверяем возможность удалить питомца, созданном другим пользователем'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, pets = pf.get_list_of_pets(auth_key, "")

    pet_id = pets['pets'][0]['id']
    status, _ = pf.delete_pet_from_database(auth_key, pet_id)

    assert status == 200
    assert pet_id not in pets.values()

def test_create_pet_simple_300_symbols_valid_key(name='gsiuoyuwrerdfgrthrtyhgfjfuyjdfghdrfhdfghdfiuoyuwrerghgsdfgrthrt'
                                                      'yhgfjfuyjdfghdriuoyiuoyuwreruwrerfhdfghdfghyjdfghdrfhdfghdfghg'
                                                      'sdfgrthrtyhgfjfuyjdfghdrvxcvbniuoyuwrergsiuoyuwrerdfgrthrtyhg'
                                                      'fjfuyjdfghdrfhdfghdfiuoyuwrerghgsdfgrthrtyhgfjfuyjdfghdriuoyi'
                                                      'uoyuwreruwrerfhdfghdfghyjdfghdrfhdfghdfghgsdfgrthrtyh',
                                                 animal_type='Kot', age='6'):
    '''Проверяем возможности ввода имени питомца длинной 300 символов в поле Имя'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_create_pet_simple_without_name_valid_key(name='', animal_type='Zver', age='5'):
    '''Проверяем возможнсть создать питомца без указания имени'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_txt_file_instead_of_image_valid_key(pet_photo='images/pet2.txt'):
    '''Проверяем возможнсть добавления фото в форма файла txt вместо фото питомца в формате jpeg'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_for_my_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert result['pet_photo'] != ""
    else:
        raise Exception('There is no my pets')