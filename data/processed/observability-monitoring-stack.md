# Understanding the monitoring stack

The monitoring stack uses the following components:

- Prometheus collects and analyzes metrics from OpenShift Container Platform components and from workloads, if configured to do so.
- Alertmanager is a component of Prometheus that handles routing, grouping, and silencing of alerts.
- Thanos handles long term storage of metrics.

.OpenShift Container Platform monitoring architecture
image::monitoring-architecture.png[OpenShift Container Platform monitoring architecture]

> **NOTE:** For single-node OpenShift clusters, disable Alertmanager and Thanos because the clusters sends all metrics to the hub cluster for analysis and retention.