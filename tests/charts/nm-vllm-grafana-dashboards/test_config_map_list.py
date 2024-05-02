from typing import Dict, Optional

from pytest_helm_templates import HelmRunner


def test_expected_dashboard_config_maps_are_included(
    default_values: Dict,
    helm_runner: HelmRunner,
    raw_dashboards: Dict[str, str],
) -> None:
    subject = render_subject(helm_runner=helm_runner)

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
