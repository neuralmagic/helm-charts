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
| datasourceHttpMethod | string | `"POST"` | The HTTP method to use for the grafana datasource |
| datasourceUid | string | `"prometheus"` | The uid to use for the grafana datasource |
| datasourceUrl | string | `"http://nm-vllm-prometheus-server/"` | The URL to use for the grafana datasource |
| grafana | object | -- | Configuration for the grafana deployment |
| grafana.sidecar.dashboards.enabled | bool | `true` | Enable the grafana sidecar for dashboards so nm-vllm dashboards can be detected and loaded. If disabled, dashboards must be loaded manually. |
| grafana.sidecar.datasources.enabled | bool | `true` | Enable the grafana sidecar for datasources so the prometheus instance can be configured and used as a grafana datasource. If disabled, the prometheus datasource must be configured manually. |
| grafana.sidecar.datasources.label | string | `"grafana_datasource"` | Grafana sidecar datasource label |
| grafana.sidecar.datasources.labelValue | string | `"1"` | Grafana sidecar datasource label |
| nm-vllm | object | -- | Configuration for the nm-vllm server deployment and service. |
| nm-vllm.podAnnotations."prometheus.io/scrape" | string | `"true"` | Enables prometheus to find pod to scrape |