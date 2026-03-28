# Installing the {FeatureName} CSI Driver

After installing the {FeatureName} Container Storage Interface (CSI) Driver Operator, install the {FeatureName} CSI driver.

.Prerequisites
- Access to the OpenShift Container Platform web console.
- {FeatureName} CSI Driver Operator installed.

.Procedure

1. Click *Administration* -> *CustomResourceDefinitions* -> *ClusterCSIDriver*.

1. On the *Instances* tab, click *Create ClusterCSIDriver*.

1. Use the following YAML file:
```yaml
apiVersion: operator.openshift.io/v1
kind: ClusterCSIDriver
metadata:
    name: smb.csi.k8s.io
spec:
  managementState: Managed
```

1. Click *Create*.

1. Wait for the following Conditions to change to a "True" status:

- `SambaDriverControllerServiceControllerAvailable`

- `SambaDriverNodeServiceControllerAvailable`