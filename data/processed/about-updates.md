# Cluster update overview

OpenShift Container Platform updates involve several services, Operators, and processes working in tandem to change the cluster to the desired version.

Red Hat hosts a public OpenShift Update Service (OSUS), which serves a graph of update possibilities based on the OpenShift Container Platform release images in the official registry.
The graph contains update information for any public release.
OpenShift Container Platform clusters are configured to connect to the OSUS by default, and the OSUS responds to clusters with information about known update targets.

An update begins when either a cluster administrator or an automatic update controller edits the custom resource (CR) of the Cluster Version Operator (CVO) with a new version.
To reconcile the cluster with the newly specified version, the CVO retrieves the target release image from an image registry and begins to apply changes to the cluster.

> **NOTE:** Operators previously installed through Operator Lifecycle Manager (OLM) follow a different process for updates. See xref:../../operators/admin/olm-upgrading-operators.adoc#olm-upgrading-operators[Updating installed Operators] for more information.

The target release image contains manifest files for all cluster components that form a specific OCP version.
When updating the cluster to a new version, the CVO applies manifests in separate stages called Runlevels.
Most, but not all, manifests support one of the cluster Operators.
As the CVO applies a manifest to a cluster Operator, the Operator might perform update tasks to reconcile itself with its new specified version.

The CVO monitors the state of each applied resource and the states reported by all cluster Operators. The CVO only proceeds with the update when all manifests and cluster Operators in the active Runlevel reach a stable condition.
After the CVO updates the entire control plane through this process, the Machine Config Operator (MCO) updates the operating system and configuration of every node in the cluster.