from typing import Dict, Optional

import pytest
import yaml
from pytest_helm_templates import HelmRunner


@pytest.mark.parametrize(
    "values",
    (
        {},
        {"prometheus": {"server": {"fullnameOverride": "meow"}}},
        {
            "prometheus": {
                "server": {
                    "fullnameOverride": (
                        "long-long-long-long-long-long-long-long-long-long"
                        "long-long-long-long-long-long-long-long-long-long"
                    ),
                },
            },
        },
        {"prometheus": {"server": {"name": "bender"}}},
        {"prometheus": {"server": {"name": "abc"}}},
        {"prometheus": {"server": {"name": "planet-express"}}},
        {
            "prometheus": {
                "server": {
                    "name": (
                        "long-long-long-long-long-long-long-long-long-long"
                        "long-long-long-long-long-long-long-long-long-long"
                    ),
                },
            },
        },
        {"prometheus": {"nameOverride": "bart-simpson"}},
        {
            "prometheus": {
                "server": {
                    "nameOverride": (
                        "long-long-long-long-long-long-long-long-long-long"
                        "long-long-long-long-long-long-long-long-long-long"
                    ),
                },
            },
        },
    ),
)
@pytest.mark.parametrize(
    "name",
    (
        "abc",
        "nm-vllm",
        "planet-express",
        "prometheus",
    ),
)
def test_grafana_datasource_url_matches_prometheus_service_name(
    helm_runner: HelmRunner,
    name: str,
    values: Dict,
) -> None:
    prometheus_service_name = _get_prometheus_service_name(
        helm_runner=helm_runner,
        name=name,
        values=values,
    )

    datasource_config_map_url = _get_datasource_config_map_url(
        helm_runner=helm_runner,
        name=name,
        values=values,
    )

    prometheus_service_url = f"http://{prometheus_service_name}/"
    assert datasource_config_map_url == prometheus_service_url


def _get_prometheus_service_name(
    helm_runner: HelmRunner,
    name: str,
    values: Optional[Dict] = None,
) -> str:
    all_the_resources = helm_runner.template(
        chart="nm-vllm-production-monitoring",
        name=name,
        values=[values] if values else [],
    )
    services = [
        resource for resource in all_the_resources if resource.get("kind") == "Service"
    ]
    for service in services:
        if service["spec"]["ports"][0].get("targetPort") == 9090:
            return str(service["metadata"]["name"])

    raise ValueError("Couldn't find prometheus service")


def _get_datasource_config_map_url(
    helm_runner: HelmRunner,
    name: str,
    values: Optional[Dict] = None,
) -> str:
    datasource_config_map = helm_runner.template(
        chart="nm-vllm-production-monitoring",
        name=name,
        show_only=["templates/config-map-datasources.yaml"],
        values=[values] if values else [],
    )[0]
    assert datasource_config_map["kind"] == "ConfigMap"
    datasource_yaml = datasource_config_map["data"]["datasource.yaml"]
    datasource = yaml.safe_load(datasource_yaml)
    return str(datasource["datasources"][0]["url"])
