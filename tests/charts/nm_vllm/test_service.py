from typing import Dict, Optional

import pytest
from pytest_helm_templates import HelmRunner


def test_constant_and_default_values(
    app_version: str,
    chart_name: str,
    chart_version: str,
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    name = "name-given-to-the-release"
    subject = render_subject(
        helm_runner=helm_runner,
        name=name,
    )

    assert "Service" == subject["kind"]
    assert "v1" == subject["apiVersion"]

    metadata = subject["metadata"]
    assert metadata
    assert metadata["name"] == f"{name}-{chart_name}"
    assert "annotations" not in metadata

    labels = metadata["labels"]
    assert labels
    assert labels["app.kubernetes.io/instance"] == name
    assert labels["app.kubernetes.io/managed-by"] == "Helm"
    assert labels["app.kubernetes.io/name"] == chart_name
    assert labels["app.kubernetes.io/version"] == app_version
    assert labels["helm.sh/chart"] == f"{chart_name}-{chart_version}"

    spec = subject["spec"]
    assert spec
    assert spec["ports"]
    assert len(spec["ports"]) == 1

    port = spec["ports"][0]
    assert port["name"] == "http"
    assert port["port"] == default_values["service"]["port"]
    assert port["protocol"] == "TCP"
    assert port["targetPort"] == "http"

    selector = spec["selector"]
    assert selector["app.kubernetes.io/instance"] == name
    assert selector["app.kubernetes.io/name"] == chart_name

    assert spec["type"] == default_values["service"]["type"]


@pytest.mark.parametrize(
    "full_name_override,expected_name",
    (
        (
            "full-name-override",
            "full-name-override",
        ),
        (
            "full-name-override-that-is-too-long-and-will-be-truncated-here-the-end",
            "full-name-override-that-is-too-long-and-will-be-truncated-here",
        ),
        (
            "full-name-override-that-is-too-long-and-will-be-truncated-here-",
            "full-name-override-that-is-too-long-and-will-be-truncated-here",
        ),
    ),
)
def test_full_name_override_overrides_name(
    app_version: str,
    chart_name: str,
    chart_version: str,
    expected_name: str,
    full_name_override: str,
    helm_runner: HelmRunner,
) -> None:
    name = "name-given-to-the-release"
    subject = render_subject(
        helm_runner=helm_runner,
        name=name,
        values={"fullnameOverride": full_name_override},
    )

    assert subject["metadata"]["name"] == expected_name


@pytest.mark.parametrize(
    "given_name,name_override,expected_name",
    (
        (
            "given-name",
            "name-override",
            "given-name-name-override",
        ),
        # if name includes the release name, the release name isn't appended
        (
            "nm-vllm-included-in-name",
            "nm-vllm",
            "nm-vllm-included-in-name",
        ),
        (
            "given-name",
            "name-override-that-is-too-long-and-will-be-truncated-here-the-end",
            "given-name-name-override-that-is-too-long-and-will-be-truncated",
        ),
        (
            "given-name",
            "name-override-that-is-too-long-and-will-be-truncated-",
            "given-name-name-override-that-is-too-long-and-will-be-truncated",
        ),
    ),
)
def test_name_override_overrides_name(
    app_version: str,
    chart_name: str,
    chart_version: str,
    expected_name: str,
    given_name: str,
    helm_runner: HelmRunner,
    name_override: str,
) -> None:
    subject = render_subject(
        helm_runner=helm_runner,
        name=given_name,
        values={"nameOverride": name_override},
    )

    assert subject["metadata"]["name"] == expected_name


def test_includes_custom_annotations(helm_runner: HelmRunner) -> None:
    annotations = {
        "baz": "bat",
        "foo": "bar",
        "meow/meow": "cat",
    }
    subject = render_subject(
        helm_runner=helm_runner,
        values={"service": {"annotations": annotations}},
    )
    assert annotations == subject["metadata"]["annotations"]


def test_port_can_be_configured(helm_runner: HelmRunner) -> None:
    port = 7777
    subject = render_subject(
        helm_runner=helm_runner,
        values={"service": {"port": port}},
    )
    assert port == subject["spec"]["ports"][0]["port"]


def test_type_can_be_configured(helm_runner: HelmRunner) -> None:
    service_type = "ClusterIP"
    subject = render_subject(
        helm_runner=helm_runner,
        values={"service": {"type": service_type}},
    )
    assert service_type == subject["spec"]["type"]


def render_subject(
    helm_runner: HelmRunner,
    name: str = "name-given-to-the-release",
    values: Optional[Dict] = None,
) -> Dict:
    manifests = helm_runner.template(
        chart="nm-vllm",
        name=name,
        show_only=["templates/service.yaml"],
        values=[values] if values else [],
    )
    subject = manifests[0]
    assert subject["kind"] == "Service"
    return subject
