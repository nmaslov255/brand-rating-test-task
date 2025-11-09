# Модуль с базовым классом репортов.
from typing import List, Tuple, Type

from exceptions import ValidationError


class BaseReport:
    """
    Базовый класс для репортов.
    Приводит ячейки таблицы к типам, заданным в __report_schema__.
    """
    __name__: str = "base_report"
    __report_schema__: List[Tuple[str, Type]] = None

    def __init__(self, table: List[tuple]):
        if not self.__report_schema__:
            raise ValidationError(
                f"Необходимо задать схему данных для репорта в {self.__name__}"
            )
        self.table = self._apply_schema(table)

    def _apply_schema(self, table: List[tuple]) -> List[tuple]:
        """Приводит таблицу к типам, заданным в __report_schema__."""
        header_schema = tuple(name for name, _ in self.__report_schema__)
        type_schema = tuple(_type for _, _type in self.__report_schema__)

        head, *body = table
        if head != header_schema:
            raise ValidationError(
                "Заголовки репорта не совпадают. "
                f"Получено: {head}, ожидается: {header_schema}"
            )

        normalized_body = [
            tuple(_type(value) for value, _type in zip(record, type_schema))
            for record in body
        ]

        return [head, *normalized_body]
