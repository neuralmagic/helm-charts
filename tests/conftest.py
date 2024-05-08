from typing import Dict

import pytest
from pytest_helm_templates import HelmRunner

from tests.test_helpers import charts_path


@pytest.fixture(scope="session")
def helm_runner() -> HelmRunner:
    return HelmRunner(cwd=charts_path())


@pytest.fixture(scope="session")
def grafana_default_values(
    helm_runner: HelmRunner,
) -> Dict:
    return helm_runner.values(
        chart="grafana",
        repo="https://grafana.github.io/helm-charts",
        version="7.3.9",
    )
