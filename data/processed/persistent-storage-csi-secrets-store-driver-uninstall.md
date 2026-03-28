# Uninstalling the Secrets Store CSI Driver Operator

.Prerequisites
- Access to the OpenShift Container Platform web console.

- Administrator access to the cluster.

.Procedure

To uninstall the Secrets Store CSI Driver Operator:

1. Stop all application pods that use the `secrets-store.csi.k8s.io` provider.
1. Remove any third-party provider plug-in for your chosen secret store.
1. Remove the Container Storage Interface (CSI) driver and associated manifests:
.. Click *Administration* → *CustomResourceDefinitions* → *ClusterCSIDriver*.
.. On the *Instances* tab, for *secrets-store.csi.k8s.io*, on the far left side, click the drop-down menu, and then click *Delete ClusterCSIDriver*.
.. When prompted, click *Delete*.
1. Verify that the CSI driver pods are no longer running.
1. Uninstall the Secrets Store CSI Driver Operator:
> **NOTE:** Before you can uninstall the Operator, you must remove the CSI driver first.
.. Click *Ecosystem* -> *Installed Operators*.
.. On the *Installed Operators* page, scroll or type "Secrets Store CSI" into the *Search by name* box to find the Operator, and then click it.
.. On the upper, right of the *Installed Operators* > *Operator details* page, click *Actions* → *Uninstall Operator*.
.. When prompted on the *Uninstall Operator* window, click the *Uninstall* button to remove the Operator from the namespace. Any applications deployed by the Operator on the cluster need to be cleaned up manually.
After uninstalling, the Secrets Store CSI Driver Operator is no longer listed in the *Installed Operators* section of the web console.