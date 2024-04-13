# nm-vllm

## Usage

[Helm](https://helm.sh) must be installed to use the charts.
Please refer to Helm's [documentation](https://helm.sh/docs/) to get started.

Once Helm is set up properly, add the repository as follows:

```console
helm repo add nm-vllm https://neuralmagic.github.io/helm-charts
```

You can then run `helm search repo nm-vllm` to see the charts.

## Customization
The following options are supported. See [values.yaml](/charts/nm-vllm/values.yaml) for more detailed documentation and examples:

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| nm-vllm | object | -- | Configuration for the nm-vllm server deployment and service. |
| nm-vllm.affinity | object | `{}` | Provide affinity rules for pod scheduling. |
| nm-vllm.apiServer | object | -- | Configuration for the nm-vllm API server |
| nm-vllm.apiServer.extraArgs | list | `[]` | Extra arguments to pass to the API server command |
| nm-vllm.fullnameOverride | string | `""` | Provide a name to substitute for the full names of resources. |
| nm-vllm.image | object | -- | Configuration for the application image. |
| nm-vllm.image.pullPolicy | string | `"IfNotPresent"` | The pull policy for the image. |
| nm-vllm.image.repository | string | `"ghcr.io/neuralmagic/nm-vllm-openai"` | The image repository for the application. |
| nm-vllm.image.tag | string | `"v0.1.0"` | The tag of the image to use. |
| nm-vllm.modelName | string | `"mistralai/Mistral-7B-v0.1"` | The name of the model to serve. |
| nm-vllm.nameOverride | string | `""` | Provide a name to substitute for the name of the chart. |
| nm-vllm.nodeSelector | object | `{}` | Node labels controlling where the pod will be scheduled. |
| nm-vllm.podAnnotations | object | `{}` | Annotations to add to the pod. |
| nm-vllm.podLabels | object | `{}` | Labels to add to the pod. |
| nm-vllm.podSecurityContext | object | `{}` | Defines the security options the pod should be run with. |
| nm-vllm.readinessProbe | object | -- | Readiness probe configuration for the container. |
| nm-vllm.readinessProbe.httpGet | object | `{"path":"/health","port":"http"}` | Specifies the http request to perform. |
| nm-vllm.readinessProbe.httpGet.path | string | `"/health"` | Path to access on the HTTP server. |
| nm-vllm.readinessProbe.httpGet.port | string | `"http"` | Name or number of the port to access on the container. |
| nm-vllm.readinessProbe.initialDelaySeconds | int | `5` | Number of seconds after the container has started before readiness probes are initiated. |
| nm-vllm.replicaCount | int | `1` | Number of replicas of the pod to run. |
| nm-vllm.resources | object | `{}` | Compute Resources required by the container. |
| nm-vllm.securityContext | object | `{}` | Defines the security options the container should be run with. |
| nm-vllm.service | object | -- | Configuration for the service resource. |
| nm-vllm.service.port | int | `80` | Port to expose on the service. |
| nm-vllm.service.type | string | `"LoadBalancer"` | The kind of service that should be used. |
| nm-vllm.tolerations | list | `[]` | Tolerations applied to the pod allowing the scheduler to schedule the pod to nodes with matching taints. |
| nm-vllm.volumeMounts | list | `[]` | Pod volumes to mount into the container's filesystem. |
| nm-vllm.volumes | list | `[]` | Volumes to make available to the pod. |
