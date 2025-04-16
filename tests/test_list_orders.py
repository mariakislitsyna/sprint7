import allure
import requests
from handle import Handle
from urls import Urls


class TestReturnOrderList:
    @allure.title('В тело ответа возвращается список заказов')
    def test_list_order(self):
        with allure.step('Отправка GET-запроса для получения списка заказов'):
            response = requests.get(f'{Urls.URL}{Handle.CREATE_ORDER}')

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200, f'Ожидался статус 200, получен {response.status_code}'

        with allure.step('Проверка наличия ключа "orders" в ответе'):
            assert "orders" in response.json(), 'Ключ "orders" отсутствует в ответе'
