# Installing the Secrets Store CSI driver

.Prerequisites
- Access to the OpenShift Container Platform web console.

- Administrator access to the cluster.

.Procedure

To install the Secrets Store CSI driver:

1. Install the Secrets Store CSI Driver Operator:
.. Log in to the web console.
.. Click *Ecosystem* -> *Software Catalog*.
.. Locate the Secrets Store CSI Driver Operator by typing "Secrets Store CSI" in the filter box.
.. Click the *Secrets Store CSI Driver Operator* button.
.. On the *Secrets Store CSI Driver Operator* page, click *Install*.
.. On the *Install Operator* page, ensure that:
- *All namespaces on the cluster (default)* is selected.

- *Installed Namespace* is set to *openshift-cluster-csi-drivers*.
.. Click *Install*.
After the installation finishes, the Secrets Store CSI Driver Operator is listed in the *Installed Operators* section of the web console.

1. Create the `ClusterCSIDriver` instance for the driver (`secrets-store.csi.k8s.io`):
.. Click *Administration* -> *CustomResourceDefinitions* -> *ClusterCSIDriver*.
.. On the *Instances* tab, click *Create ClusterCSIDriver*.
Use the following YAML file:
```yaml
apiVersion: operator.openshift.io/v1
kind: ClusterCSIDriver
metadata:
    name: secrets-store.csi.k8s.io
spec:
  managementState: Managed
```
.. Click *Create*.