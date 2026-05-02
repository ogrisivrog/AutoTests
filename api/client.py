import os
import requests
from dotenv import load_dotenv

load_dotenv()

# базовый url и таймаут берём из .env файла
BASE_URL = os.getenv("BASE_URL", "https://jsonplaceholder.typicode.com")
TIMEOUT = int(os.getenv("TIMEOUT", "10"))


class ApiClient:
    # этот класс нужен чтобы не писать BASE_URL в каждом тесте
    # плюс сессия быстрее чем каждый раз делать новый запрос

    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def get(self, url, params=None):
        full_url = self.base_url + url
        response = self.session.get(full_url, params=params, timeout=TIMEOUT)
        return response

    def post(self, url, data):
        full_url = self.base_url + url
        response = self.session.post(full_url, json=data, timeout=TIMEOUT)
        return response

    def put(self, url, data):
        full_url = self.base_url + url
        response = self.session.put(full_url, json=data, timeout=TIMEOUT)
        return response

    def patch(self, url, data):
        full_url = self.base_url + url
        response = self.session.patch(full_url, json=data, timeout=TIMEOUT)
        return response

    def delete(self, url):
        full_url = self.base_url + url
        response = self.session.delete(full_url, timeout=TIMEOUT)
        return response
