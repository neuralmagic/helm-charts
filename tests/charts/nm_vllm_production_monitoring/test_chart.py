from typing import Dict, List, Optional

from pytest_helm_templates import HelmRunner

from tests.test_helpers.test_assertions import assert_values_are_known_to_schema


def test_values_are_known_to_schema(
    chart_values: Dict,
    chart_values_schema: Dict,
) -> None:
    assert_values_are_known_to_schema(
        chart_values=chart_values,
        chart_values_schema=chart_values_schema,
    )


def test_grafana_sub_chart_can_be_disabled(helm_runner: HelmRunner) -> None:
    for grafana_enabled in [False, True]:
        resources = render_chart(
            helm_runner=helm_runner,
            name="nm-vllm",
            values={"grafana": {"enabled": grafana_enabled}},
        )
        deployment_names = [
            resource["metadata"]["name"]
            for resource in resources
            if resource["kind"] == "Deployment"
        ]
        assert ("nm-vllm-grafana" in deployment_names) is grafana_enabled


def test_nm_vllm_grafana_dashboards_sub_chart_can_be_disabled(
    helm_runner: HelmRunner,
) -> None:
    for nm_vllm_grafana_dashboards_enabled in [False, True]:
        resources = render_chart(
            helm_runner=helm_runner,
            name="nm-vllm",
            values={
                "nm-vllm-grafana-dashboards": {
                    "enabled": nm_vllm_grafana_dashboards_enabled
                },
            },
        )
        config_map_names = [
            resource["metadata"]["name"]
            for resource in resources
            if resource["kind"] == "ConfigMap"
        ]
        assert (
            "nm-vllm-nm-vllm-grafana-dashboards-default" in config_map_names
        ) is nm_vllm_grafana_dashboards_enabled


def test_prometheus_sub_chart_can_be_disabled(helm_runner: HelmRunner) -> None:
    for prometheus_enabled in [False, True]:
        resources = render_chart(
            helm_runner=helm_runner,
            name="nm-vllm",
            values={"prometheus": {"enabled": prometheus_enabled}},
        )
        deployment_names = [
            resource["metadata"]["name"]
            for resource in resources
            if resource["kind"] == "Deployment"
        ]
        assert ("nm-vllm-prometheus-server" in deployment_names) is prometheus_enabled


def render_chart(
    helm_runner: HelmRunner,
    name: str = "name-given-to-the-release",
    values: Optional[Dict] = None,
) -> List[Dict]:
    return helm_runner.template(
        chart="nm-vllm-production-monitoring",
        name=name,
        values=[values] if values else [],
    )
