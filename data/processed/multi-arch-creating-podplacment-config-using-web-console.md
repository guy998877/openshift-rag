# Creating the ClusterPodPlacementConfig object by using the web console

To deploy the pod placement operand that enables architecture-aware workload scheduling, you can create the `ClusterPodPlacementConfig` object by using the OpenShift Container Platform web console.

.Prerequisites

- You have access to the cluster with `cluster-admin` privileges.
- You have access to the OpenShift Container Platform web console.
- You have installed the Multiarch Tuning Operator.

.Procedure

1. Log in to the OpenShift Container Platform web console.

1. Navigate to *Ecosystem* -> *Installed Operators*.

1. On the *Installed Operators* page, click *Multiarch Tuning Operator*. 

1. Click the *Cluster Pod Placement Config* tab.

1. Select either *Form view* or *YAML view*.

1. Configure the `ClusterPodPlacementConfig` object parameters.

1. Click *Create*.

1. Optional: If you want to edit the `ClusterPodPlacementConfig` object, perform the following actions:

.. Click the *Cluster Pod Placement Config* tab.
.. Select *Edit ClusterPodPlacementConfig* from the options menu.
.. Click *YAML* and edit the `ClusterPodPlacementConfig` object parameters.
.. Click *Save*.

.Verification

- On the *Cluster Pod Placement Config* page, check that the `ClusterPodPlacementConfig` object is in the `Ready` state.