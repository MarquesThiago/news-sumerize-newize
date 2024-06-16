from csv import DictReader, DictWriter
from typing import Dict, List, Any


def read_column_csv(
    path: str, column_name: str, newline: str = "\n"
) -> Dict[str, List[str]]:

    values = []
    with open(path, newline=newline) as file:
        reader = DictReader(file)
        for row in reader:
            values.append(row[column_name])

    return {column_name: values}


def write_csv(
    path: str, columns: List[str], values: List[Dict[Any, Any]]
) -> None:

    with open(path, 'w', newline='') as file:
        writer = DictWriter(file, fieldnames=columns)
        writer.writeheader()
        for row in values:
            writer.writerow(row)
