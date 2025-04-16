import json
import allure
import pytest
import requests
from data import Orders
from handle import Handle
from urls import Urls


class TestCreateOrder:

    @pytest.mark.parametrize('order_data',
                             [{"color": ["BLACK"]},
                              {"color": ["GREY"]},
                              {"color": [""]},
                              {"color": ["BLACK", "GREY"]}])
    @allure.title('Создание заказа')
    def test_create_order(self, order_data):
        with allure.step('Обновление данных заказа'):
            Orders.data_order.update(order_data)

        with allure.step('Подготовка данных для запроса'):
            order_data_json = json.dumps(Orders.data_order)

        headers = {'Content-Type': 'application/json'}

        with allure.step('Отправка POST-запроса для создания заказа'):
            response = requests.post(f'{Urls.URL}{Handle.CREATE_ORDER}', data=order_data_json, headers=headers)

        with allure.step('Проверка ответа на создание заказа'):
            assert response.status_code == 201, f'Ожидался статус 201, получен {response.status_code}'
            assert 'track' in response.text, 'Отсутствует ожидаемый ключ "track" в ответе'
