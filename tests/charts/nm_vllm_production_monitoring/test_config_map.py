from typing import Dict, Optional

from pytest_helm_templates import HelmRunner
import yaml

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
    grafana_default_values: Dict,
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

    datasources_config = grafana_default_values["sidecar"]["datasources"]
    label = datasources_config["label"]
    label_value = datasources_config["labelValue"]

    labels = subject["metadata"]["labels"]
    assert labels[label] == label_value


def test_datasource_http_method_can_be_configured(
    helm_runner: HelmRunner,
) -> None:
    http_method = "POST"
    subject = render_subject(
        helm_runner=helm_runner,
        values={
            "datasource": {
                "httpMethod": http_method
            },
        }
    )
    datasource_yaml_unparsed = subject["data"]["datasource.yaml"]
    datasource_yaml = yaml.safe_load(datasource_yaml_unparsed)
    datasources = datasource_yaml["datasources"]
    for datasource in datasources:
        actual_http_method = datasource["jsonData"]["httpMethod"]
        assert actual_http_method == http_method


def test_datasource_scrape_internal_can_be_configured(
    helm_runner: HelmRunner,
) -> None:
    scrape_interval = "POST"
    subject = render_subject(
        helm_runner=helm_runner,
        values={
            "datasource": {
                "scrapeInterval": scrape_interval
            },
        }
    )
    datasource_yaml_unparsed = subject["data"]["datasource.yaml"]
    datasource_yaml = yaml.safe_load(datasource_yaml_unparsed)
    datasources = datasource_yaml["datasources"]
    for datasource in datasources:
        actual_scrape_interval = datasource["jsonData"]["timeInterval"]
        assert actual_scrape_interval == scrape_interval


def test_datasource_uid_can_be_configured(
    helm_runner: HelmRunner,
) -> None:
    uid = "POST"
    subject = render_subject(
        helm_runner=helm_runner,
        values={
            "datasource": {
                "uid": uid
            },
        }
    )
    datasource_yaml_unparsed = subject["data"]["datasource.yaml"]
    datasource_yaml = yaml.safe_load(datasource_yaml_unparsed)
    datasources = datasource_yaml["datasources"]
    for datasource in datasources:
        actual_uid = datasource["uid"]
        assert actual_uid == uid


def test_datasource_url_can_be_configured(
    helm_runner: HelmRunner,
) -> None:
    url = "POST"
    subject = render_subject(
        helm_runner=helm_runner,
        values={
            "datasource": {
                "url": url
            },
        }
    )
    datasource_yaml_unparsed = subject["data"]["datasource.yaml"]
    datasource_yaml = yaml.safe_load(datasource_yaml_unparsed)
    datasources = datasource_yaml["datasources"]
    for datasource in datasources:
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
