# Installing the descheduler

The descheduler is not available by default. To enable the descheduler, you must install the Kube Descheduler Operator from the software catalog and enable one or more descheduler profiles.

By default, the descheduler runs in predictive mode, which means that it only simulates pod evictions. You must change the mode to automatic for the descheduler to perform the pod evictions.

> **IMPORTANT:** If you have enabled hosted control planes in your cluster, set a custom priority threshold to lower the chance that pods in the hosted control plane namespaces are evicted. Set the priority threshold class name to `hypershift-control-plane`, because it has the lowest priority value (`100000000`) of the hosted control plane priority classes.

.Prerequisites

- You are logged in to OpenShift Container Platform as a user with the `cluster-admin` role.
- Access to the OpenShift Container Platform web console.

.Procedure

1. Log in to the OpenShift Container Platform web console.
1. Create the required namespace for the Kube Descheduler Operator.
.. Navigate to *Administration* -> *Namespaces* and click *Create Namespace*.
.. Enter `openshift-kube-descheduler-operator` in the *Name* field, enter `openshift.io/cluster-monitoring=true` in the *Labels* field to enable descheduler metrics, and click *Create*.
1. Install the Kube Descheduler Operator.
.. Navigate to *Ecosystem* -> *Software Catalog*.
.. Type *Kube Descheduler Operator* into the filter box.
.. Select the *Kube Descheduler Operator* and click *Install*.
.. On the *Install Operator* page, select *A specific namespace on the cluster*. Select *openshift-kube-descheduler-operator* from the drop-down menu.
.. Adjust the values for the *Update Channel* and *Approval Strategy* to the desired values.
.. Click *Install*.
1. Create a descheduler instance.
.. From the *Ecosystem* -> *Installed Operators* page, click the *Kube Descheduler Operator*.
.. Select the *Kube Descheduler* tab and click *Create KubeDescheduler*.
.. Edit the settings as necessary.
... To evict pods instead of simulating the evictions, change the *Mode* field to *Automatic*.