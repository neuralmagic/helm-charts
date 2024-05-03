import json
from os import path
from pathlib import Path
from typing import Dict

import yaml


def charts_path() -> str:
    test_helpers_path = Path(__file__).parent.parent
    _charts_path = test_helpers_path.joinpath("../charts")
    return path.normpath(str(_charts_path.absolute()))


def chart_path(chart_name: str) -> str:
    return f"{charts_path()}/{chart_name}"


def get_chart_yaml(chart_name: str) -> Dict:
    chart_yaml_path = f"{chart_path(chart_name)}/Chart.yaml"
    with open(chart_yaml_path, encoding="utf-8", mode="r") as file:
        chart_yaml = yaml.safe_load(file)
    assert isinstance(chart_yaml, Dict)
    return chart_yaml


def get_chart_values(chart_name: str) -> Dict:
    chart_values_path = f"{chart_path(chart_name)}/values.yaml"
    with open(chart_values_path, encoding="utf-8", mode="r") as file:
        chart_values = yaml.safe_load(file)
    assert isinstance(chart_values, Dict)
    return chart_values


def get_chart_values_schema(chart_name: str) -> Dict:
    chart_values_schema_path = f"{chart_path(chart_name)}/values.schema.json"
    with open(chart_values_schema_path, encoding="utf-8", mode="r") as file:
        chart_values_schema = json.loads(file.read())
    assert isinstance(chart_values_schema, Dict)
    return chart_values_schema
