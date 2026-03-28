# Deleting the ClusterPodPlacementConfig object by using the CLI

You can create only one instance of the `ClusterPodPlacementConfig` object. If you want to re-create this object, you must first delete the existing instance.

You can delete this object by using the OpenShift CLI (`oc`).

.Prerequisites

- You have installed `oc`.
- You have logged in to `oc` as a user with `cluster-admin` privileges.

.Procedure

1. Log in to the pass:quotes[OpenShift CLI (`oc`)].

1. Delete the `ClusterPodPlacementConfig` object by running the following command:
```bash
$ oc delete clusterpodplacementconfig cluster
```

.Verification

- To check that the `ClusterPodPlacementConfig` object is deleted, run the following command:
```bash
$ oc get clusterpodplacementconfig
```
.Example output
```bash
No resources found
```