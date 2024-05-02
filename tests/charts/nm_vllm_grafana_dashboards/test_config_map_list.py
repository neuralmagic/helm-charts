from typing import Dict, Optional

from pytest_helm_templates import HelmRunner


def test_expected_dashboard_config_maps_are_included(
    app_version: str,
    chart_name: str,
    chart_version: str,
    default_values: Dict,
    helm_runner: HelmRunner,
    raw_dashboards: Dict[str, str],
) -> None:
    name = "name-given-to-the-chart"
    subject = render_subject(helm_runner=helm_runner, name=name)

    assert subject["apiVersion"] == "v1"
    assert subject["kind"] == "ConfigMapList"

    dashboards = subject["items"]
    assert dashboards
    assert len(dashboards) == len(raw_dashboards)

    for dashboard in dashboards:
        assert dashboard["apiVersion"] == "v1"
        assert dashboard["kind"] == "ConfigMap"

        metadata = dashboard["metadata"]
        assert metadata

        labels = metadata["labels"]
        assert labels
        assert labels["app.kubernetes.io/instance"] == name
        assert labels["app.kubernetes.io/managed-by"] == "Helm"
        assert labels["app.kubernetes.io/name"] == chart_name
        assert labels["app.kubernetes.io/version"] == app_version
        assert labels["helm.sh/chart"] == f"{chart_name}-{chart_version}"
        assert labels[default_values["label"]] == default_values["labelValue"]

        data = dashboard["data"]
        for dashboard_file_name, dashboard_raw in data.items():
            expected_dashboard = raw_dashboards[dashboard_file_name]
            assert dashboard_raw == expected_dashboard


def render_subject(
    helm_runner: HelmRunner,
    name: str = "name-given-to-the-chart",
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
