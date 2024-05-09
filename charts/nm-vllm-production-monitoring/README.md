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
| datasource | object | -- | Configuration for the datasource connecting prometheus and grafana. |
| datasource.enabled | bool | `true` | Toggles whether or not a prometheus datasource will be configured in grafana. |
| datasource.httpMethod | string | `"POST"` | The HTTP method to use for prometheus datasource configured in grafana. |
| datasource.isDefault | bool | `true` | Toggles whether or not the prometheus datasource configured in grafana should be the default grafana datasource. |
| datasource.name | string | `"Prometheus"` | The name to use for the prometheus datasource configured in grafana. |
| datasource.timeInterval | string | `"15s"` | The time interval with which grafana should scrape the prometheus datasource. |
| datasource.uid | string | `"prometheus"` | The uid to use for the prometheus datasource configured in grafana. |
| datasource.url | string | `nil` | The URL to use for the prometheus datasource configured in grafana. |
| grafana | object | -- | Configuration for the grafana sub-chart |
| grafana.enabled | bool | `true` | Toggle whether or not the grafana sub-chart is included |
| grafana.sidecar | object | -- | Allows for deployment of containers alongside the grafana container for purposes such as importing dashboards and datasources. |
| grafana.sidecar.dashboards | object | -- | Enables the automatic import and management of grafana dashboards from ConfigMaps or secrets. |
| grafana.sidecar.dashboards.enabled | bool | `true` | Enable the grafana sidecar for dashboards so nm-vllm dashboards can be detected and loaded. If disabled, dashboards must be loaded manually. |
| grafana.sidecar.datasources | object | -- | Enables the dynamic configuration of datasources from ConfigMaps or secrets. |
| grafana.sidecar.datasources.enabled | bool | `true` | Enable the grafana sidecar for datasources so the prometheus instance can be configured and used as a grafana datasource. If disabled, the prometheus datasource must be configured manually. |
| grafanaDatasourcesLabelOverride | string | `nil` | Label used by grafana's sidecar for datasources to identify config maps with datasources that should be added to grafana. Should match the value of the `sidecar.datasources.label` configuration in the grafana chart. |
| grafanaDatasourcesLabelValueOverride | string | `nil` | Label value used by grafana's sidecar for datasources to identify config maps with datasources that should be added to grafana. Should match the value of the `sidecar.datasources.labelValue` configuration in the grafana chart. |
| nm-vllm | object | -- | Configuration for the nm-vllm server deployment and service. |
| nm-vllm-grafana-dashboards | object | `{"enabled":true}` | Configuration for the nm-vllm-grafana-dashboards chart |
| nm-vllm-grafana-dashboards.enabled | bool | `true` | Toggle whether or not the nm-vllm-grafana-dashboards sub-chart is included |
| nm-vllm.podAnnotations."prometheus.io/scrape" | string | `"true"` | Enables prometheus to find pod to scrape |
| prometheus | object | -- | Configuration for the prometheus sub-chart |
| prometheus.enabled | bool | `true` | Toggle whether or not the prometheus sub-chart is included |