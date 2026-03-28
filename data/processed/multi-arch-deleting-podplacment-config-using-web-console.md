# Deleting the ClusterPodPlacementConfig object by using the web console

You can create only one instance of the `ClusterPodPlacementConfig` object. If you want to re-create this object, you must first delete the existing instance.

You can delete this object by using the OpenShift Container Platform web console.

.Prerequisites

- You have access to the cluster with `cluster-admin` privileges.
- You have access to the OpenShift Container Platform web console.
- You have created the `ClusterPodPlacementConfig` object.

.Procedure

1. Log in to the OpenShift Container Platform web console.

1. Navigate to *Ecosystem* -> *Installed Operators*.

1. On the *Installed Operators* page, click *Multiarch Tuning Operator*. 

1. Click the *Cluster Pod Placement Config* tab.

1. Select *Delete ClusterPodPlacementConfig* from the options menu.

1. Click *Delete*.

.Verification

- On the *Cluster Pod Placement Config* page, check that the `ClusterPodPlacementConfig` object has been deleted.