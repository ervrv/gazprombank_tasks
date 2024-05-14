from csv import reader, writer
from typing import Iterable


def get_unique_rows(file: str) -> tuple[list[str], set[tuple]]:
    """
    Collects unique rows from file containing csv-like table.
    :param file: path to file, containing csv-like table
    :return: tuple of table columns as list and set of table rows as tuples
    """
    with open(file, encoding='utf-8', mode='r', newline='') as csv_file:
        csv_reader = reader(csv_file, delimiter='|')
        columns = []
        for row in csv_reader:
            columns = row
            break
        rows = set((tuple(row) for row in csv_reader if row))
    return columns, rows


def get_rows_with_common_ids(rows: set[tuple]) -> list[tuple]:
    """
    Collects rows with common ids and different content.
    :param rows: set of tuples with id as last element
    :return: list of tuples with common id
    """
    ids = set()
    common_ids = set()
    for row in rows:
        if row[-1] in ids:
            common_ids.add(row[-1])
        else:
            ids.add(row[-1])

    rows_with_common_ids = filter(lambda r: r[-1] in common_ids, rows)
    result_rows = list(rows_with_common_ids)
    # result_rows = sorted(rows_with_common_ids, key=lambda r: r[-1])
    return result_rows


def save_rows(file: str, columns: list[str], rows: Iterable[tuple]) -> None:
    """
    Saves csv-like table to file.
    :param file: path to file to save csv-like table to
    :param columns: table columns as list
    :param rows: set of table rows as tuples
    :return: None
    """
    with open(file, encoding='utf-8', mode='w', newline='') as csv_file:
        csv_writer = writer(csv_file, delimiter='|')
        csv_writer.writerow(columns)
        csv_writer.writerows(rows)


if __name__ == '__main__':
    column_names, unique_rows = get_unique_rows('f.csv')
    save_rows('unique_rows.csv', column_names, unique_rows)
    rows_with_equal_ids = get_rows_with_common_ids(unique_rows)
    save_rows('rows_with_equal_ids.csv', column_names, rows_with_equal_ids)
