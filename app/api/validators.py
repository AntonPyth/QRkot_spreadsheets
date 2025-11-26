from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_project_name_duplicate(
        name: str,
        session: AsyncSession
) -> None:
    """Если проект с дублирующим именем, вызывает сообщение об ошибке."""
    project_id = await charity_project_crud.get_project_id_by_name(
        name,
        session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
    project_id: int, session: AsyncSession
) -> CharityProject:
    """Благотворительный проект уже создан."""
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Проект не найден!'
        )
    return project


async def check_project_closed_or_invested(
    project_id: int, session: AsyncSession
) -> None:
    """Проект закрыт или инвестиции уже накоплены."""
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Проект не найден!'
        )
    if project.invested_amount > 0 or project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект уже были внесены средства, нельзя удалить!',
        )


async def check_project_before_edit(
    full_amount: int, project_id: int, session: AsyncSession
) -> None:
    """Можно ли вносить изменения в проект."""
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Проект не найден!'
        )
    if project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
    if full_amount < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                'Нельзя установить значение full_amount '
                'меньше ранее вложенной суммы.'
            ),
        )
