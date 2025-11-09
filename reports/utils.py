import os
import importlib.util


def select_report_by_name(report_name: str):
    """Загружает класс Report из модуля reports/{report_name}.py"""
    report_name = report_name.replace('-', '_')

    path = os.path.join("reports", f"{report_name}.py")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Модуль '{path}' не найден")

    spec = importlib.util.spec_from_file_location(report_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    try:
        return module.Report
    except AttributeError:
        raise ImportError(f"В модуле '{path}' отсутствует класс Report")
