import logging
import sys
from typing import Optional

from pydantic import BaseSettings, EmailStr

MIN_PASS_LEN = 3

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    '%(asctime)s,'
    '%(levelname)s,'
    '%(message)s,'
    '%(name)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд'
    app_description: str = 'Поддержка котиков'
    database_url: str = 'sqlite+aiosqlite:///./cat_charity_fund.db'
    secret: str = 'CHANGE_ME'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'
        env_prefix = 'CAT_'


settings = Settings()
