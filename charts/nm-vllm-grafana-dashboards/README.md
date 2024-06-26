# NM vLLM Graphana Dashboards

A collection of [Grafana](https://grafana.com/) dashboards for monitoring [NM
vLLM](https://github.com/neuralmagic/nm-vllm) deployments.

## Usage Options

The dashboards included in this respository in the [dashboards](/dashboards)
directory can be utilized in two ways:

1. Import dashboards into an exisiting Grafana instance directly by importing
   `dashboards/*.json` into the target Grafana instance.
   a. See [Import
   dashboards](https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/import-dashboards/)
   for detailed instructions on importing dashboards into an existing Grafana
   instance.
2. Use this chart to deploy the dashboard to Kubernetes as ConfigMap resources
   that can be detected by the Grafana dashboard sidecar that is part of the
   official [Grafana Helm
   chart](https://github.com/grafana/helm-charts/tree/main/charts/grafana).

The directions that follow cover how to deploy this Helm chart for use with a
Grafana instance managed by Helm.

## Requirements

Using this Helm chart with an existing Grafana Helm chart deployment depends on
the Grafana instance having the dashboards sidecar enabled and configured to
auto-detect labelled dashboard `ConfigMap` resources that are added to the
cluster.

For more information on enabling Grafana's dashboards sidecar, please refer to
Grafana's [sidecar for dashboards
documentation](https://github.com/grafana/helm-charts/blob/main/charts/grafana/README.md#sidecar-for-dashboards)
for more details.

Once the Grafana sidecar for dashboards is enabled, it's also important to make
sure that the `label` and `labelValue` values for this chart are configured to
match the respective `sidecar.dashboards.label` and
`sidecar.dashboards.labelValue` values that your Grafana chart is configured
with.

By default, this chart replicates the `label` and `labelValue` values used by
the Grafana chart, so by default, no additional configuration should be
required.

## Installation

[Helm](https://helm.sh) must be installed to use the charts.
Please refer to Helm's [documentation](https://helm.sh/docs/) to get started.

Once Helm is set up properly, add the Neural Magic Helm repository as follows:

```console
helm repo add neuralmagic https://helm.neuralmagic.com
```

You can then run `helm search repo neuralmagic` to see all available charts.

To install this chart, after setting up the Neural Magic Helm repository, run
the following install command:

```bash
helm install nm-vllm-grafana-charts nm-vllm-grafana-charts
```

## Customization

The following options are supported. See
[values.yaml](/charts/nm-vllm-grafana-dashboards/values.yaml) for more detailed
documentation and examples.

### Values

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| fullnameOverride | string | `""` | Provide a name to substitute for the full names of resources. |
| grafanaDashboardsLabelOverride | string | `nil` | Label used by Grafana's dashboards sidecar to identify config maps with dashboards that should be added to Grafana. Should match the value of the `sidecar.dashboards.label` configuration in the Grafana chart. |
| grafanaDashboardsLabelValueOverride | string | `nil` | Label value used by Grafana's dashboards sidecar to identify config maps with dashboards that should be added to Grafana. Should match the value of the `sidecar.dashboards.labelValue` configuration in the Grafana chart. |
| nameOverride | string | `""` | Provide a name to substitute for the name of the chart. |
