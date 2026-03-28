# Adding worker nodes using the Assisted Installer and OpenShift Cluster Manager

You can add worker nodes to single-node OpenShift clusters that were created on the [OpenShift Cluster Manager](https://console.redhat.com/openshift) by using the [Assisted Installer](https://console.redhat.com/openshift/assisted-installer/clusters/~new). This method provides and alternative to using command-line commands.

> **IMPORTANT:** Adding worker nodes to single-node OpenShift clusters is only supported for clusters running OpenShift Container Platform version 4.11 and up.

.Prerequisites

- Have access to a single-node OpenShift cluster installed using link:https://console.redhat.com/openshift/assisted-installer/clusters/~new[Assisted Installer].
- Install the OpenShift CLI (`oc`).
- Log in as a user with `cluster-admin` privileges.
- Ensure that all the required DNS records exist for the cluster that you are adding the worker node to.

.Procedure

1. Log in to the link:https://console.redhat.com/openshift[OpenShift Cluster Manager] and click the single-node cluster that you want to add a worker node to.

1. Click *Add hosts*, and download the discovery ISO for the new worker node, adding SSH public key and configuring cluster-wide proxy settings as required.

1. Boot the target host using the discovery ISO, and wait for the host to be discovered in the console. After the host is discovered, start the installation.

1. As the installation proceeds, the installation generates pending certificate signing requests (CSRs) for the worker node. When prompted, approve the pending CSRs to complete the installation.
When the worker node is sucessfully installed, it is listed as a worker node in the cluster web console.
> **IMPORTANT:** New worker nodes are encrypted using the same method as the original cluster.