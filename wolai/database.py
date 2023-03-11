from wolai.constants import WOLAI_URL, API_VERSION_V1
from wolai.types.resp import DatabaseFormat
from wolai.types.database import CreateDatabaseRow, DatabaseRowData
from wolai.encoder import to_json


DATABASE_API_URL = f'{WOLAI_URL}/{API_VERSION_V1}/databases'


def get_database(ctx: callable, database_id: str) -> DatabaseFormat:
    url = f'{DATABASE_API_URL}/{database_id}'
    resp = ctx(url, method='get')['data']

    return DatabaseFormat(**resp)


def insert_database(ctx: callable, database_id: str,
                    rows: list[CreateDatabaseRow] | list[DatabaseRowData] | list[dict]) -> str:
    new_rows = []

    for item in rows:
        if isinstance(item, DatabaseRowData):
            new_rows.append(item.to_create_database_row())
        elif isinstance(item, CreateDatabaseRow):
            new_rows.append(item)
        elif isinstance(item, dict):
            new_rows.append(CreateDatabaseRow(item))

    url = f'{DATABASE_API_URL}/{database_id}/rows'
    data = {'rows': new_rows}
    resp = ctx(url, data=to_json(data))['data']

    return resp
