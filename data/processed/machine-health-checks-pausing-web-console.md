// * updating/updating_a_cluster/updating-cluster-web-console.adoc

# Pausing a MachineHealthCheck resource by using the web console

During the update process, nodes in the cluster might become temporarily unavailable. In the case of worker nodes, the machine health check might identify such nodes as unhealthy and reboot them. To avoid rebooting such nodes, pause all the `MachineHealthCheck` resources before updating the cluster.

.Prerequisites

- You have access to the cluster with `cluster-admin` privileges.
- You have access to the OpenShift Container Platform web console.

.Procedure

1. Log in to the OpenShift Container Platform web console.
1. Navigate to *Compute* -> *MachineHealthChecks*.
1. To pause the machine health checks, add the `cluster.x-k8s.io/paused=""` annotation to each `MachineHealthCheck` resource. For example, to add the annotation to the `machine-api-termination-handler` resource, complete the following steps:
.. Click the Options menu image:kebab.png[title="Options menu"] next to the `machine-api-termination-handler` and click *Edit annotations*.
.. In the *Edit annotations* dialog, click *Add more*.
.. In the *Key* and *Value* fields, add `cluster.x-k8s.io/paused` and `""` values, respectively, and click *Save*.