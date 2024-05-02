from typing import Any, Dict, List, Optional, Union

import pytest
from pytest_helm_templates import HelmRunner


def test_constant_and_default_values(
    app_version: str,
    chart_name: str,
    chart_version: str,
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    name = "name-given-to-the-chart"
    subject = render_subject(
        helm_runner=helm_runner,
        name=name,
    )

    assert "Deployment" == subject["kind"]
    assert "apps/v1" == subject["apiVersion"]

    deployment_metadata = subject["metadata"]
    assert deployment_metadata
    assert deployment_metadata["name"] == f"{name}-{chart_name}"

    deployment_labels = deployment_metadata["labels"]
    assert deployment_labels
    assert deployment_labels["app.kubernetes.io/instance"] == name
    assert deployment_labels["app.kubernetes.io/managed-by"] == "Helm"
    assert deployment_labels["app.kubernetes.io/name"] == chart_name
    assert deployment_labels["app.kubernetes.io/version"] == app_version
    assert deployment_labels["helm.sh/chart"] == f"{chart_name}-{chart_version}"

    deployment_spec = subject["spec"]
    assert deployment_spec

    assert deployment_spec["replicas"] == default_values["replicaCount"]

    match_labels = deployment_spec["selector"]["matchLabels"]
    assert match_labels["app.kubernetes.io/instance"] == name
    assert match_labels["app.kubernetes.io/name"] == chart_name

    template = deployment_spec["template"]
    assert template

    pod_metadata = template["metadata"]
    assert pod_metadata

    assert "annotations" not in pod_metadata

    pod_labels = pod_metadata["labels"]
    assert pod_labels
    assert pod_labels["app.kubernetes.io/instance"] == name
    assert pod_labels["app.kubernetes.io/managed-by"] == "Helm"
    assert pod_labels["app.kubernetes.io/name"] == chart_name
    assert pod_labels["app.kubernetes.io/version"] == app_version
    assert pod_labels["helm.sh/chart"] == f"{chart_name}-{chart_version}"

    pod_spec = template["spec"]
    assert pod_spec

    assert "affinity" not in pod_spec

    containers = pod_spec["containers"]
    assert containers
    assert len(containers) == 1

    container = containers[0]
    expected_command = get_expected_command(
        host=default_values["apiServer"]["host"],
        model_name=default_values["modelName"],
        port=default_values["apiServer"]["port"],
    )
    assert container["command"] == expected_command

    expected_image = get_expected_image(
        repository=default_values["image"]["repository"],
        tag=default_values["image"]["tag"],
    )
    assert container["image"] == expected_image

    assert container["imagePullPolicy"] == default_values["image"]["pullPolicy"]

    assert "livenessProbe" not in container

    assert container["name"] == chart_name

    ports = container["ports"]
    assert ports
    assert len(ports) == 1

    port = ports[0]
    assert port
    assert port["containerPort"] == default_values["apiServer"]["port"]
    assert port["name"] == "http"
    assert port["protocol"] == "TCP"

    readiness_probe = container["readinessProbe"]
    assert readiness_probe

    http_get = readiness_probe["httpGet"]
    default_readiness_probe = default_values["readinessProbe"]
    default_http_get = default_readiness_probe["httpGet"]
    assert http_get
    assert http_get["path"] == default_http_get["path"]
    assert http_get["port"] == default_http_get["port"]
    default_initial_delay_seconds = default_readiness_probe["initialDelaySeconds"]
    assert readiness_probe["initialDelaySeconds"] == default_initial_delay_seconds
    assert readiness_probe["periodSeconds"] == default_readiness_probe["periodSeconds"]

    assert "resources" not in container
    assert "securityContext" not in container
    assert "volumeMounts" not in container

    assert "nodeSelector" not in pod_spec
    assert "securityContext" not in pod_spec
    assert "tolerations" not in pod_spec
    assert "volumes" not in pod_spec


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
    name = "name-given-to-the-chart"
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


def test_replicas_can_be_configured(helm_runner: HelmRunner) -> None:
    replica_count = 10
    subject = render_subject(
        helm_runner=helm_runner,
        values={"replicaCount": replica_count},
    )
    actual_replica_count = subject["spec"]["replicas"]
    assert replica_count == actual_replica_count


def test_pod_annotations_is_omitted_when_not_given(helm_runner: HelmRunner) -> None:
    subject = render_subject(
        helm_runner=helm_runner,
        values={"podAnnotations": None},
    )
    assert "annotations" not in subject["spec"]["template"]["metadata"]


def test_pod_annotations_can_be_configured(helm_runner: HelmRunner) -> None:
    pod_annotations = {
        "baz": "bat",
        "foo": "bar",
        "meow/meow": "cat",
    }
    subject = render_subject(
        helm_runner=helm_runner,
        values={"podAnnotations": pod_annotations},
    )
    actual_annotations = subject["spec"]["template"]["metadata"]["annotations"]
    assert pod_annotations == actual_annotations


def test_pod_labels_can_be_configured(helm_runner: HelmRunner) -> None:
    pod_labels = {
        "baz": "bat",
        "foo": "bar",
        "meow/meow": "cat",
    }
    subject = render_subject(
        helm_runner=helm_runner,
        values={"podLabels": pod_labels},
    )
    actual_labels = subject["spec"]["template"]["metadata"]["labels"]
    for label_key, label_value in pod_labels.items():
        assert actual_labels[label_key] == label_value


def test_affinity_is_omitted_when_not_given(helm_runner: HelmRunner) -> None:
    subject = render_subject(
        helm_runner=helm_runner,
        values={"affinity": None},
    )
    assert "affinity" not in subject["spec"]["template"]["metadata"]


def test_affinity_can_be_configured(helm_runner: HelmRunner) -> None:
    affinity = {
        "nodeAffinity": {
            "requiredDuringSchedulingIgnoredDuringExecution": {
                "nodeSelectorTerms": [
                    {
                        "matchExpressions": [
                            {
                                "key": "topology.kubernetes.io/zone",
                                "operator": "In",
                                "values": ["antarctica-east1"],
                            }
                        ],
                    }
                ],
            },
        },
    }
    subject = render_subject(
        helm_runner=helm_runner,
        values={"affinity": affinity},
    )
    actual_affinity = subject["spec"]["template"]["spec"]["affinity"]
    assert actual_affinity == affinity


def test_model_name_can_be_configured(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    model_name = "foo/bar"
    subject = render_subject(
        helm_runner=helm_runner,
        values={"modelName": model_name},
    )
    expected_command = get_expected_command(
        host=default_values["apiServer"]["host"],
        model_name=model_name,
        port=default_values["apiServer"]["port"],
    )
    actual_command = get_container(subject)["command"]
    assert actual_command == expected_command


def test_api_server_host_can_be_configured(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    host = "127.0.0.1"
    subject = render_subject(
        helm_runner=helm_runner,
        values={"apiServer": {"host": host}},
    )
    expected_command = get_expected_command(
        host=host,
        model_name=default_values["modelName"],
        port=default_values["apiServer"]["port"],
    )
    actual_command = get_container(subject)["command"]
    assert actual_command == expected_command


def test_api_server_port_can_be_configured(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    port = 9753
    subject = render_subject(
        helm_runner=helm_runner,
        values={"apiServer": {"port": port}},
    )
    expected_command = get_expected_command(
        host=default_values["apiServer"]["host"],
        model_name=default_values["modelName"],
        port=port,
    )
    container = get_container(subject)
    actual_command = container["command"]
    assert actual_command == expected_command
    assert container["ports"][0]["containerPort"] == port


def test_api_server_extra_args_can_be_provided(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    extra_args = [
        "--dtype",
        "float16",
        "--int",
        7,
        "--bool",
        True,
        "--float",
        1.01,
        "--float",
        1.01,
        "--e-float",
        1.203e2,
    ]
    subject = render_subject(
        helm_runner=helm_runner,
        values={"apiServer": {"extraArgs": extra_args}},
    )
    expected_command = get_expected_command(
        extra_args=extra_args,
        host=default_values["apiServer"]["host"],
        model_name=default_values["modelName"],
        port=default_values["apiServer"]["port"],
    )
    actual_command = get_container(subject)["command"]
    assert actual_command == expected_command


def test_container_image_repository_can_be_configured(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    repository = "some.repo"
    subject = render_subject(
        helm_runner=helm_runner,
        values={"image": {"repository": repository}},
    )
    expected_image = get_expected_image(
        repository=repository,
        tag=default_values["image"]["tag"],
    )
    assert get_container(subject)["image"] == expected_image


def test_container_image_tag_can_be_configured(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    tag = "v1000"
    subject = render_subject(
        helm_runner=helm_runner,
        values={"image": {"tag": tag}},
    )
    expected_image = get_expected_image(
        repository=default_values["image"]["repository"],
        tag=tag,
    )
    assert get_container(subject)["image"] == expected_image


def test_container_image_tag_defaults_to_app_version_when_omitted(
    app_version: str,
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    subject = render_subject(
        helm_runner=helm_runner,
        values={"image": {"tag": None}},
    )
    expected_image = get_expected_image(
        repository=default_values["image"]["repository"],
        tag=app_version,
    )
    assert get_container(subject)["image"] == expected_image


def test_container_image_pull_policy_can_be_configured(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    pull_policy = "Never"
    subject = render_subject(
        helm_runner=helm_runner,
        values={"image": {"pullPolicy": pull_policy}},
    )
    assert get_container(subject)["imagePullPolicy"] == pull_policy


def test_container_liveness_probe_is_omitted_when_not_given(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    subject = render_subject(
        helm_runner=helm_runner,
        values={"livenessProbe": None},
    )
    assert "livenessProbe" not in get_container(subject)


def test_container_liveness_probe_can_be_configured(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    liveness_probe = {
        "httpGet": {
            "path": "/",
            "port": "http",
        },
        "initialDelaySeconds": 100,
        "periodSeconds": 300,
    }
    subject = render_subject(
        helm_runner=helm_runner,
        values={"livenessProbe": liveness_probe},
    )
    assert get_container(subject)["livenessProbe"] == liveness_probe


def test_container_readiness_probe_is_omitted_when_not_given(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    subject = render_subject(
        helm_runner=helm_runner,
        values={"readinessProbe": None},
    )
    assert "readinessProbe" not in get_container(subject)


def test_container_readiness_probe_can_be_configured(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    readiness_probe = {
        "httpGet": {
            "path": "/readyz",
            "port": "https",
        },
        "initialDelaySeconds": 100,
        "periodSeconds": 300,
    }
    subject = render_subject(
        helm_runner=helm_runner,
        values={"readinessProbe": readiness_probe},
    )
    assert get_container(subject)["readinessProbe"] == readiness_probe


def test_container_resources_is_omitted_when_not_given(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    subject = render_subject(
        helm_runner=helm_runner,
        values={"resources": None},
    )
    assert "resources" not in get_container(subject)


def test_container_resources_can_be_configured(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    resources = {
        "limits": {
            "cpu": "1000m",
            "memory": "1G",
        },
        "requests": {
            "cpu": "100m",
            "memory": "128Mi",
        },
    }
    subject = render_subject(
        helm_runner=helm_runner,
        values={"resources": resources},
    )
    assert get_container(subject)["resources"] == resources


def test_container_security_context_is_omitted_when_not_given(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    subject = render_subject(
        helm_runner=helm_runner,
        values={"securityContext": None},
    )
    assert "securityContext" not in get_container(subject)


def test_container_security_context_can_be_configured(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    security_context = {"allowPrivilegeEscalation": False}
    subject = render_subject(
        helm_runner=helm_runner,
        values={"securityContext": security_context},
    )
    assert get_container(subject)["securityContext"] == security_context


def test_container_volume_mounts_is_omitted_when_not_given(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    subject = render_subject(
        helm_runner=helm_runner,
        values={"volumeMounts": None},
    )
    assert "volumeMounts" not in get_container(subject)


def test_container_volume_mounts_can_be_configured(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    volume_mounts = [{"name": "sec-ctx-vol", "mountPath": "/data/demo"}]
    subject = render_subject(
        helm_runner=helm_runner,
        values={"volumeMounts": volume_mounts},
    )
    assert get_container(subject)["volumeMounts"] == volume_mounts


def test_pod_node_selector_is_omitted_when_not_given(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    subject = render_subject(
        helm_runner=helm_runner,
        values={"nodeSelector": None},
    )
    assert "nodeSelector" not in subject["spec"]["template"]["spec"]


def test_pod_node_selector_can_be_configured(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    node_selector = {"disktype": "ssd"}
    subject = render_subject(
        helm_runner=helm_runner,
        values={"nodeSelector": node_selector},
    )
    assert subject["spec"]["template"]["spec"]["nodeSelector"] == node_selector


def test_pod_security_context_is_omitted_when_not_given(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    subject = render_subject(
        helm_runner=helm_runner,
        values={"podSecurityContext": None},
    )
    assert "securityContext" not in subject["spec"]["template"]["spec"]


def test_pod_security_context_can_be_configured(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    security_context = {
        "fsGroup": 2000,
        "runAsGroup": 3000,
        "runAsUser": 1000,
    }
    subject = render_subject(
        helm_runner=helm_runner,
        values={"podSecurityContext": security_context},
    )
    assert security_context == subject["spec"]["template"]["spec"]["securityContext"]


def test_pod_tolerations_is_omitted_when_not_given(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    subject = render_subject(
        helm_runner=helm_runner,
        values={"tolerations": None},
    )
    assert "tolerations" not in subject["spec"]["template"]["spec"]


def test_pod_tolerations_can_be_configured(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    tolerations = [
        {
            "effect": "NoSchedule",
            "key": "nodetype",
            "operator": "Equal",
            "value": "gpu",
        }
    ]
    subject = render_subject(
        helm_runner=helm_runner,
        values={"tolerations": tolerations},
    )
    assert subject["spec"]["template"]["spec"]["tolerations"] == tolerations


def test_pod_volumes_is_omitted_when_not_given(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    subject = render_subject(
        helm_runner=helm_runner,
        values={"volumes": None},
    )
    assert "volumes" not in subject["spec"]["template"]["spec"]


def test_pod_volumes_can_be_configured(
    default_values: Dict,
    helm_runner: HelmRunner,
) -> None:
    volumes = [
        {
            "name": "sec-ctx-vol",
            "emptyDir": {},
        }
    ]
    subject = render_subject(
        helm_runner=helm_runner,
        values={"volumes": volumes},
    )
    assert subject["spec"]["template"]["spec"]["volumes"] == volumes


def render_subject(
    helm_runner: HelmRunner,
    name: str = "name-given-to-the-chart",
    values: Optional[Dict] = None,
) -> Dict:
    manifests = helm_runner.template(
        chart="nm-vllm",
        name=name,
        show_only=["templates/deployment.yaml"],
        values=[values] if values else [],
    )
    subject = manifests[0]
    assert subject["kind"] == "Deployment"
    return subject


def get_container(subject: Dict) -> Dict:
    container = subject["spec"]["template"]["spec"]["containers"][0]
    assert isinstance(container, Dict)
    return container


def get_expected_command(
    host: str,
    model_name: str,
    port: Union[int, str],
    extra_args: List[Any] = [],
) -> List[str]:
    return [
        "python3",
        "-m",
        "vllm.entrypoints.openai.api_server",
        "--host",
        host,
        "--model",
        model_name,
        "--port",
        str(port),
        *[
            str(extra_arg).lower() if isinstance(extra_arg, bool) else str(extra_arg)
            for extra_arg in extra_args
        ],
    ]


def get_expected_image(repository: str, tag: str) -> str:
    return f"{repository}:{tag}"
