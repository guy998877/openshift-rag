// * post_installation_configuration/configuring-multi-arch-compute-machines/multi-architecture-configuration.adoc

# Verifying cluster compatibility

Before you can start adding compute nodes of different architectures to your cluster, you must verify that your cluster is multi-architecture compatible.

.Prerequisites

- You installed the pass:quotes[OpenShift CLI (`oc`)].
- IBM Power only: Ensure that you meet the following prerequisites:
- When using multiple architectures, hosts for OpenShift Container Platform nodes must share the same storage layer. If they do not have the same storage layer, use a storage provider such as `nfs-provisioner`.
- You should limit the number of network hops between the compute and control plane as much as possible.

.Procedure

1. Log in to the pass:quotes[OpenShift CLI (`oc`)].

1. You can check that your cluster uses the architecture payload by running the following command:
```bash
$ oc adm release info -o jsonpath="{ .metadata.metadata}"
```

.Verification

- If you see the following output, your cluster is using the multi-architecture payload:
```bash
{
 "release.openshift.io/architecture": "multi",
 "url": "https://access.redhat.com/errata/<errata_version>"
}
```
You can then begin adding multi-arch compute nodes to your cluster.

- If you see the following output, your cluster is not using the multi-architecture payload:
```bash
{
 "url": "https://access.redhat.com/errata/<errata_version>"
}
```
> **IMPORTANT:** To migrate your cluster so the cluster supports multi-architecture compute machines, follow the procedure in xref:../../updating/updating_a_cluster/migrating-to-multi-payload.adoc#migrating-to-multi-payload[Migrating to a cluster with multi-architecture compute machines].