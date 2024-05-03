from typing import Dict

import pytest

from tests.test_helpers import get_chart_values, get_chart_values_schema, get_chart_yaml


CHART_DIR_NAME = "nm-vllm"


@pytest.fixture
def app_version(chart_yaml: Dict) -> str:
    _app_version = chart_yaml["appVersion"]
    assert isinstance(_app_version, str)
    return _app_version


@pytest.fixture
def chart_name(chart_yaml: Dict) -> str:
    _chart_name = chart_yaml["name"]
    assert isinstance(_chart_name, str)
    return _chart_name


@pytest.fixture
def chart_version(chart_yaml: Dict) -> str:
    _chart_version = chart_yaml["version"]
    assert isinstance(_chart_version, str)
    return _chart_version


@pytest.fixture
def chart_yaml() -> Dict:
    return get_chart_yaml(CHART_DIR_NAME)


@pytest.fixture
def chart_values() -> Dict:
    return get_chart_values(CHART_DIR_NAME)


@pytest.fixture
def chart_values_schema() -> Dict:
    return get_chart_values_schema(CHART_DIR_NAME)
