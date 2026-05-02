import re
import allure


# вынес проверки в отдельный файл чтобы не дублировать код в тестах
# allure.step нужен чтобы в отчёте было видно что именно проверялось


def check_status(response, expected_status):
    with allure.step(f"Проверяю статус код: ожидаю {expected_status}"):
        actual = response.status_code
        assert actual == expected_status, (
            f"Ожидал статус {expected_status}, получил {actual}\n"
            f"URL: {response.url}\n"
            f"Тело ответа: {response.text[:300]}"
        )


def check_response_time(response, max_seconds=2.0):
    with allure.step(f"Проверяю время ответа: должно быть меньше {max_seconds}с"):
        elapsed = response.elapsed.total_seconds()
        assert elapsed < max_seconds, (
            f"Апи тормозит: ответил за {elapsed:.2f}с, лимит {max_seconds}с"
        )


def check_field_exists(body, field):
    with allure.step(f"Проверяю что поле '{field}' есть в ответе"):
        assert field in body, f"Поля '{field}' нет в ответе: {body}"


def check_list_not_empty(data, label="Список"):
    with allure.step(f"Проверяю что {label} не пустой"):
        assert isinstance(data, list), f"Ожидал список, получил {type(data)}"
        assert len(data) > 0, f"{label} пустой"


def check_field_value(body, field, expected):
    with allure.step(f"Проверяю что {field} == {expected!r}"):
        actual = body.get(field)
        assert actual == expected, (
            f"Поле '{field}': ожидал {expected!r}, получил {actual!r}"
        )


def check_email_format(email):
    with allure.step(f"Проверяю формат email: {email}"):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        assert re.match(pattern, email), f"Некорректный email: {email}"


def check_unique_ids(data, field="id"):
    with allure.step(f"Проверяю что все '{field}' уникальные"):
        all_ids = [item[field] for item in data]
        assert len(all_ids) == len(set(all_ids)), "Нашёл дублирующиеся id"
