{{/*
Expand the name of the chart.
*/}}
{{- define "nm-vllm-production-monitoring.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "nm-vllm-production-monitoring.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "nm-vllm-production-monitoring.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "nm-vllm-production-monitoring.labels" -}}
helm.sh/chart: {{ include "nm-vllm-production-monitoring.chart" . }}
{{ include "nm-vllm-production-monitoring.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "nm-vllm-production-monitoring.selectorLabels" -}}
app.kubernetes.io/name: {{ include "nm-vllm-production-monitoring.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Get the label used by grafana to identify datasource config maps
*/}}
{{- define "nm-vllm-production-monitoring.grafanaDatasourcesLabel" -}}
{{- if .Values.grafanaDatasourcesLabelOverride -}}
{{- .Values.grafanaDatasourcesLabelOverride -}}
{{- else if (((.Values.grafana).sidecar).datasources).label }}
{{- .Values.grafana.sidecar.datasources.label -}}
{{- else -}}
grafana_datasource
{{- end -}}
{{- end }}

{{/*
Get the label value used by grafana to identify datasource config maps
*/}}
{{- define "nm-vllm-production-monitoring.grafanaDatasourcesLabelValue" -}}
{{- if .Values.grafanaDatasourcesLabelValueOverride -}}
{{- .Values.grafanaDatasourcesLabelValueOverride -}}
{{- else if (((.Values.grafana).sidecar).datasources).labelValue }}
{{- .Values.grafana.sidecar.datasources.labelValue -}}
{{- else -}}
{{- /* intentionally blank because grafana default is "" */ -}}
{{- end -}}
{{- end }}

{{/*
Template for calculating the prometheus server name. Taken from prometheus chart:
https://github.com/prometheus-community/helm-charts/blob/26ff0a752b8f1864e1a6bd2d7e68981e0784cb77/charts/prometheus/templates/_helpers.tpl#L87-L98
*/}}
{{- define "nm-vllm-production-monitoring._prometheusServerName" -}}
{{- if ((.Values.prometheus).server).fullnameOverride -}}
{{- .Values.prometheus.server.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default "prometheus" (.Values.prometheus).nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- printf "%s-%s" .Release.Name ((.Values.prometheus).server).name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s-%s" .Release.Name $name ((.Values.prometheus).server).name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Get the URL that the grafana datasource should use to reach prometheus
*/}}
{{- define "nm-vllm-production-monitoring.grafanaDatasourceUrl" -}}
{{- if (.Values.datasource).url -}}
{{- .Values.datasource.url -}}
{{- else if .Values.prometheus }}
{{- printf "http://%s/" (include "nm-vllm-production-monitoring._prometheusServerName" $) -}}
{{- else -}}
{{- /* Default imagines they've installed the prometheus chart independently */ -}}
http://prometheus-server/
{{- end -}}
{{- end }}
