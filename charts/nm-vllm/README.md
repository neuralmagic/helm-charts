# nm-vllm

## Usage

[Helm](https://helm.sh) must be installed to use the charts.
Please refer to Helm's [documentation](https://helm.sh/docs/) to get started.

Once Helm is set up properly, add the repository as follows:

```console
helm repo add neuralmagic https://helm.neuralmagic.com
```

You can then run `helm search repo neuralmagic` to see the charts.

## Customization

The following options are supported. See [values.yaml](/charts/nm-vllm/values.yaml) for more detailed documentation and examples:

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Provide affinity rules for pod scheduling. |
| apiServer | object | -- | Configuration for the nm-vllm API server |
| apiServer.extraArgs | list | `[]` | Extra arguments to pass to the API server command |
| fullnameOverride | string | `""` | Provide a name to substitute for the full names of resources. |
| image | object | -- | Configuration for the application image. |
| image.pullPolicy | string | `"IfNotPresent"` | The pull policy for the image. |
| image.repository | string | `"ghcr.io/neuralmagic/nm-vllm-openai"` | The image repository for the application. |
| image.tag | string | `"v0.1.0"` | The tag of the image to use. |
| modelName | string | `"mistralai/Mistral-7B-v0.1"` | The name of the model to serve. |
| nameOverride | string | `""` | Provide a name to substitute for the name of the chart. |
| nodeSelector | object | `{}` | Node labels controlling where the pod will be scheduled. |
| podAnnotations | object | `{}` | Annotations to add to the pod. |
| podLabels | object | `{}` | Labels to add to the pod. |
| podSecurityContext | object | `{}` | Defines the security options the pod should be run with. |
| readinessProbe | object | -- | Readiness probe configuration for the container. |
| readinessProbe.httpGet | object | `{"path":"/health","port":"http"}` | Specifies the http request to perform. |
| readinessProbe.httpGet.path | string | `"/health"` | Path to access on the HTTP server. |
| readinessProbe.httpGet.port | string | `"http"` | Name or number of the port to access on the container. |
| readinessProbe.initialDelaySeconds | int | `5` | Number of seconds after the container has started before readiness probes are initiated. |
| replicaCount | int | `1` | Number of replicas of the pod to run. |
| resources | object | `{}` | Compute Resources required by the container. |
| securityContext | object | `{}` | Defines the security options the container should be run with. |
| service | object | -- | Configuration for the service resource. |
| service.annotations | object | `{}` | Annotations to add to the service. |
| service.port | int | `80` | Port to expose on the service. |
| service.type | string | `"LoadBalancer"` | The kind of service that should be used. |
| tolerations | list | `[]` | Tolerations applied to the pod allowing the scheduler to schedule the pod to nodes with matching taints. |
| volumeMounts | list | `[]` | Pod volumes to mount into the container's filesystem. |
| volumes | list | `[]` | Volumes to make available to the pod. |

## Examples

- [Basic](./examples/basic)
  - Demonstrates configuring `apiServer.extraArgs`, `modelName`,
  `nodeSelector`, and `resources`.
