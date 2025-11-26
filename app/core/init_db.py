import contextlib
from typing import Optional

from app.core.config import logger, settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate
from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


__all__ = ['create_user', 'create_first_superuser']


async def create_user(
    email: EmailStr, password: str, is_superuser: bool = False
) -> bool:
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                        )
                    )

        logger.info('Created user %s', email)
        return True

    except UserAlreadyExists:
        logger.info('User %s already exists', email)
        return False

    except Exception:
        logger.exception('Failed to create user %s', email)
        return False


async def create_first_superuser() -> None:
    email: Optional[str] = settings.first_superuser_email
    password: Optional[str] = settings.first_superuser_password

    if not (email and password):
        logger.debug('Суперпользователь не задан в переменных окружения')
        return

    created = await create_user(
        email=email,
        password=password,
        is_superuser=True
    )
    if created:
        logger.info('Initial superuser %s created', email)
    else:
        logger.info('Initial superuser %s already present', email)
