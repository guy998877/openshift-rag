# Workload monitoring

By default, OpenShift Container Platform does not collect metrics for application workloads. You can configure a cluster to collect workload metrics.

.Prerequisites

- You have defined endpoints to gather workload metrics on the cluster.

.Procedure

1. Create a `ConfigMap` CR and save it as `monitoringConfigMap.yaml`, as in the following example:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-monitoring-config
  namespace: openshift-monitoring
data:
  config.yaml: |
    enableUserWorkload: true <1>
```
<1> Set to `true` to enable workload monitoring.

1. Apply the `ConfigMap` CR by running the following command:
```bash
$ oc apply -f monitoringConfigMap.yaml
```

1. Create a `ServiceMonitor` CR, and save it as `monitoringServiceMonitor.yaml`, as in the following example:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  labels:
    app: ui
  name: myapp
  namespace: myns
spec:
  endpoints: <1>
  - interval: 30s
    port: ui-http
    scheme: http
    path: /healthz <2>
  selector:
    matchLabels:
      app: ui
```
<1> Use endpoints to define workload metrics. 
<2> Prometheus scrapes the path `/metrics` by default. You can define a custom path here. 

1. Apply the `ServiceMonitor` CR by running the following command:
```bash
$ oc apply -f monitoringServiceMonitor.yaml
```

Prometheus scrapes the `/metrics` path by default. However, you can define a custom path. 
The vendor of the application must decide whether to expose the endpoint for scraping, with metrics that they deem relevant.

## Creating a workload alert

You can enable alerts for user workloads on a cluster.

.Procedure

1. Create a `ConfigMap` CR, and save it as `monitoringConfigMap.yaml`, as in the following example:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-monitoring-config
  namespace: openshift-monitoring
data:
  config.yaml: |
    enableUserWorkload: true <1>
# ...
```
<1> Set to `true` to enable workload monitoring.

1. Apply the `ConfigMap` CR by running the following command:
```bash
$ oc apply -f monitoringConfigMap.yaml
```

1. Create a YAML file for alerting rules, `monitoringAlertRule.yaml`, as in the following example:
```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: myapp-alert
  namespace: myns
spec:
  groups:
  - name: example
    rules:
    - alert: InternalErrorsAlert
      expr: flask_http_request_total{status="500"} > 0
# ...
```

1. Apply the alert rule by running the following command:
```bash
$ oc apply -f monitoringAlertRule.yaml
```