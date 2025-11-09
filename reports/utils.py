import os
import sys
import importlib.util


def select_reporter_by_name(report_name: str):
    """
    Загружает класс Report из модуля reports/{report_name}.py
    """
    report_path = os.path.join("reports", f"{report_name}.py")

    if not os.path.isfile(report_path):
        print(f"Ошибка: файл {report_path} не найден")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location(report_name, report_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.Report
