# Determining the cluster version update path

Use the [Red Hat OpenShift Container Platform Update Graph](https://access.redhat.com/labs/ocpupgradegraph/update_path/) tool to determine if the path is valid for the z-stream release you want to update to.

> **IMPORTANT:** The <4.y+1.z> or <4.y+2.z> version that you update to must have the same patch level as the <4.y.z> release you are updating from. The OpenShift Container Platform update process mandates that if a fix is present in a specific <4.y.z> release, then the that fix must be present in the <4.y+1.z> release that you update to.

.Bug fix backporting and the update graph
image::openshift-bug-fix-backporting-update-graph.png[Bug fix backporting and the update graph]

> **IMPORTANT:** OpenShift Container Platform development has a strict backport policy that prevents regressions. For example, a bug must be fixed in 4.16.z before it is fixed in 4.15.z. This means that the update graph does not allow for updates to chronologically older releases even if the minor version is greater, for example, updating from 4.15.24 to 4.16.2.