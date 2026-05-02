import pytest
import allure
from pydantic import ValidationError
from models import UserSchema
from utils import (
    check_status,
    check_list_not_empty,
    check_field_exists,
    check_email_format,
    check_unique_ids,
)


@allure.feature("Юзеры")
@allure.story("Получение юзеров")
@pytest.mark.regression
@pytest.mark.users
class TestUsers:

    @allure.title("GET /users возвращает 200")
    def test_get_users(self, client):
        response = client.get("/users")
        check_status(response, 200)

    @allure.title("Юзеров ровно 10")
    def test_users_count(self, all_users):
        assert len(all_users) == 10, f"Ожидал 10 юзеров, получил {len(all_users)}"

    @allure.title("У всех юзеров уникальные id")
    def test_user_ids_are_unique(self, all_users):
        check_unique_ids(all_users)

    @allure.title("У юзера есть все нужные поля")
    @pytest.mark.parametrize("field", ["id", "name", "username", "email", "address", "phone", "website", "company"])
    def test_user_has_required_fields(self, user_1, field):
        check_field_exists(user_1, field)

    @allure.title("Юзер проходит валидацию схемы")
    def test_user_schema(self, user_1):
        try:
            UserSchema(**user_1)
        except ValidationError as error:
            pytest.fail(f"Схема юзера не прошла валидацию:\n{error}")

    @allure.title("У всех юзеров корректные email адреса")
    def test_all_user_emails(self, all_users):
        for user in all_users:
            check_email_format(user["email"])

    @allure.title("В адресе юзера есть координаты гео")
    def test_user_address_has_geo(self, all_users):
        for user in all_users:
            geo = user.get("address", {}).get("geo", {})
            assert "lat" in geo, f"Нет lat у юзера {user['id']}"
            assert "lng" in geo, f"Нет lng у юзера {user['id']}"

    @allure.title("В компании юзера есть нужные поля")
    def test_user_company_fields(self, all_users):
        for user in all_users:
            company = user.get("company", {})
            for field in ["name", "catchPhrase", "bs"]:
                assert field in company, (
                    f"В компании юзера {user['id']} нет поля '{field}'"
                )

    @allure.title("Фильтр юзеров по username работает")
    def test_filter_by_username(self, client):
        response = client.get("/users", params={"username": "Bret"})
        check_status(response, 200)
        users = response.json()
        check_list_not_empty(users, "Юзеры с username=Bret")
        for user in users:
            assert user["username"] == "Bret"

    @allure.title("GET /users/{id} для разных юзеров")
    @pytest.mark.parametrize("user_id", [1, 3, 5, 7, 10])
    def test_get_user_by_id(self, client, user_id):
        response = client.get(f"/users/{user_id}")
        check_status(response, 200)
        assert response.json()["id"] == user_id
