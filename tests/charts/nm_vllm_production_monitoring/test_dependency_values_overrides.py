from typing import Dict

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
