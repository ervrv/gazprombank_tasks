from pydantic import BaseModel, Field, StrictStr, StrictInt
from datetime import datetime
from typing import Annotated
from pandas import DataFrame
from airflow.providers.http.hooks.http import HttpHook


ColumnsTuple = tuple[StrictStr, StrictStr, StrictStr]
Columns = Annotated[ColumnsTuple, Field(strict=False)]
RowTuple = tuple[StrictInt, datetime, StrictStr]
Rows = list[Annotated[RowTuple, Field(strict=False)]]


class ImportantDocsModel(BaseModel):
    Columns: Columns
    Description: StrictStr
    RowCount: StrictInt
    Rows: Rows


def get_important_docs_json(url: str) -> dict:
    """
    Requests docs by http request to outer API and returns response body.
    :param url: url to request docs
    :return: dict, containing docs data
    """
    hook = HttpHook(method='GET')
    try:
        response = hook.run(endpoint=url)
        json_data = response.json()
    except Exception as ex:
        print(f'Failed to get json from bank API: {ex}')
        json_data = {}
    return json_data


def handle_docs(docs_model: ImportantDocsModel) -> DataFrame:
    """
    Creates pandas dataframe for docs from pydantic model,
    renames columns in dataframe
    and adds column 'load_dt' with current datetime.
    :param docs_model: pydantic model of docs
    :return: docs data in dataframe
    """
    df = DataFrame(columns=docs_model.Columns, data=docs_model.Rows)
    columns = {
        'key1': 'document_id',
        'key2': 'document_dt',
        'key3': 'document_name'
    }
    df.rename(columns=columns, inplace=True)
    df.insert(3, 'load_dt', datetime.now())
    return df


if __name__ == '__main__':
    host = 'api.gazprombank.ru/'
    today = datetime.today()
    beginning_of_today = datetime(today.year, today.month, today.day)
    docs_date = beginning_of_today.timestamp()
    api_url = f'{host}very/important/docs?documents_date={docs_date}'
    json_docs = get_important_docs_json(api_url)
    docs = ImportantDocsModel(**json_docs)  # validating here
    dataframe = handle_docs(docs)
    print(dataframe.to_csv())
