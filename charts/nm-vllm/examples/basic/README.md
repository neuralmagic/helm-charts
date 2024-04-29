# Basic

This example demonstrates the values required to use the `nm-vllm` chart to
deploy the `TheBloke/Mistral-7B-Instruct-v0.2-GPTQ` model.

Because the target model is quantized using GPTQ, the values also specify extra
arguments for the vLLM OpenAI API server to inform the server to use `float16`
for the data type of the model weights and activations.

Finally, the values configure the resource limits for the API server deployment
such that the pod is limited to:

- `4 cpus`
- `16Gi memory`
- `1 nvidia.com/gpu`

## Values

The `values.yaml` is included in full below, but the `values.yaml` file is also
available [here](./values.yaml).

```yaml
apiServer:
  extraArgs:
    - --dtype
    - float16

modelName:
  TheBloke/Mistral-7B-Instruct-v0.2-GPTQ

resources:
  limits:
    cpu: 4
    memory: 16Gi
    nvidia.com/gpu: 1
```

## Example invocations

### Using Neural Magic Helm Repository

```bash
helm repo add neuralmagic https://helm.neuralmagic.com
helm install nm-vllm nm-vllm -f https://raw.githubusercontent.com/neuralmagic/helm-charts/main/charts/nm-vllm/examples/basic/values.yaml
```

### Using `helm-charts` git repository

```bash
git clone https://github.com/neuralmagic/helm-charts.git
cd helm-charts
helm install nm-vllm charts/nm-vllm -f charts/nm-vllm/examples/basic/values.yaml
```
