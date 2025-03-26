import allure
import jsonschema
import pytest
import requests
from .schemas.pet_schema import PET_SCHEMA
BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store") # горячая клаваши для импортирования Alt+Enter
class Test_Store:
    @allure.title('Размещение заказа')
    def test_new_order(self):
        with allure.step("Отправляем заказ"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            response.json = response.json()

        with allure.step("Проверка статуса ответа и данных заказа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json['id'] == payload['id']
            assert response.json['petId'] == payload['petId']
            assert response.json['quantity'] == payload['quantity']
            assert response.json['status'] == payload['status']
            assert response.json['complete'] == payload['complete']



    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self):
        with allure.step("Получаем информацию о заказе по id"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа и данных заказа"):
                assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
                assert response.json()['id'] == 1, "id  не совпало с ожидаемым"



    @allure.title("Удаление заказа по ID")
    def test_delete_order(self):
        with allure.step("Удаляем информацию о заказе по ID"):
            response = requests.delete(f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Отправка запроса на получение информации об удалённом заказе"):
            response = requests.get(f'{BASE_URL}/store/order/1')

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"



    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_delete_nonexistent_order(self):
        with allure.step("Попытка получить информацию о несуществующем заказе"):
            response = requests.get(f'{BASE_URL}/store/order/9999')

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
                assert response.text == ("Order not found"), "Текст ошибки не совпал с ожидаемым"



    @allure.title("Получение инвентаря магазина")
    def test_get_inventory_shop(self):
        with allure.step(""):
            response = requests.get(f'{BASE_URL}/store/inventory')

        with allure.step("Проверка статуса ответа и данных инвентаря"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json() == {"approved":57,"delivered":50}, "Формат не совпал с ожидаемым"






