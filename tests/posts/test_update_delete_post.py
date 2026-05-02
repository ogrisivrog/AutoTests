import pytest
import allure
from utils import check_status, check_field_value, make_post


@allure.feature("Посты")
@allure.story("Обновление постов")
@pytest.mark.regression
@pytest.mark.posts
class TestUpdatePost:

    @allure.title("PUT /posts/1 — полное обновление поста")
    def test_put_post(self, client):
        new_data = make_post()
        response = client.put("/posts/1", data=new_data)
        check_status(response, 200)

    @allure.title("PUT /posts/1 — в ответе новые данные")
    def test_put_returns_new_data(self, client):
        new_data = make_post()
        response = client.put("/posts/1", data=new_data)
        body = response.json()
        check_field_value(body, "title", new_data["title"])
        check_field_value(body, "body", new_data["body"])

    @allure.title("PATCH /posts/1 — частичное обновление только title")
    def test_patch_title(self, client):
        response = client.patch("/posts/1", data={"title": "обновлённый title"})
        check_status(response, 200)
        body = response.json()
        check_field_value(body, "title", "обновлённый title")

    @allure.title("PATCH /posts/{id} для нескольких постов")
    @pytest.mark.parametrize("post_id", [1, 10, 50])
    def test_patch_multiple_posts(self, client, post_id):
        response = client.patch(f"/posts/{post_id}", data={"title": f"пост {post_id} обновлён"})
        check_status(response, 200)


@allure.feature("Посты")
@allure.story("Удаление постов")
@pytest.mark.regression
@pytest.mark.posts
class TestDeletePost:

    @allure.title("DELETE /posts/1 — возвращает 200")
    def test_delete_post(self, client):
        response = client.delete("/posts/1")
        check_status(response, 200)

    @allure.title("После удаления тело ответа пустое")
    def test_delete_returns_empty_body(self, client):
        response = client.delete("/posts/1")
        check_status(response, 200)
        assert response.json() == {}, f"Ожидал пустой объект, получил: {response.json()}"

    @allure.title("DELETE /posts/{id} для нескольких постов")
    @pytest.mark.parametrize("post_id", [1, 50, 100])
    def test_delete_multiple_posts(self, client, post_id):
        response = client.delete(f"/posts/{post_id}")
        check_status(response, 200)
