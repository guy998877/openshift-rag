# Configuring descheduler profiles

To manage cluster pod eviction behavior, select which descheduler profiles to enable.

.Prerequisites

- You are logged in to OpenShift Container Platform as a user with the `cluster-admin` role.

.Procedure

1. Edit the `KubeDescheduler` object:
```bash
$ oc edit kubedeschedulers.operator.openshift.io cluster -n openshift-kube-descheduler-operator
```

1. Specify one or more profiles in the `spec.profiles` section.
```yaml
apiVersion: operator.openshift.io/v1
kind: KubeDescheduler
metadata:
  name: cluster
  namespace: openshift-kube-descheduler-operator
spec:
  deschedulingIntervalSeconds: 3600
  logLevel: Normal
  managementState: Managed
  operatorLogLevel: Normal
  mode: Predictive
  profileCustomizations:
    namespaces:
      excluded:
      - my-namespace
    podLifetime: 48h
    thresholdPriorityClassName: my-priority-class-name
  evictionLimits:
    total: 20
  profiles:
  - AffinityAndTaints
  - TopologyAndDuplicates
  - LifecycleAndUtilization
  - EvictPodsWithLocalStorage
  - EvictPodsWithPVC
```
where:

`spec.mode`:: Specifies the eviction mode. By default, the descheduler does not evict pods. To evict pods, set `mode` to `Automatic`.
`spec.profileCustomizations.namespaces`:: Specifies a list of user-created namespaces to include or exclude from descheduler operations. Use `excluded` to set a list of namespaces to exclude or use `included` to set a list of namespaces to include. Note that protected namespaces (`openshift-*`, `kube-system`, `hypershift`) are excluded by default. This value is optional.
`spec.profileCustomizations.podLifetime`:: Specifies a custom pod lifetime value for the `LifecycleAndUtilization` profile. Valid units are `s`, `m`, or `h`. The default pod lifetime is 24 hours. This value is optional.
`spec.profileCustomizations.thresholdPriorityClassName`:: Specifies a priority threshold to consider pods for eviction only if their priority is lower than the specified level. Use the `thresholdPriority` field to set a numerical priority threshold (for example, `10000`) or use the `thresholdPriorityClassName` field to specify a certain priority class name (for example, `my-priority-class-name`). If you specify a priority class name, it must already exist or the descheduler will throw an error. Do not set both `thresholdPriority` and `thresholdPriorityClassName`. This value is optional.
`spec.evictionLimits.total`:: Specifies the maximum number of pods to evict during each descheduler run. This value is optional.
`spec.profiles`:: Specifies one or more profiles to enable. Available profiles: `AffinityAndTaints`, `TopologyAndDuplicates`, `LifecycleAndUtilization`, `SoftTopologyAndDuplicates`, `EvictPodsWithLocalStorage`, `EvictPodsWithPVC`, `CompactAndScale`, and `LongLifecycle`. You can enable multiple profiles, but ensure that you do not enable profiles that conflict with each other. The order of the list of profiles is not important.

1. Save the file to apply the changes.