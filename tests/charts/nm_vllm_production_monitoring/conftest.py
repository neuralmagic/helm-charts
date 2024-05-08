from typing import Dict

import pytest
from pytest_helm_templates import HelmRunner

from tests.test_helpers import ChartDependencies, make_chart_fixtures, make_helm_runner


CHART_DIR_NAME = "nm-vllm-production-monitoring"


# Override helm_runner fixture so we can use it as a hook to ensure chart
# dependencies are installed.
@pytest.fixture(scope="package")
def helm_runner() -> HelmRunner:
    helm_runner = make_helm_runner()
    helm_runner.dependency_update_if_missing(chart=CHART_DIR_NAME)
    return helm_runner


make_chart_fixtures(
    chart_dir_name=CHART_DIR_NAME,
    conftest_globals=globals(),
)


def _get_dependency_values(
    chart_dependencies: ChartDependencies,
    dependency_name: str,
    helm_runner: HelmRunner,
) -> Dict:
    dependency = chart_dependencies[dependency_name]
    dependency_values = helm_runner.values(
        chart=dependency_name,
        repo=dependency.repository,
        version=dependency.version,
    )
    return dependency_values


# Cache dependency default values because they can be slow to fetch
@pytest.fixture(scope="module")
def nm_vllm_default_values(
    chart_dependencies: ChartDependencies,
    chart_name: str,
    helm_runner: HelmRunner,
) -> Dict:
    return _get_dependency_values(
        chart_dependencies=chart_dependencies,
        dependency_name="nm-vllm",
        helm_runner=helm_runner,
    )


@pytest.fixture(scope="module")
def grafana_default_values(
    chart_dependencies: ChartDependencies,
    chart_name: str,
    helm_runner: HelmRunner,
) -> Dict:
    return _get_dependency_values(
        chart_dependencies=chart_dependencies,
        dependency_name="grafana",
        helm_runner=helm_runner,
    )
