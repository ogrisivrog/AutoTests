import pytest
import allure
from utils import check_status, check_field_exists, check_field_value, make_post


# невалидные данные для негативных тестов
# jsonplaceholder принимает всё и возвращает 201 даже без title
# в реальном апи тут было бы 422, но для учёбы ок — хотя бы проверяем что json приходит
INVALID_PAYLOADS = [
    pytest.param({"body": "нет title", "userId": 1}, id="no_title"),
    pytest.param({"title": "нет body", "userId": 1}, id="no_body"),
    pytest.param({"title": "", "body": "пустой titile", "userId": 1}, id="empty_title"),
    pytest.param({}, id="empty_object"),
]


@allure.feature("Посты")
@allure.story("Создание постов")
@pytest.mark.regression
@pytest.mark.posts
class TestCreatePost:

    @allure.title("Создать пост с валидными данными")
    def test_create_post(self, client):
        payload = make_post()
        response = client.post("/posts", data=payload)
        check_status(response, 201)

    @allure.title("В ответе есть id нового поста")
    def test_response_has_id(self, client):
        payload = make_post()
        response = client.post("/posts", data=payload)
        body = response.json()
        check_field_exists(body, "id")
        assert isinstance(body["id"], int), "id должен быть числом"

    @allure.title("Ответ содержит те же данные что отправляли")
    def test_response_reflects_payload(self, client):
        payload = make_post()
        response = client.post("/posts", data=payload)
        check_status(response, 201)
        body = response.json()
        check_field_value(body, "title", payload["title"])
        check_field_value(body, "body", payload["body"])
        check_field_value(body, "userId", payload["userId"])

    @allure.title("Создать 3 поста подряд — faker каждый раз другой")
    @pytest.mark.parametrize("run_number", [1, 2, 3])
    def test_create_multiple_posts(self, client, run_number):
        payload = make_post()
        response = client.post("/posts", data=payload)
        check_status(response, 201)

    @allure.title("Отправить невалидные данные — ответ всё равно json")
    @pytest.mark.negative
    @pytest.mark.parametrize("payload", INVALID_PAYLOADS)
    def test_invalid_payload(self, client, payload):
        # jsonplaceholder не валидирует данные — это особенность фейкового апи
        # в реальном проекте здесь ожидал бы 422 или 400
        response = client.post("/posts", data=payload)
        assert response.json() is not None, "Ответ должен быть валидным json"
