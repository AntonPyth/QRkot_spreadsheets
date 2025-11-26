from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Возвращается при чтении доступных данных юзера."""


class UserCreate(schemas.BaseUserCreate):
    """Используется при создании нового пользователя."""


class UserUpdate(schemas.BaseUserUpdate):
    """Используется для акцепта частичных обновлений."""
