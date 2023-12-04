import requests
import json

class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формете
        JSON с никальным уключем пользователя, найденного по указанным email и паролем"""

        headers = {
            'email': email,
            'password': password,
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str='') -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формет JSON
        со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_information_about_new_pet(self, auth_key: json, name: str, animal_type: str,
                                       age: str, pet_photo: str) -> json:
        """Метод отправляет запрос к API сервера и возвращает статус запроса и результат в формет JSON
        со информацией о созданном питомце и добавляет информацию о созданном питомце в базу данных"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        res = requests.post(self.base_url+'api/pets', headers=headers, data=data, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet_from_database(self, auth_key: json, pet_id: str) -> json:
        """Метод удаляет с серврера информацию о питомце по заданному pet_id и возвращает статус запроса"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url+'api/pets/'+pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def change_information_about_pet(self, auth_key: json, pet_id: str, name: str,
                                     animal_type: str, age: str) -> json:
        """Метод отправляет запрос к API сервера и возвращает статус запроса и результат в формате JSON
        с информацией о созданном питомце и добавляет информацию о созданном питомце в базу данных"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }

        res = requests.put(self.base_url+'api/pets/'+pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет запрос к API сервера и возвращает статус запроса и результат в формет JSON
        с информацией о созданном питомце и добавляет информацию о созданном питомце в базу данных БЕЗ фото питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_photo_for_my_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет запрос к API сервера и возвращает статус запроса и результат в формет JSON
        с информацией о питомце для которого была добаленна фотография"""

        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')}

        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result