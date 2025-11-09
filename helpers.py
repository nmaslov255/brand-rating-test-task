# Функции-помошники для работы с файлами
import csv
from exceptions import ValidationError


def merge_csv(file_paths: list) -> list[tuple]:
    """
    Объединяет несколько CSV файлов в один список кортежей.

    :param file_paths: Список путей к CSV файлам
    :return: Список кортежей, где первый элемент — заголовок
    :raises ValueError: Если заголовки файлов отличаются
    """
    merged = []
    header = None

    for path in file_paths:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            current_header = tuple(next(reader))

            if header is None:
                header = current_header
                merged.append(header)
            elif header != current_header:
                raise ValidationError(f'В переданных файлах различаются заголовки: "{file_paths}"')

            merged.extend(tuple(row) for row in reader)

    return merged
