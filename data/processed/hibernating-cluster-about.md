# About cluster hibernation

OpenShift Container Platform clusters can be hibernated in order to save money on cloud hosting costs. You can hibernate your OpenShift Container Platform cluster for up to 90 days and expect it to resume successfully.

You must wait at least 24 hours after cluster installation before hibernating your cluster to allow for the first certification rotation.

> **IMPORTANT:** If you must hibernate your cluster before the 24 hour certificate rotation, use the following procedure instead: link:https://www.redhat.com/en/blog/enabling-openshift-4-clusters-to-stop-and-resume-cluster-vms[Enabling OpenShift 4 Clusters to Stop and Resume Cluster VMs].

When hibernating a cluster, you must hibernate all cluster nodes. It is not supported to suspend only certain nodes.

After resuming, it can take up to 45 minutes for the cluster to become ready.