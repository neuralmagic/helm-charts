from typing import Dict, Optional

from pytest_helm_templates import HelmRunner


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
