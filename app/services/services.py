from datetime import datetime
from typing import Union

from app.models import CharityProject, Donation
from app.models.donation_base import DonationsBase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def closing_project(project: CharityProject, session: AsyncSession):
    """Отмечает проект полностью заполненным."""
    if project.full_amount == project.invested_amount:
        project.fully_invested = True
        project.close_date = datetime.now()
        await session.commit()
        await session.refresh(project)
    return project


async def closing_single_investment(
    investment: DonationsBase,
    session: AsyncSession
):
    """Помечает взнос как полностью инвестированный."""
    investment.invested_amount = investment.full_amount
    investment.fully_invested = True
    investment.close_date = datetime.now()


async def investment_process(
    model_object: Union[CharityProject, Donation],
    session: AsyncSession
):
    """Распределяет инвестиции между проектами."""
    try:
        free_objects_model = model_object.investment_counterpart
    except AttributeError:
        raise ValueError(
            'Не содержит противоположную модель и не поддерживает инвестиции.'
        )

    result = await session.execute(
        select(free_objects_model)
        .where(~free_objects_model.fully_invested)
        .order_by(free_objects_model.create_date)
    )

    free_objects = result.scalars().all()

    if not free_objects:
        return model_object

    model_remaining = model_object.full_amount - model_object.invested_amount

    for free_object in free_objects:
        free_remaining = free_object.full_amount - free_object.invested_amount

        if free_remaining < model_remaining:
            model_object.invested_amount += free_remaining
            await closing_single_investment(free_object, session)
            model_remaining -= free_remaining
            continue

        if free_remaining == model_remaining:
            await closing_single_investment(model_object, session)
            await closing_single_investment(free_object, session)
            break

        free_object.invested_amount += model_remaining
        await closing_single_investment(model_object, session)
        break

    await session.commit()
    await session.refresh(model_object)
    
    # Закрыть проект если он полностью инвестирован
    if isinstance(model_object, CharityProject):
        await closing_project(model_object, session)
    
    return model_object
