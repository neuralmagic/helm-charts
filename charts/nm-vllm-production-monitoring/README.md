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
| nm-vllm | object | -- | Configuration for the nm-vllm server deployment and service. |
