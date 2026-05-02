import pytest
import allure
from pydantic import ValidationError
from models import PostSchema
from utils import (
    check_status,
    check_response_time,
    check_field_exists,
    check_list_not_empty,
    check_unique_ids,
)


@allure.feature("Посты")
@allure.story("Получение постов")
@pytest.mark.regression
@pytest.mark.posts
class TestGetPosts:

    @allure.title("GET /posts возвращает список постов")
    def test_get_all_posts(self, client):
        response = client.get("/posts")
        check_status(response, 200)
        data = response.json()
        check_list_not_empty(data, "Список постов")

    @allure.title("Постов ровно 100 штук")
    def test_posts_count(self, all_posts):
        assert len(all_posts) == 100, f"Ожидал 100 постов, получил {len(all_posts)}"

    @allure.title("У всех постов уникальные id")
    def test_post_ids_are_unique(self, all_posts):
        check_unique_ids(all_posts)

    @allure.title("В посте есть все нужные поля")
    def test_post_has_required_fields(self, post_1):
        for field in ["id", "title", "body", "userId"]:
            check_field_exists(post_1, field)

    @allure.title("Пост проходит валидацию схемы")
    def test_post_schema(self, post_1):
        # использую pydantic чтобы проверить не только наличие полей
        # но и их типы — например что id это int а не строка
        try:
            PostSchema(**post_1)
        except ValidationError as error:
            pytest.fail(f"Схема не прошла валидацию:\n{error}")

    @allure.title("Все 100 постов проходят валидацию схемы")
    def test_all_posts_schema(self, all_posts):
        errors = []
        for post in all_posts:
            try:
                PostSchema(**post)
            except ValidationError as e:
                errors.append(f"Пост {post.get('id')}: {e}")
        assert not errors, "Нашёл посты с невалидной схемой:\n" + "\n".join(errors)

    @allure.title("Фильтр по userId работает")
    def test_filter_by_user(self, client):
        response = client.get("/posts", params={"userId": 1})
        check_status(response, 200)
        posts = response.json()
        check_list_not_empty(posts, "Посты юзера 1")
        # проверяю что все посты действительно принадлежат юзеру 1
        for post in posts:
            assert post["userId"] == 1, (
                f"Пост {post['id']} принадлежит юзеру {post['userId']}, а не 1"
            )

    @allure.title("Несуществующий пост возвращает 404")
    @pytest.mark.negative
    def test_nonexistent_post_returns_404(self, client):
        response = client.get("/posts/99999")
        check_status(response, 404)

    @allure.title("GET /posts отвечает быстро")
    def test_response_time(self, client):
        response = client.get("/posts")
        check_response_time(response)

    @allure.title("GET /posts/{id} для разных постов")
    @pytest.mark.parametrize("post_id", [1, 25, 50, 75, 100])
    def test_get_post_by_id(self, client, post_id):
        response = client.get(f"/posts/{post_id}")
        check_status(response, 200)
        body = response.json()
        assert body["id"] == post_id, f"Запросил пост {post_id}, вернулся {body['id']}"
