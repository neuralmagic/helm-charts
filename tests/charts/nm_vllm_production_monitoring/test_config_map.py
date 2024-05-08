from typing import Dict, Optional

import yaml
from pytest_helm_templates import HelmRunner


def test_static_and_default_values(
    chart_name: str,
    chart_values: Dict,
    grafana_dependency_default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    name = "name-given-to-release"
    subject = render_subject(
        name=name,
        helm_runner=helm_runner,
    )

    assert subject["apiVersion"] == "v1"
    assert subject["kind"] == "ConfigMap"

    metadata = subject["metadata"]
    assert metadata
    assert metadata["name"] == f"{name}-{chart_name}-grafana-datasource"

    datasources_config = grafana_dependency_default_values["sidecar"]["datasources"]
    label = datasources_config["label"]
    label_value = datasources_config["labelValue"]

    labels = metadata["labels"]
    assert labels
    assert labels[label] == label_value

    data = subject["data"]
    assert data
    datasource_yaml = data["datasource.yaml"]
    assert datasource_yaml
    datasource_data = yaml.safe_load(datasource_yaml)
    assert datasource_data

    assert datasource_data["apiVersion"] == 1
    datasources = datasource_data["datasources"]
    assert datasources

    datasource = datasources[0]

    assert datasource["access"] == "proxy"
    assert datasource["isDefault"] is True
    assert datasource["name"] == "Prometheus"
    assert datasource["type"] == "prometheus"
    datasource_values = chart_values["datasource"]
    assert datasource["uid"] == datasource_values["uid"]
    assert datasource["url"] == datasource_values["url"]

    datasource_json_data = datasource["jsonData"]
    assert datasource_json_data
    assert datasource_json_data["httpMethod"] == datasource_values["httpMethod"]
    assert datasource_json_data["timeInterval"] == datasource_values["timeInterval"]


def test_grafana_datasources_label_and_label_value_can_be_configured(
    helm_runner: HelmRunner,
) -> None:
    label = "grafana_datasource_label"
    label_value = "grafana_datasource_label_value"
    subject = render_subject(
        helm_runner=helm_runner,
        values={
            "grafanaDatasourcesLabelOverride": label,
            "grafanaDatasourcesLabelValueOverride": label_value,
        },
    )
    labels = subject["metadata"]["labels"]
    assert labels[label] == label_value


def test_grafana_datasources_label_and_label_value_can_take_values_from_grafana_chart(
    helm_runner: HelmRunner,
) -> None:
    label = "grafana_datasource_label"
    label_value = "grafana_datasource_label_value"
    subject = render_subject(
        helm_runner=helm_runner,
        values={
            "grafana": {
                "sidecar": {
                    "datasources": {
                        "label": label,
                        "labelValue": label_value,
                    },
                },
            },
        },
    )
    labels = subject["metadata"]["labels"]
    assert labels[label] == label_value


def test_grafana_datasources_label_and_label_value_defaults_match_grafana_defaults(
    grafana_dependency_default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    subject = render_subject(
        helm_runner=helm_runner,
        # Make sure we don't get the values from grafana values
        values={
            "grafana": {
                "sidecar": {
                    "datasources": {
                        "label": None,
                        "labelValue": None,
                    },
                },
            },
        },
    )

    datasources_config = grafana_dependency_default_values["sidecar"]["datasources"]
    label = datasources_config["label"]
    label_value = datasources_config["labelValue"]

    labels = subject["metadata"]["labels"]
    assert labels[label] == label_value


def test_datasource_http_method_can_be_configured(helm_runner: HelmRunner) -> None:
    http_method = "POST"
    subject = render_subject(
        helm_runner=helm_runner,
        values={"datasource": {"httpMethod": http_method}},
    )
    datasource_yaml_unparsed = subject["data"]["datasource.yaml"]
    datasource_yaml = yaml.safe_load(datasource_yaml_unparsed)
    datasource = datasource_yaml["datasources"][0]
    actual_http_method = datasource["jsonData"]["httpMethod"]
    assert actual_http_method == http_method


def test_datasource_is_default_can_be_configured(helm_runner: HelmRunner) -> None:
    is_default = False
    subject = render_subject(
        helm_runner=helm_runner,
        values={"datasource": {"isDefault": is_default}},
    )
    datasource_yaml_unparsed = subject["data"]["datasource.yaml"]
    datasource_yaml = yaml.safe_load(datasource_yaml_unparsed)
    datasource = datasource_yaml["datasources"][0]
    assert datasource["isDefault"] == is_default


def test_datasource_name_can_be_configured(helm_runner: HelmRunner) -> None:
    name = "not-prometheus"
    subject = render_subject(
        helm_runner=helm_runner,
        values={"datasource": {"name": name}},
    )
    datasource_yaml_unparsed = subject["data"]["datasource.yaml"]
    datasource_yaml = yaml.safe_load(datasource_yaml_unparsed)
    datasource = datasource_yaml["datasources"][0]
    assert datasource["name"] == name


def test_datasource_time_interval_can_be_configured(helm_runner: HelmRunner) -> None:
    time_interval = "POST"
    subject = render_subject(
        helm_runner=helm_runner,
        values={"datasource": {"timeInterval": time_interval}},
    )
    datasource_yaml_unparsed = subject["data"]["datasource.yaml"]
    datasource_yaml = yaml.safe_load(datasource_yaml_unparsed)
    datasource = datasource_yaml["datasources"][0]
    actual_time_interval = datasource["jsonData"]["timeInterval"]
    assert actual_time_interval == time_interval


def test_datasource_uid_can_be_configured(helm_runner: HelmRunner) -> None:
    uid = "POST"
    subject = render_subject(
        helm_runner=helm_runner,
        values={"datasource": {"uid": uid}},
    )
    datasource_yaml_unparsed = subject["data"]["datasource.yaml"]
    datasource_yaml = yaml.safe_load(datasource_yaml_unparsed)
    datasource = datasource_yaml["datasources"][0]
    actual_uid = datasource["uid"]
    assert actual_uid == uid


def test_datasource_url_can_be_configured(helm_runner: HelmRunner) -> None:
    url = "POST"
    subject = render_subject(
        helm_runner=helm_runner,
        values={"datasource": {"url": url}},
    )
    datasource_yaml_unparsed = subject["data"]["datasource.yaml"]
    datasource_yaml = yaml.safe_load(datasource_yaml_unparsed)
    datasource = datasource_yaml["datasources"][0]
    actual_url = datasource["url"]
    assert actual_url == url


def render_subject(
    helm_runner: HelmRunner,
    name: str = "name-given-to-the-release",
    values: Optional[Dict] = None,
) -> Dict:
    manifests = helm_runner.template(
        chart="nm-vllm-production-monitoring",
        name=name,
        show_only=["templates/config-map-datasources.yaml"],
        values=[values] if values else [],
    )
    subject = manifests[0]
    assert subject["kind"] == "ConfigMap"
    return subject
