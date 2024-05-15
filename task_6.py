from pydantic import BaseModel, Field, StrictStr, StrictInt
from datetime import datetime
from typing import Annotated
from pandas import DataFrame
from airflow.providers.http.hooks.http import HttpHook
from airflow.exceptions import AirflowException


ColumnsTuple = tuple[StrictStr, StrictStr, StrictStr]
Columns = Annotated[ColumnsTuple, Field(strict=False)]
RowTuple = tuple[StrictInt, datetime, StrictStr]
Rows = list[Annotated[RowTuple, Field(strict=False)]]


class ImportantDocsModel(BaseModel):
    Columns: Columns
    Description: StrictStr
    RowCount: StrictInt
    Rows: Rows


def get_important_docs_json(conn_id: str, endpoint: str) -> dict:
    """
    Requests docs by http request to outer API and returns response body.
    :param conn_id: connection id for HttpHook
    :param endpoint: important docs endpoint
    :return: dict, containing docs data
    """
    hook = HttpHook(method='GET', http_conn_id=conn_id)
    try:
        response = hook.run(endpoint=endpoint, headers={"Content-type": "application/json"})
        json_data = response.json()
    except AirflowException as ex:
        print(f'Failed to get response from docs API: {ex}')
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
    today = datetime.today()
    beginning_of_today = datetime(today.year, today.month, today.day)
    docs_date = beginning_of_today.timestamp()
    connection_id = 'https://api.gazprombank.ru'
    docs_endpoint = f'/very/important/docs?documents_date={docs_date}'
    json_docs = get_important_docs_json(connection_id, docs_endpoint)
    docs = ImportantDocsModel(**json_docs)  # validating implicitly here
    dataframe = handle_docs(docs)
    print(dataframe.to_csv())
