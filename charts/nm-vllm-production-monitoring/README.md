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
| datasourceHttpMethod | string | `"POST"` | Grafana datasource http method |
| datasourceUid | string | `"prometheus"` | Grafana datasource uid |
| datasourceUrl | string | `"http://nm-vllm-prometheus-server/"` | Grafana datasource url |
| grafana | object | -- | Grafana sidecar values |
| grafana.sidecar.dashboards.enabled | bool | `true` | True is required to enable sidecar dashboards |
| grafana.sidecar.dashboards.label | string | `"grafana_dashboard"` | Grafana sidecar dashboard label |
| grafana.sidecar.dashboards.labelValue | string | `"1"` | Grafana sidecar dashboard label value |
| grafana.sidecar.datasources.enabled | bool | `true` | True is required to enable sidecar datasources |
| grafana.sidecar.datasources.label | string | `"grafana_datasource"` | Grafana sidecar datasource label |
| grafana.sidecar.datasources.labelValue | string | `"1"` | Grafana sidecar datasource label |
| nm-vllm | object | -- | Configuration for the nm-vllm server deployment and service. |
| nm-vllm.podAnnotations."prometheus.io/scrape" | string | `"true"` | Enables prometheus to find pod to scrape |