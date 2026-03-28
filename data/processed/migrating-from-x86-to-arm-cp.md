# Migrating the x86 control plane to arm64 architecture on Amazon Web Services

You can migrate the control plane in your cluster from `x86` to `arm64` architecture on Amazon Web Services (AWS).

.Prerequisites

- You have installed the pass:quotes[OpenShift CLI (`oc`)].
- You logged in to `oc` as a user with `cluster-admin` privileges.

.Procedure

1. Check the architecture of the control plane nodes by running the following command:
```bash
$ oc get nodes -o wide
```
.Example output
```bash
NAME                          STATUS   ROLES                  AGE    VERSION   INTERNAL-IP EXTERNAL-IP   OS-IMAGE                                         KERNEL-VERSION                 CONTAINER-RUNTIME
worker-001.example.com        Ready    worker                 100d   v1.30.7   10.x.x.x    <none>        Red Hat Enterprise Linux CoreOS 4xx.xx.xxxxx-0   5.x.x-xxx.x.x.el9_xx.x86_64    cri-o://1.30.x
worker-002.example.com        Ready    worker                 98d    v1.30.7   10.x.x.x    <none>        Red Hat Enterprise Linux CoreOS 4xx.xx.xxxxx-0   5.x.x-xxx.x.x.el9_xx.x86_64    cri-o://1.30.x
worker-003.example.com        Ready    worker                 98d    v1.30.7   10.x.x.x    <none>        Red Hat Enterprise Linux CoreOS 4xx.xx.xxxxx-0   5.x.x-xxx.x.x.el9_xx.x86_64    cri-o://1.30.x
master-001.example.com        Ready    control-plane,master   120d   v1.30.7   10.x.x.x    <none>        Red Hat Enterprise Linux CoreOS 4xx.xx.xxxxx-0   5.x.x-xxx.x.x.el9_xx.x86_64    cri-o://1.30.x
master-002.example.com        Ready    control-plane,master   120d   v1.30.7   10.x.x.x    <none>        Red Hat Enterprise Linux CoreOS 4xx.xx.xxxxx-0   5.x.x-xxx.x.x.el9_xx.x86_64    cri-o://1.30.x
master-003.example.com        Ready    control-plane,master   120d   v1.30.7   10.x.x.x    <none>        Red Hat Enterprise Linux CoreOS 4xx.xx.xxxxx-0   5.x.x-xxx.x.x.el9_xx.x86_64    cri-o://1.30.x
```
The `KERNEL-VERSION` field in the output indicates the architecture of the nodes.

1. Check that your cluster uses the multi payload by running the following command:
```bash
$ oc adm release info -o jsonpath="{ .metadata.metadata}"
```
If you see the following output, the cluster is multi-architecture compatible.
```bash
{
 "release.openshift.io/architecture": "multi",
 "url": "https://access.redhat.com/errata/<errata_version>"
}
```
If the cluster is not using the multi payload, migrate the cluster to a multi-architecture cluster. For more information, see "Migrating to a cluster with multi-architecture compute machines". 

1. Update your image stream from single-architecture to multi-architecture by running the following command:
--
--

1. Get the `arm64` compatible Amazon Machine Image (AMI) for configuring the control plane machine set by running the following command:
```bash
$ oc get configmap/coreos-bootimages -n openshift-machine-config-operator -o jsonpath='{.data.stream}' | jq -r '.architectures.aarch64.images.aws.regions."<aws_region>".image' <1>
```
<1> Replace `<aws_region>` with the AWS region where the current cluster is installed. You can get the AWS region for the installed cluster by running the following command:
```bash
$ oc get infrastructure cluster -o jsonpath='{.status.platformStatus.aws.region}'
```
.Example output
```bash
ami-xxxxxxx
```

1. Update the control plane machine set to support the `arm64` architecture by running the following command:
```bash
$ oc edit controlplanemachineset.machine.openshift.io cluster -n openshift-machine-api
```
Update the `instanceType` field to a type that supports the `arm64` architecture, and set the `ami.id` field to an AMI that is compatible with the `arm64` architecture. For information about supported instance types, see "Tested instance types for AWS on 64-bit ARM infrastructures".
For more information about configuring the control plane machine set for AWS, see "Control plane configuration options for Amazon Web Services".

.Verification

- Verify that the control plane nodes are now running on the `arm64` architecture:
```bash
$ oc get nodes -o wide
```
.Example output
```bash
NAME                          STATUS   ROLES                  AGE    VERSION   INTERNAL-IP EXTERNAL-IP   OS-IMAGE                                         KERNEL-VERSION                 CONTAINER-RUNTIME
worker-001.example.com        Ready    worker                 100d   v1.30.7   10.x.x.x    <none>        Red Hat Enterprise Linux CoreOS 4xx.xx.xxxxx-0   5.x.x-xxx.x.x.el9_xx.x86_64    cri-o://1.30.x
worker-002.example.com        Ready    worker                 98d    v1.30.7   10.x.x.x    <none>        Red Hat Enterprise Linux CoreOS 4xx.xx.xxxxx-0   5.x.x-xxx.x.x.el9_xx.x86_64    cri-o://1.30.x
worker-003.example.com        Ready    worker                 98d    v1.30.7   10.x.x.x    <none>        Red Hat Enterprise Linux CoreOS 4xx.xx.xxxxx-0   5.x.x-xxx.x.x.el9_xx.x86_64    cri-o://1.30.x
master-001.example.com        Ready    control-plane,master   120d   v1.30.7   10.x.x.x    <none>        Red Hat Enterprise Linux CoreOS 4xx.xx.xxxxx-0   5.x.x-xxx.x.x.el9_xx.aarch64   cri-o://1.30.x
master-002.example.com        Ready    control-plane,master   120d   v1.30.7   10.x.x.x    <none>        Red Hat Enterprise Linux CoreOS 4xx.xx.xxxxx-0   5.x.x-xxx.x.x.el9_xx.aarch64   cri-o://1.30.x
master-003.example.com        Ready    control-plane,master   120d   v1.30.7   10.x.x.x    <none>        Red Hat Enterprise Linux CoreOS 4xx.xx.xxxxx-0   5.x.x-xxx.x.x.el9_xx.aarch64   cri-o://1.30.x
```