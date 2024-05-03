from typing import Dict, Optional

from pytest_helm_templates import HelmRunner


def test_expected_dashboard_config_maps_are_included(
    app_version: str,
    chart_name: str,
    chart_values: Dict,
    chart_version: str,
    helm_runner: HelmRunner,
    raw_dashboards: Dict[str, str],
) -> None:
    name = "name-given-to-the-release"
    subject = render_subject(helm_runner=helm_runner, name=name)

    assert subject["apiVersion"] == "v1"
    assert subject["kind"] == "ConfigMapList"

    dashboards = subject["items"]
    assert dashboards
    assert len(dashboards) == len(raw_dashboards)

    for dashboard in dashboards:
        data = dashboard["data"]
        # Each dashboard gets its own ConfigMap
        assert len(data) == 1

        # Start by looking at the data so we know the name of the dashboard
        dashboard_file_name, dashboard_raw = list(data.items())[0]
        expected_dashboard = raw_dashboards[dashboard_file_name]
        assert dashboard_raw == expected_dashboard

        assert dashboard["apiVersion"] == "v1"
        assert dashboard["kind"] == "ConfigMap"

        metadata = dashboard["metadata"]
        assert metadata

        dashboard_name = dashboard_file_name.replace(".json", "")
        metadata_name = f"{name}-{chart_name}-{dashboard_name}"[:63].rstrip("-")
        assert metadata["name"] == metadata_name

        labels = metadata["labels"]
        assert labels
        assert labels["app.kubernetes.io/instance"] == name
        assert labels["app.kubernetes.io/managed-by"] == "Helm"
        assert labels["app.kubernetes.io/name"] == chart_name
        assert labels["app.kubernetes.io/version"] == app_version
        assert labels["helm.sh/chart"] == f"{chart_name}-{chart_version}"
        assert labels[chart_values["label"]] == chart_values["labelValue"]

def test_label_and_label_value_can_be_configured(
    helm_runner: HelmRunner,
) -> None:
    label = "grafana_dashboard"
    label_value = "grafana_dashboard_value"
    subject = render_subject(
        helm_runner=helm_runner,
        values={"label": label, "labelValue": label_value},
    )
    dashboards = subject["items"]
    for dashboard in dashboards:
        labels = dashboard["metadata"]["labels"]
        assert  labels[label] == label_value


def render_subject(
    helm_runner: HelmRunner,
    name: str = "name-given-to-the-release",
    values: Optional[Dict] = None,
) -> Dict:
    manifests = helm_runner.template(
        chart="nm-vllm-grafana-dashboards",
        name=name,
        show_only=["templates/config-map-list.yaml"],
        values=[values] if values else [],
    )
    subject = manifests[0]
    assert subject["kind"] == "ConfigMapList"
    return subject
