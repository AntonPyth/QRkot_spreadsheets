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
    # Google service account credentials (used by Google API client)
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    # email is used in tests to verify existence of a credentials attribute
    email: Optional[str] = None

    class Config:
        env_file = '.env'
        env_prefix = 'CAT_'


settings = Settings()

# Constants for Google Sheets/Drive integration
DATE_FORMAT = '%d.%m.%Y %H:%M:%S'
PERMISSION_BODY = {'role': 'writer', 'type': 'anyone'}
SPREADSHEET_BODY = {
    'properties': {
        'title': 'Отчёт'
    },
    'sheets': []
}
TABLE_VALUES: list[list[str]] = [
    ['Title', 'Date', 'Info']
]
