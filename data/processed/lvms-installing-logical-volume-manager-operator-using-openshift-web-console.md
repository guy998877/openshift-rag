# Installing LVM Storage by using the web console

You can install LVM Storage by using the OpenShift Container Platform web console.

> **NOTE:** The default namespace for the LVM Storage Operator is `openshift-lvm-storage`.

.Prerequisites

- You have access to the cluster.
- You have access to OpenShift Container Platform with `cluster-admin` and Operator installation permissions.

.Procedure

1. Log in to the OpenShift Container Platform web console.
1. Click *Ecosystem* -> *Software Catalog*.
1. Click *LVM Storage* on the software catalog page.
1. Set the following options on the *Operator Installation* page:
.. *Update Channel* as *stable-4.21*.
.. *Installation Mode* as *A specific namespace on the cluster*.
.. *Installed Namespace* as *Operator recommended namespace openshift-storage*.
   If the `openshift-lvm-storage` namespace does not exist, it is created during the operator installation.
.. *Update approval* as *Automatic* or *Manual*.
> **NOTE:** If you select *Automatic* updates, the Operator Lifecycle Manager (OLM) automatically updates the running instance of LVM Storage without any intervention. If you select *Manual* updates, the OLM creates an update request. As a cluster administrator, you must manually approve the update request to update LVM Storage to a newer version.
1. Optional: Select the *Enable Operator recommended cluster monitoring on this Namespace* checkbox.
1. Click *Install*.

.Verification steps

- Verify that LVM Storage shows a green tick, indicating successful installation.