from os import path
from pathlib import Path


def _charts_path() -> Path:
    test_helpers_path = Path(__file__).parent
    return test_helpers_path.joinpath("../../charts")


def charts_path() -> Path:
    return path.normpath(str(_charts_path().absolute()))


def chart_path(chart_name: str) -> str:
    chart_path = _charts_path().joinpath(chart_name)
    if not path.exists(chart_path):
        raise ValueError(f"Could not find chart: '{chart_path}' ({chart_path})")

    return path.normpath(str(chart_path.absolute()))
