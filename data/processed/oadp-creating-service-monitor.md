# Creating OADP service monitor

Create a `ServiceMonitor` resource to scrape Velero metrics from the OADP service endpoint. This helps you collect metrics for monitoring backup and restore operations in the OpenShift Container Platform monitoring stack.

OADP provides an `openshift-adp-velero-metrics-svc` service. The user workload monitoring service monitor must use the `openshift-adp-velero-metrics-svc` service.

.Procedure

1. Ensure that the `openshift-adp-velero-metrics-svc` service exists. It should contain `app.kubernetes.io/name=velero` label, which is used as selector for the `ServiceMonitor` object.
```bash
$ oc get svc -n openshift-adp -l app.kubernetes.io/name=velero
```
.Example output
```bash
NAME                               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
openshift-adp-velero-metrics-svc   ClusterIP   172.30.38.244   <none>        8085/TCP   1h
```

1. Create a `ServiceMonitor` YAML file that matches the existing service label, and save the file as `3_create_oadp_service_monitor.yaml`. The service monitor is created in the `openshift-adp` namespace which has the `openshift-adp-velero-metrics-svc` service.
```yaml
+
```
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  labels:
    app: oadp-service-monitor
  name: oadp-service-monitor
  namespace: openshift-adp
spec:
  endpoints:
  - interval: 30s
    path: /metrics
    targetPort: 8085
    scheme: http
  selector:
    matchLabels:
      app.kubernetes.io/name: "velero"

1. Apply the `3_create_oadp_service_monitor.yaml` file:
```bash
$ oc apply -f 3_create_oadp_service_monitor.yaml
```
.Example output
```bash
servicemonitor.monitoring.coreos.com/oadp-service-monitor created
```

.Verification

- Confirm that the new service monitor is in an *Up* state by using the *Administrator* perspective of the OpenShift Container Platform web console. Wait a few minutes for the service monitor to reach the *Up* state.
.. Navigate to the *Observe* -> *Targets* page.
.. Ensure the *Filter* is unselected or that the *User* source is selected and type `openshift-adp` in the `Text` search field.
.. Verify that the status for the *Status* for the service monitor is *Up*.
.OADP metrics targets

image::oadp-metrics-targets.png[OADP metrics targets]