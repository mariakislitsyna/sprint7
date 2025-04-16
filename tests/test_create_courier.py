import allure
import requests
import pytest


from handle import Handle
from urls import Urls
from generator import register_new_courier as gen
from generator import register_new_courier_without_login as gen_without_login
from generator import register_new_courier_without_login as gen_without_password


class TestCreateCourier:
    data = gen()

    @pytest.fixture
    def create_courier(self):
        courier_data = TestCreateCourier.data
        response = requests.post(f'{Urls.URL}{Handle.CREATE_COURIER}', json=courier_data)
        assert response.status_code == 201, 'Курьер не был создан'
        return courier_data

    @allure.title('Создание курьера')
    def test_create_courier(self):
        response_body = '{"ok":true}'

        with allure.step('Отправка POST-запроса для создания курьера'):
            response = requests.post(
                f'{Urls.URL}{Handle.CREATE_COURIER}',
                TestCreateCourier.data
            )

        with allure.step('Проверка ответа на создание курьера'):
            assert response.status_code == 201, 'Ожидался статус 201'
            assert response.text == response_body, f'Ожидался ответ: {response_body}, получен: {response.text}'

    @allure.title('Нельзя создать двух одинаковых курьеров с одинаковыми логинами')
    def test_courier_was_created(self):
        with allure.step('Отправка POST-запроса для создания курьера'):
            response = requests.post(
                f'{Urls.URL}{Handle.CREATE_COURIER}',
                TestCreateCourier.data
            )

        with allure.step('Проверка ответа на повторное создание курьера'):
            assert response.status_code == 409, 'Ожидался статус 409'
            assert 'Этот логин уже используется' in response.text, 'Сообщение об ошибке неверное'

    @allure.title('Нельзя создать курьера без логина')
    def test_create_courier_without_login(self):
        with allure.step('Отправка POST-запроса для создания курьера без логина'):
            response = requests.post(
                f'{Urls.URL}{Handle.CREATE_COURIER}',
                gen_without_login()
            )

        with allure.step('Проверка ответа на отсутствие логина'):
            assert response.status_code == 400, 'Ожидался статус 400'
            assert 'Недостаточно данных для создания учетной записи' in response.text, 'Сообщение об ошибке неверное'

    @allure.title('Нельзя создать курьера без пароля')
    def test_create_courier_without_password(self):
        with allure.step('Отправка POST-запроса для создания курьера без пароля'):
            response = requests.post(
                f'{Urls.URL}{Handle.CREATE_COURIER}',
                gen_without_password()
            )

        with allure.step('Проверка ответа на отсутствие пароля'):
            assert response.status_code == 400, 'Ожидался статус 400'
            assert 'Недостаточно данных для создания учетной записи' in response.text, 'Сообщение об ошибке неверное'
