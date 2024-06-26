{{/*
Expand the name of the chart.
*/}}
{{- define "nm-vllm-grafana-dashboards.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "nm-vllm-grafana-dashboards.fullname" -}}
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
{{- define "nm-vllm-grafana-dashboards.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "nm-vllm-grafana-dashboards.labels" -}}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/name: {{ include "nm-vllm-grafana-dashboards.name" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
helm.sh/chart: {{ include "nm-vllm-grafana-dashboards.chart" . }}
{{- end }}

{{/*
Get the label used by grafana to identify dashboard config maps
*/}}
{{- define "nm-vllm-grafana-dashboards.grafanaDashboardsLabel" -}}
{{- if .Values.grafanaDashboardsLabelOverride -}}
{{- .Values.grafanaDashboardsLabelOverride -}}
{{- else if (((.Values.grafana).sidecar).dashboards).label }}
{{- .Values.grafana.sidecar.dashboards.label -}}
{{- else -}}
grafana_dashboard
{{- end -}}
{{- end }}

{{/*
Get the label value used by grafana to identify dashboard config maps
*/}}
{{- define "nm-vllm-grafana-dashboards.grafanaDashboardsLabelValue" -}}
{{- if .Values.grafanaDashboardsLabelValueOverride -}}
{{- .Values.grafanaDashboardsLabelValueOverride -}}
{{- else if (((.Values.grafana).sidecar).dashboards).labelValue }}
{{- .Values.grafana.sidecar.dashboards.labelValue -}}
{{- else -}}
{{- /* intentionally blank because grafana default is "" */ -}}
{{- end -}}
{{- end }}
