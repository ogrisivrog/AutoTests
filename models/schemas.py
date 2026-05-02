from pydantic import BaseModel, EmailStr


# схемы для валидации ответов от api
# pydantic сам проверяет типы и кидает ошибку если что-то не так


class PostSchema(BaseModel):
    id: int
    title: str
    body: str
    userId: int


class GeoSchema(BaseModel):
    lat: str
    lng: str


class AddressSchema(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoSchema


class CompanySchema(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class UserSchema(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    address: AddressSchema
    phone: str
    website: str
    company: CompanySchema


class CommentSchema(BaseModel):
    postId: int
    id: int
    name: str
    email: EmailStr
    body: str
