import json
from os import path
from pathlib import Path
from typing import Dict

import pytest
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


def make_chart_fixtures(
    chart_dir_name: str,
    conftest_globals: Dict,
) -> None:
    @pytest.fixture(scope="package")
    def app_version(chart_yaml: Dict) -> str:
        _app_version = chart_yaml["appVersion"]
        assert isinstance(_app_version, str)
        return _app_version

    conftest_globals["app_version"] = app_version

    @pytest.fixture(scope="package")
    def chart_name(chart_yaml: Dict) -> str:
        _chart_name = chart_yaml["name"]
        assert isinstance(_chart_name, str)
        return _chart_name

    conftest_globals["chart_name"] = chart_name

    @pytest.fixture(scope="package")
    def chart_version(chart_yaml: Dict) -> str:
        _chart_version = chart_yaml["version"]
        assert isinstance(_chart_version, str)
        return _chart_version

    conftest_globals["chart_version"] = chart_version

    @pytest.fixture(scope="package")
    def chart_yaml() -> Dict:
        return get_chart_yaml(chart_dir_name)

    conftest_globals["chart_yaml"] = chart_yaml

    @pytest.fixture(scope="package")
    def chart_values() -> Dict:
        return get_chart_values(chart_dir_name)

    conftest_globals["chart_values"] = chart_values

    @pytest.fixture(scope="package")
    def chart_values_schema() -> Dict:
        return get_chart_values_schema(chart_dir_name)

    conftest_globals["chart_values_schema"] = chart_values_schema
