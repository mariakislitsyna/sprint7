import allure
import requests
import pytest
import handle
from urls import Urls
from data import Users


class TestLoginCourier:

    @allure.title('Авторизация под курьером выдает id')
    def test_courier_log_in(self):
        with allure.step('Отправка POST-запроса для авторизации курьера'):
            response = requests.post(
                f'{Urls.URL}{handle.Handle.LOGIN_COURIER}',
                data=Users.data_current
            )

        with allure.step('Проверка статуса ответа и наличия id'):
            assert response.status_code == 200, f'Ожидался статус 200, получен {response.status_code}'
            assert 'id' in response.text, 'Ключ "id" отсутствует в ответе'

    @allure.title('Ошибка при авторизации если логин или пароль не корректные')
    def test_courier_log_negative(self):
        with allure.step('Отправка POST-запроса для авторизации с некорректными данными'):
            response = requests.post(
                f'{Urls.URL}{handle.Handle.LOGIN_COURIER}',
                data=Users.data_negative
            )

        with allure.step('Проверка статуса ответа и сообщения об ошибке'):
            assert response.status_code == 404, f'Ожидался статус 404, получен {response.status_code}'
            assert 'Учетная запись не найдена' in response.text, 'Сообщение об ошибке отсутствует'

    @pytest.mark.parametrize('data_without_login_or_password', [Users.data_without_login, Users.data_without_password])
    @allure.title('Ошибка при авторизации если не заполнить логин или пароль')
    def test_courier_log_not_all_data(self, data_without_login_or_password):
        with allure.step('Отправка POST-запроса для авторизации с неполными данными'):
            response = requests.post(
                f'{Urls.URL}{handle.Handle.LOGIN_COURIER}',
                data=data_without_login_or_password
            )

        with allure.step('Проверка статуса ответа и сообщения об ошибке'):
            assert response.status_code == 400, f'Ожидался статус 400, получен {response.status_code}'
            assert 'Недостаточно данных для входа' in response.text, 'Сообщение об ошибке отсутствует'
