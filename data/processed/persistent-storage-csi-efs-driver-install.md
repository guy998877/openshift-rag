# Installing the {FeatureName} CSI Driver

After installing the [{FeatureName} CSI Driver Operator](https://github.com/openshift/aws-efs-csi-driver-operator) (a Red Hat operator), you install the [{FeatureName} CSI driver](https://github.com/openshift/aws-efs-csi-driver).

.Prerequisites
- Access to the OpenShift Container Platform web console.

.Procedure

1. Click *Administration* -> *CustomResourceDefinitions* -> *ClusterCSIDriver*.

1. On the *Instances* tab, click *Create ClusterCSIDriver*.

1. Use the following YAML file:
```yaml
apiVersion: operator.openshift.io/v1
kind: ClusterCSIDriver
metadata:
    name: efs.csi.aws.com
spec:
  managementState: Managed
```

1. Click *Create*.

1. Wait for the following Conditions to change to a "True" status:

- AWSEFSDriverNodeServiceControllerAvailable

- AWSEFSDriverControllerServiceControllerAvailable