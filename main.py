#!/usr/bin/env python3
import argparse
import importlib.util
import os
import sys
import csv


def load_report_processor(report_name: str):
    report_path = os.path.join("reports", f"{report_name}.py")

    if not os.path.isfile(report_path):
        print(f"Ошибка: {report_path} не найден")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location(report_name, report_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "run_processor"):
        print(f"Ошибка: файл отчёта должен содержать функцию run_processor(files)")
        sys.exit(1)

    return module.run_processor


def merge_csv(file_paths: list) -> list[tuple]:
    """
    Объединяет список из нескольких csv файлов

    :param file_paths: list[str] — пути к CSV файлам
    :return: list[tuple] — Объединенный список из csv файлов
    """

    head = None
    normalized = []

    for file_path in file_paths:
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            
            if not head:  # Создаем заголовок csv файла
                head = next(reader)
                normalized.append(tuple(head))
            elif head != next(reader):  # Возбуждаем исключение, если csv заголовок нового файла отличается по структуре
                raise Exception(f'Структура заголовка {file_path} отличается от других переданных файлов!')

            for record in reader:
                normalized.append(tuple(record))
    return normalized

def main():
    parser = argparse.ArgumentParser(
        description="CLI для генерации таблички в терминале."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Список путей к CSV-файлам"
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Название отчёта (имя модуля в директории reports, без расширения .py)"
    )

    args = parser.parse_args()

    records = merge_csv(args.files)
    report_processor = load_report_processor(args.report)
    # print(records)
    print(report_processor(records))


if __name__ == "__main__":
    main()
