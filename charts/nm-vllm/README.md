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
The following options are supported. See [values.yaml](/charts/nmvllm/values.yaml) for more detailed documentation and examples:

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | Provide affinity rules for the pod scheduling. |
| fullnameOverride | string | `""` | Provide a name to substitute for the full names of resources. |
| image.pullPolicy | string | `"IfNotPresent"` | The pull policy for the Docker image. |
| image.repository | string | `"ghcr.io/neuralmagic/nm-vllm-openai"` | The Docker image repository for the application. |
| image.tag | string | `"v0.1.0"` | The tag of the Docker image to use. |
| modelName | string | `"mistralai/Mistral-7B-v0.1"` |  |
| nameOverride | string | `""` | Provide a name to substitute for the name of the chart. |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` |  |
| podLabels | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| readinessProbe.httpGet.path | string | `"/health"` |  |
| readinessProbe.httpGet.port | string | `"http"` |  |
| readinessProbe.initialDelaySeconds | int | `5` |  |
| readinessProbe.periodSeconds | int | `5` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` |  |
| securityContext | object | `{}` |  |
| service.port | int | `80` |  |
| service.type | string | `"LoadBalancer"` |  |
| tolerations | list | `[]` |  |
| volumeMounts | list | `[]` |  |
| volumes | list | `[]` |  |
