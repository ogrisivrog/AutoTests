import pytest
from api import ApiClient


# scope="session" значит что клиент создаётся один раз на весь прогон
# без этого каждый тест создавал бы новый клиент — медленнее

@pytest.fixture(scope="session")
def client():
    api = ApiClient()
    yield api
    api.session.close()


# эти фикстуры делают один запрос и отдают данные всем тестам
# смысл тот же — не дёргать апи лишний раз

@pytest.fixture(scope="session")
def all_posts(client):
    response = client.get("/posts")
    return response.json()


@pytest.fixture(scope="session")
def all_users(client):
    response = client.get("/users")
    return response.json()


@pytest.fixture(scope="session")
def all_comments(client):
    response = client.get("/comments")
    return response.json()


@pytest.fixture(scope="session")
def post_1(client):
    response = client.get("/posts/1")
    return response.json()


@pytest.fixture(scope="session")
def user_1(client):
    response = client.get("/users/1")
    return response.json()
