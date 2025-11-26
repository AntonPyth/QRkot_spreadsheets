from typing import Any, Dict, List, Optional, Type

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model: Type[Any]) -> None:
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession) -> Optional[Any]:
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalars().first()

    async def get_multi(self, session: AsyncSession) -> List[Any]:
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def create(
        self,
        obj_in: Any,
        session: AsyncSession,
        user: Optional[User] = None,
    ) -> Any:
        if hasattr(obj_in, 'dict'):
            payload: Dict[str, Any] = obj_in.dict()
        else:
            payload = dict(obj_in)
        if user is not None:
            payload['user_id'] = user.id
        instance = self.model(**payload)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def update(
        self,
        db_obj: Any,
        obj_in: Any,
        session: AsyncSession,
    ) -> Any:
        current_data = jsonable_encoder(db_obj)
        if hasattr(obj_in, 'dict'):
            update_data = obj_in.dict(exclude_unset=True)
        else:
            update_data = dict(obj_in)
        for field, value in update_data.items():
            if field in current_data:
                setattr(db_obj, field, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj: Any, session: AsyncSession) -> Any:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_by_attribute(
        self, attr_name: str, attr_value: Any, session: AsyncSession
    ) -> Optional[Any]:
        attr = getattr(self.model, attr_name)
        result = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return result.scalars().first()
