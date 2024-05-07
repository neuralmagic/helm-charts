# nm-vllm

## Usage

[Helm](https://helm.sh) must be installed to use the charts.
Please refer to Helm's [documentation](https://helm.sh/docs/) to get started.

Once Helm is set up properly, add the repository as follows:

```console
helm repo add neuralmagic https://helm.neuralmagic.com
```

You can then run `helm search repo neuralmagic` to see the charts.

The following options are supported. See [values.yaml](/charts/nm-vllm-production-monitoring/values.yaml) for more detailed documentation and examples:

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| datasourceHttpMethod | string | `"POST"` | The HTTP method to use for the Grafana datasource |
| datasourceUid | string | `"prometheus"` | The uid to use for the Grafana datasource |
| datasourceUrl | string | `"http://nm-vllm-prometheus-server/"` | The URL to use for the Grafana datasource |
| grafana | object | -- | Configuration for the Grafana deployment |
| grafana.sidecar.dashboards.enabled | bool | `true` | Enable the Grafana sidecar for dashboards so nm-vllm dashboards can be detected and loaded. If disabled, dashboards must be loaded manually. |
| grafana.sidecar.datasources.enabled | bool | `true` | Enable the Grafana sidecar for datasources so the prometheus instance can be configured and used as a Grafana datasource. If disabled, the prometheus datasource must be configured manually. |
| grafanaDatasourcesLabel | string | `"grafana_datasource"` | Label used by Grafana's sidecar for datasources to identify config maps with datasources that should be added to Grafana. Should match the value of the `sidecar.datasources.label` configuration in the Grafana chart. |
| grafanaDatasourcesLabelValue | string | `""` | Label value used by Grafana's sidecar for datasources to identify config maps with datasources that should be added to Grafana. Should match the value of the `sidecar.datasources.labelValue` configuration in the Grafana chart. |
| nm-vllm | object | -- | Configuration for the nm-vllm server deployment and service. |
| nm-vllm.podAnnotations."prometheus.io/scrape" | string | `"true"` | Enables prometheus to find pod to scrape |