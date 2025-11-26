from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.services.apis_google import (set_user_permissions,
                                     spreadsheets_create,
                                     spreadsheets_update_value)

router = APIRouter()


@router.post(
    '/',
    response_model=dict[str, str],
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
    await set_user_permissions(spreadsheet_id, wrapper_services)
    await spreadsheets_update_value(
        spreadsheet_id,
        projects,
        wrapper_services,
    )
    return projects


# from datetime import datetime, timedelta
# from typing import Any

# from aiogoogle import Aiogoogle

# from app.core.config import (DATE_FORMAT, PERMISSION_BODY,
#                              SPREADSHEET_BODY, TABLE_VALUES)
# from app.models.charity_project import CharityProject


# async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
#     now_date_time = datetime.now().strftime(DATE_FORMAT)
#     service = await wrapper_services.discover('sheets', 'v4')
#     spreadsheet_body: dict[str, Any] = SPREADSHEET_BODY
#     spreadsheet_body['properties']['title'] = f'Отчёт от {now_date_time}'
#     response = await wrapper_services.as_service_account(
#         service.spreadsheets.create(json=spreadsheet_body)
#     )
#     spreadsheet_id = response['spreadsheetId']
#     return spreadsheet_id


# async def set_user_permissions(
#         spreadsheet_id: str,
#         wrapper_services: Aiogoogle
# ) -> None:
#     service = await wrapper_services.discover('drive', 'v3')
#     await wrapper_services.as_service_account(
#         service.permissions.create(
#             fileId=spreadsheet_id,
#             json=PERMISSION_BODY,
#             fields="id"
#         ))


# async def spreadsheets_update_value(
#         spreadsheet_id: str,
#         charity_projects: list[CharityProject],
#         wrapper_services: Aiogoogle
# ) -> None:
#     now_date_time = datetime.now().strftime(DATE_FORMAT)
#     service = await wrapper_services.discover('sheets', 'v4')
#     table_values = list(TABLE_VALUES)
#     table_values[0][1] = now_date_time
#     for project in charity_projects:
#         new_row = [
#             str(project['name']),
#             str(timedelta(days=project['days_before_closed'])),
#             str(project['description'])
#         ]
#         table_values.append(new_row)
#     update_body = {
#         'majorDimension': 'ROWS',
#         'values': table_values
#     }
#     await wrapper_services.as_service_account(
#         service.spreadsheets.values.update(
#             spreadsheetId=spreadsheet_id,
#             range='A1:E30',
#             valueInputOption='USER_ENTERED',
#             json=update_body
#         )
#     )
