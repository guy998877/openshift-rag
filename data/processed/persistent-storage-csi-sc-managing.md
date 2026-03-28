# Managing the default storage class using the web console

.Prerequisites
- Access to the OpenShift Container Platform web console.

- Access to the cluster with cluster-admin privileges.

.Procedure

To manage the default storage class using the web console:

1. Log in to the web console.

1. Click *Administration* > *CustomResourceDefinitions*.

1. On the *CustomResourceDefinitions* page, type `clustercsidriver` to find the `ClusterCSIDriver` object.

1. Click *ClusterCSIDriver*, and then click the *Instances* tab.

1. Click the name of the desired instance, and then click the *YAML* tab.

1. Add the `spec.storageClassState` field with a value of `Managed`, `Unmanaged`, or `Removed`.
.Example
```yaml
...
spec:
  driverConfig:
    driverType: ''
  logLevel: Normal
  managementState: Managed
  observedConfig: null
  operatorLogLevel: Normal
  storageClassState: Unmanaged <1>
...
```
<1> `spec.storageClassState` field set to "Unmanaged"

1. Click *Save*.