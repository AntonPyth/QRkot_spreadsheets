from sqlalchemy import Column, ForeignKey, Integer, Text

from .donation_base import DonationsBase


class Donation(DonationsBase):
    """Модель пожертвования, вклад пользователя в благотворительный проект."""

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
