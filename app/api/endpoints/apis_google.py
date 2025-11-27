import asyncio
from typing import Any, Dict, List

from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.apis_google import (set_user_permissions,
                                      spreadsheets_create,
                                      spreadsheets_update_value)

router = APIRouter()


@router.post(
    '/',
    response_model=List[Dict[str, Any]],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session
    )
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await asyncio.gather(
        set_user_permissions(spreadsheet_id, wrapper_services),
        spreadsheets_update_value(spreadsheet_id, projects, wrapper_services),
    )
    return projects
