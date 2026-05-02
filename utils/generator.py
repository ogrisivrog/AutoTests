import random
from faker import Faker

# использую faker чтобы не хардкодить данные
# так тесты каждый раз работают с разными значениями
faker = Faker("ru_RU")


def make_post():
    return {
        "title": faker.sentence(nb_words=5),
        "body": faker.text(max_nb_chars=200),
        "userId": random.randint(1, 10)
    }


def make_user():
    return {
        "name": faker.name(),
        "username": faker.user_name(),
        "email": faker.email(),
        "phone": faker.phone_number(),
        "website": faker.domain_name()
    }


def make_comment(post_id=None):
    return {
        "postId": post_id or random.randint(1, 100),
        "name": faker.sentence(nb_words=4),
        "email": faker.email(),
        "body": faker.text(max_nb_chars=150)
    }
