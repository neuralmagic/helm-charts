from pytest_helm_templates import HelmRunner


def test_notes_shows_expected_cluster_ip_notes_for_cluster_ip_service(
    helm_runner: HelmRunner,
) -> None:
    port = 80
    name = "nm-vllm"
    namespace = "test-namespace"
    notes = helm_runner.notes(
        chart="nm-vllm",
        name=name,
        namespace=namespace,
        values=[{"service": {"port": port, "type": "ClusterIP"}}],
    )
    expected_pod_name_command = (
        f"kubectl get pods --namespace {namespace}"
        f' -l "app.kubernetes.io/name={name},app.kubernetes.io/instance={name}"'
        ' -o jsonpath="{.items[0].metadata.name}"'
    )
    assert expected_pod_name_command in notes
    expected_container_port_command = (
        f"kubectl get pod --namespace {namespace} $POD_NAME"
        ' -o jsonpath="{.spec.containers[0].ports[0].containerPort}"'
    )
    assert expected_container_port_command in notes
    expected_port_forward_command = (
        f"kubectl --namespace {namespace} port-forward $POD_NAME 8080:$CONTAINER_PORT"
    )
    assert expected_port_forward_command in notes


def test_notes_shows_expected_node_port_notes_for_node_port_service(
    helm_runner: HelmRunner,
) -> None:
    name = "nm-vllm"
    namespace = "test-namespace"
    notes = helm_runner.notes(
        chart="nm-vllm",
        name=name,
        namespace=namespace,
        values=[{"service": {"type": "NodePort"}}],
    )
    expected_node_port_command = (
        f"kubectl get --namespace {namespace}"
        """ -o jsonpath="{.spec.ports[0].nodePort}" services"""
        f" {name}"
    )
    assert expected_node_port_command in notes
    expected_node_ip_command = (
        f"kubectl get nodes --namespace {namespace}"
        ' -o jsonpath="{.items[0].status.addresses[0].address}"'
    )
    assert expected_node_ip_command in notes


def test_notes_shows_expected_loadbalancer_notes_for_loadbalancer_service(
    helm_runner: HelmRunner,
) -> None:
    port = 80
    name = "nm-vllm"
    namespace = "test-namespace"
    notes = helm_runner.notes(
        chart="nm-vllm",
        name=name,
        namespace=namespace,
        values=[{"service": {"port": port, "type": "LoadBalancer"}}],
    )
    expected_status_watch_command = f"kubectl get --namespace {namespace} svc -w {name}"
    assert expected_status_watch_command in notes
    expected_service_ip_command = (
        f"kubectl get svc --namespace {namespace} {name}"
        ' --template "{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}'
    )
    assert expected_service_ip_command in notes
