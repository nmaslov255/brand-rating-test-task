#!/usr/bin/env python3
import argparse
from tabulate import tabulate

from helpers import merge_csv
from reports import select_reporter_by_name


def main():
    parser = argparse.ArgumentParser(
        description="CLI для генерации таблички в терминале."
    )
    parser.add_argument(
        "--files", nargs="+", required=True, help="Список CSV-файлов"
    )
    parser.add_argument(
        "--report", required=True, help="Имя отчёта из reports (без .py)"
    )

    args = parser.parse_args()

    # Загружаем класс репорта и объединяем CSV
    Reporter = select_reporter_by_name(args.report)
    table: list[tuple] = merge_csv(args.files)

    # Генерируем отчёт и выводим
    report_table: list[tuple] = Reporter(table).build()
    print(tabulate(report_table, headers="firstrow"))


if __name__ == "__main__":
    main()
