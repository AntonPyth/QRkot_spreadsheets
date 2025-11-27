from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_project_before_edit,
                                check_project_closed_or_invested,
                                check_project_exists,
                                check_project_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.services import marks_project_completed, distributes_investments

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    summary='Запрашивает список всех благотворительных проектов',
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
) -> list[CharityProjectDB]:
    return await charity_project_crud.get_multi(session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Удалить благотворительный проект',
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    project = await check_project_exists(project_id, session)
    await check_project_closed_or_invested(project_id, session)
    return await charity_project_crud.remove(project, session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Создать новый благотворительный проект',
)
async def create_new_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    await check_project_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    return await distributes_investments(new_project, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Внести изменения в благотворительный проект',
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> CharityProjectDB:
    project = await check_project_exists(project_id, session)
    if obj_in.name is not None:
        await check_project_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_project_before_edit(
            obj_in.full_amount,
            project_id, session
        )
    project = await charity_project_crud.update(project, obj_in, session)
    return await marks_project_completed(project, session)
