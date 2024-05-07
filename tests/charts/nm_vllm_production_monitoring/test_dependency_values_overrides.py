from typing import Dict

import pytest
from pytest_helm_templates import HelmRunner

from tests.test_helpers import ChartDependencies
from tests.test_helpers.test_assertions import assert_dependency_value_override


def test_nm_vllm_pod_annotations_includes_prometheus_scrape(
    chart_computed_values: Dict,
    nm_vllm_default_values: Dict,
) -> None:
    assert_dependency_value_override(
        dependency_computed_values=chart_computed_values["nm-vllm"],
        dependency_default_values=nm_vllm_default_values,
        expected_default_value={},
        expected_override_value={"prometheus.io/scrape": "true"},
        path=["podAnnotations"],
    )


def test_grafana_sidecar_dashboards_is_enabled(
    chart_computed_values: Dict,
    grafana_default_values: Dict,
) -> None:
    assert_dependency_value_override(
        dependency_computed_values=chart_computed_values["grafana"],
        dependency_default_values=grafana_default_values,
        expected_default_value=False,
        expected_override_value=True,
        path=["sidecar", "dashboards", "enabled"],
    )


def test_grafana_sidecar_datasources_is_enabled(
    chart_computed_values: Dict,
    grafana_default_values: Dict,
) -> None:
    assert_dependency_value_override(
        dependency_computed_values=chart_computed_values["grafana"],
        dependency_default_values=grafana_default_values,
        expected_default_value=False,
        expected_override_value=True,
        path=["sidecar", "datasources", "enabled"],
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
