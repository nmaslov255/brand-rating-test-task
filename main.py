"""
Выдержка из Тестового задания:


```
Скрипт читает файлы с данными о рейтингах товаров и формирует отчеты.

Отчёт включает в себя список брендов и средний рейтинг бренда, бренды
сортируются по рейтингу.

Название файлов (может быть несколько) и название отчета передается
в виде параметров --files и --report.

Отчёт формируется по всем переданных файлам, а не по каждому отдельно.
```

FAQ:
    - Для объединения csv файлов в таблицу дергаем `helpers.merge_csv`.
    - Для добавления нового репорта создаем модуль в `reports/{report_name}.py`
    - Для каждого репорта нужно задать схему таблицы входных данных.
    - Стандарт кодирования pep8, в качестве линтера flake8.
"""
import argparse
from tabulate import tabulate

from helpers import merge_csv
from reports import select_report_by_name


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

    # Загружаем класс репорта и объединяем CSV в одну табличку
    Report = select_report_by_name(args.report)
    table: list[tuple] = merge_csv(args.files)

    # Генерируем отчёт и выводим
    report_table: list[tuple] = Report(table).calculate()
    print(tabulate(report_table, headers="firstrow"))


if __name__ == "__main__":
    main()
