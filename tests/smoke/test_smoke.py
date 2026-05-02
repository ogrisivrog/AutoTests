import pytest
import allure
from utils import check_status, check_response_time


# smoke тесты — самые базовые проверки
# запускаю их первыми чтобы убедиться что апи вообще работает
# если тут всё упало — остальные тесты смысла запускать нет


@allure.feature("Smoke")
@pytest.mark.smoke
class TestSmoke:

    @allure.title("Апи отвечает на GET /posts")
    def test_api_is_alive(self, client):
        response = client.get("/posts")
        check_status(response, 200)

    @allure.title("Время ответа меньше 2 секунд")
    def test_api_is_fast(self, client):
        response = client.get("/posts")
        check_response_time(response, max_seconds=2.0)

    @allure.title("В ответе приходит JSON а не что-то другое")
    def test_content_type_is_json(self, client):
        response = client.get("/posts")
        content_type = response.headers.get("Content-Type", "")
        assert "application/json" in content_type, f"Ожидал json, получил: {content_type}"

    # проверяю что все основные эндпоинты живые
    @allure.title("Эндпоинт {endpoint} отвечает 200")
    @pytest.mark.parametrize("endpoint", ["/posts", "/users", "/comments", "/todos", "/albums"])
    def test_all_endpoints_alive(self, client, endpoint):
        response = client.get(endpoint)
        check_status(response, 200)
