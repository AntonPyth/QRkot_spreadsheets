from datetime import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer
from sqlalchemy.orm import declared_attr

from app.core.db import Base


class DonationsBase(Base):
    """Базовая модель пожертвований."""

    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = (
        CheckConstraint(
            'full_amount > 0',
            name='итоговая сумма положительная ?'
        ),
        CheckConstraint(
            'invested_amount >= 0',
            name='вложенная сумма положительная ?'
        ),
    )
