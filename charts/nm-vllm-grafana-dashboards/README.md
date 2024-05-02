# nm-vllm

## Usage

[Helm](https://helm.sh) must be installed to use the charts.
Please refer to Helm's [documentation](https://helm.sh/docs/) to get started.

Once Helm is set up properly, add the repository as follows:

```console
helm repo add neuralmagic https://helm.neuralmagic.com
```

You can then run `helm search repo neuralmagic` to see the charts.

If you manage your grafana instance with helm you can use this chart to create configmaps that would be detectable by the grafana dashboards sidecar
Refer to grafana's [documentation](https://github.com/grafana/helm-charts/blob/main/charts/grafana/README.md#sidecar-for-dashboards) for more details

## Customization
The following options are supported. See [values.yaml](/charts/nm-vllm-grafana-dashboards/values.yaml) for more detailed documentation and examples:

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| label | string | `"grafana_dashboard"` | Grafana sidecar dashboard label |
| labelValue | string | `"1"` | Grafana sidecar dashboard label value |
