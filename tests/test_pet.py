import allure
import jsonschema
import pytest
import requests
from .schemas.pet_schema import PET_SCHEMA
BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet") # горячая клаваши для импортирования Alt+Enter
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == ("Pet deleted"), "Текст ошибки не совпал с ожидаемым!"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_onexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f"{BASE_URL}/pet", json = payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == ("Pet not found"), "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце!")
    def test_get_onexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == ("Pet not found"), "Текст ошибки не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "Buddy",
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response.json = response.json()

        with allure.step("Проверка статуса ответа и валидации  JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response.json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response.json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response.json['name'] == payload['name'],"имя питомца не совпадает с ожидаемым"
            assert response.json['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца c полными данными")
    def test_add_pet_full(self):
        with allure.step("Подготовка данных для создания питомца с полными данными"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {"id": 11, "name": "Dogs"},
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response.json = response.json()

        with allure.step("Проверка статуса ответа и валидации  JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response.json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response.json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response.json['name'] == payload['name'],"имя питомца не совпадает с ожидаемым"
            assert response.json['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"
            assert response.json['category'] == payload['category'], "категория питомца не совпадает с ожидаемой"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()['id'] == pet_id
            assert response.json()['name'] == create_pet["name"]

    @allure.title("Обновление информации о питомце")
    def test_update_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на обновление созданного питомца"):
            payload = {
            "id": pet_id,
            "name": "Buddy Updated",
            "status": "sold"
        }
        response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса питомца и данных ответа"):
            assert response.status_code == 200
            assert response.json()['id'] == payload['id'], "ID не совпал с ожидаемым"
            assert response.json()['name'] == payload['name'], "Имя не совпало с ожидаемым"
            assert response.json()['status'] == payload['status'], "Статус не совпал с ожидаемым"

    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Удаление созданного питомца по ID"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации об удалённом питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("available", 200),
            ("pending", 200),
            ("sold", 200),
            ('',400),
            ('fox', 400)
            ]
    )
    def test_get_pet_by_status(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомца по статусу {status}"):
            response = requests.get(url=f"{BASE_URL}/pet/findByStatus", params={"status":status})

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expected_status_code
            assert isinstance(response.json(), list) or isinstance(response.text, str)


