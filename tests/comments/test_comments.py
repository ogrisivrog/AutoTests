import re
import pytest
import allure
from pydantic import ValidationError
from models import CommentSchema
from utils import (
    check_status,
    check_list_not_empty,
    check_unique_ids,
)


@allure.feature("Комменты")
@allure.story("Получение комментов")
@pytest.mark.regression
@pytest.mark.comments
class TestComments:

    @allure.title("GET /comments возвращает 200 и список")
    def test_get_all_comments(self, client):
        response = client.get("/comments")
        check_status(response, 200)
        check_list_not_empty(response.json(), "Список комментов")

    @allure.title("Комментов ровно 500")
    def test_comments_count(self, all_comments):
        assert len(all_comments) == 500, f"Ожидал 500, получил {len(all_comments)}"

    @allure.title("У всех комментов уникальные id")
    def test_comment_ids_are_unique(self, all_comments):
        check_unique_ids(all_comments)

    @allure.title("У всех комментов корректные email")
    def test_comment_emails(self, all_comments):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        invalid = []
        for comment in all_comments:
            if not re.match(pattern, comment.get("email", "")):
                invalid.append(f"Коммент {comment['id']}: {comment.get('email')}")
        assert not invalid, "Нашёл невалидные email:\n" + "\n".join(invalid)

    @allure.title("Фильтр комментов по postId работает")
    def test_filter_by_post(self, client):
        response = client.get("/comments", params={"postId": 1})
        check_status(response, 200)
        comments = response.json()
        check_list_not_empty(comments, "Комменты поста 1")
        for comment in comments:
            assert comment["postId"] == 1, (
                f"Коммент {comment['id']} принадлежит посту {comment['postId']}, а не 1"
            )

    @allure.title("Вложенный эндпоинт /posts/1/comments совпадает с фильтром")
    def test_nested_vs_filter(self, client):
        # это интересный тест — проверяю что два разных пути дают одинаковые данные
        # GET /posts/1/comments  vs  GET /comments?postId=1
        via_nested = client.get("/posts/1/comments").json()
        via_filter = client.get("/comments", params={"postId": 1}).json()

        nested_ids = sorted(c["id"] for c in via_nested)
        filter_ids = sorted(c["id"] for c in via_filter)

        assert nested_ids == filter_ids, (
            "Вложенный эндпоинт и фильтр вернули разные комменты!\n"
            f"Вложенный: {nested_ids}\n"
            f"Фильтр:    {filter_ids}"
        )

    @allure.title("Коммент проходит валидацию схемы")
    def test_comment_schema(self, client):
        response = client.get("/comments/1")
        check_status(response, 200)
        try:
            CommentSchema(**response.json())
        except ValidationError as error:
            pytest.fail(f"Схема не прошла:\n{error}")

    @allure.title("У поста {post_id} есть комменты")
    @pytest.mark.parametrize("post_id", [1, 10, 50, 99, 100])
    def test_comments_for_different_posts(self, client, post_id):
        response = client.get(f"/posts/{post_id}/comments")
        check_status(response, 200)
        check_list_not_empty(response.json(), f"Комменты поста {post_id}")
