from pathlib import Path
# from src.common.store.extra_files import write_csv
from machine_learning.src.common.store.extra_files import (
    write_csv, read_column_csv
)


def test_write_csv():

    path = "test.csv"
    columns_name = ["Name", "Nick"]
    data = [
        ["João Marcio", "JoJo"],
        ["Francisco Marinho", "Marinho"],
        ["Kuiz Augusto", "Gus"]
    ]

    values = map(
        lambda row: {columns_name[0]: row[0], columns_name[1]: row[1]},
        data
    )

    write_csv(path, columns_name, values)

    assert Path(path).exists()


def test_reader_csv():

    values = read_column_csv("test.csv", "Nick")
    assert values["Nick"][0] == "JoJo"
