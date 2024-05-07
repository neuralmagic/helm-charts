from pathlib import Path
from typing import Dict

import pytest

from tests.test_helpers import chart_path, make_chart_fixtures


CHART_DIR_NAME = "nm-vllm-grafana-dashboards"


make_chart_fixtures(
    chart_dir_name=CHART_DIR_NAME,
    conftest_globals=globals(),
)


@pytest.fixture
def raw_dashboards() -> Dict[str, str]:
    dashboards_path = f"{chart_path(CHART_DIR_NAME)}/dashboards"
    dashboard_file_names = Path(dashboards_path).glob("*.json")
    _raw_dashboards = {}

    for dashboard_file_path in dashboard_file_names:
        with open(dashboard_file_path, encoding="utf-8", mode="r") as file:
            _raw_dashboards[dashboard_file_path.name] = file.read()

    return _raw_dashboards
