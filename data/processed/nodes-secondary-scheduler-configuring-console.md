# Deploying a secondary scheduler

After you have installed the Secondary Scheduler Operator, you can deploy a secondary scheduler to apply custom placement logic for specific pods.

.Prerequisites

- You are logged in to OpenShift Container Platform as a user with the `cluster-admin` role.
- You have access to the OpenShift Container Platform web console.
- The Secondary Scheduler Operator for Red Hat OpenShift is installed.

.Procedure

1. Log in to the OpenShift Container Platform web console.
1. Create config map to hold the configuration for the secondary scheduler.
.. Navigate to *Workloads* -> *ConfigMaps*.
.. Click *Create ConfigMap*.
.. In the YAML editor, enter the config map definition that contains the necessary `KubeSchedulerConfiguration` configuration. For example:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: "secondary-scheduler-config"
  namespace: "openshift-secondary-scheduler-operator"
data:
  "config.yaml": |
    apiVersion: kubescheduler.config.k8s.io/v1
    kind: KubeSchedulerConfiguration
    leaderElection:
      leaderElect: false
    profiles:
      - schedulerName: secondary-scheduler
        plugins:
          score:
            disabled:
              - name: NodeResourcesBalancedAllocation
              - name: NodeResourcesLeastAllocated
```
where:

`metadata.name`:: Specifies the name of the config map. This is used in the *Scheduler Config* field when creating the `SecondaryScheduler` CR.
`metadata.namespace`:: Specifies the namespace to create the config map in. The namespace must be `openshift-secondary-scheduler-operator`.
`data."config.yaml".kind`:: Specifies the `KubeSchedulerConfiguration` resource for the secondary scheduler. For more information, see [`KubeSchedulerConfiguration`](https://kubernetes.io/docs/reference/config-api/kube-scheduler-config.v1/#kubescheduler-config-k8s-io-v1-KubeSchedulerConfiguration) in the Kubernetes API documentation.
`data."config.yaml".profiles.schedulerName`:: Specifies the name of the secondary scheduler. Pods that set their `spec.schedulerName` field to this value are scheduled with this secondary scheduler.
`data."config.yaml".profiles.plugins`:: Specifies the plugins to enable or disable for the secondary scheduler. For a list default scheduling plugins, see [Scheduling plugins](https://kubernetes.io/docs/reference/scheduling/config/#scheduling-plugins) in the Kubernetes documentation.

.. Click *Create*.

1. Create the `SecondaryScheduler` CR:
.. Navigate to *Ecosystem* -> *Installed Operators*.
.. Select *Secondary Scheduler Operator for Red Hat OpenShift*.
.. Select the *Secondary Scheduler* tab and click *Create SecondaryScheduler*.
.. The *Name* field defaults to `cluster`; do not change this name.
.. The *Scheduler Config* field defaults to `secondary-scheduler-config`. Ensure that this value matches the name of the config map created earlier in this procedure.
.. In the *Scheduler Image* field, enter the image name for your custom scheduler.
> **IMPORTANT:** Red Hat does not directly support the functionality of your custom secondary scheduler.

.. Click *Create*.