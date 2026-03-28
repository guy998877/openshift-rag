# Uninstalling the {FeatureName} CSI Driver Operator

All EFS PVs are inaccessible after uninstalling the [AWS EFS CSI Driver Operator](https://github.com/openshift/aws-efs-csi-driver-operator) (a Red Hat operator).

.Prerequisites
- Access to the OpenShift Container Platform web console.

.Procedure
To uninstall the {FeatureName} CSI Driver Operator from the web console:

1. Log in to the web console.

1. Stop all applications that use {FeatureName} PVs.

1. Delete all {FeatureName} PVs:

.. Click *Storage* -> *PersistentVolumeClaims*.

.. Select each PVC that is in use by the {FeatureName} CSI Driver Operator, click the drop-down menu on the far right of the PVC, and then click *Delete PersistentVolumeClaims*.

1. Uninstall the https://github.com/openshift/aws-efs-csi-driver[{FeatureName} CSI driver]:
> **NOTE:** Before you can uninstall the Operator, you must remove the CSI driver first.

.. Click *Administration* -> *CustomResourceDefinitions* -> *ClusterCSIDriver*.

.. On the *Instances* tab, for *{provisioner}*, on the far left side, click the drop-down menu, and then click *Delete ClusterCSIDriver*.

.. When prompted, click *Delete*.

1. Uninstall the {FeatureName} CSI Operator:

.. Click *Ecosystem* -> *Installed Operators*.

.. On the *Installed Operators* page, scroll or type {FeatureName} CSI into the *Search by name* box to find the Operator, and then click it.

.. On the upper, right of the *Installed Operators > Operator details* page, click *Actions* -> *Uninstall Operator*.

.. When prompted on the *Uninstall Operator* window, click the *Uninstall* button to remove the Operator from the namespace. Any applications deployed by the Operator on the cluster need to be cleaned up manually.
After uninstalling, the {FeatureName} CSI Driver Operator is no longer listed in the *Installed Operators* section of the web console.

> **NOTE:** Before you can destroy a cluster (`openshift-install destroy cluster`), you must delete the EFS volume in AWS. An OpenShift Container Platform cluster cannot be destroyed when there is an EFS volume that uses the cluster's VPC. Amazon does not allow deletion of such a VPC.