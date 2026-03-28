# Adding extensions to RHCOS

RHCOS is a minimal container-oriented RHEL operating system, designed to provide a common set of capabilities to OpenShift Container Platform clusters across all platforms. Although adding software packages to RHCOS systems is generally discouraged, the MCO provides an `extensions` feature you can use to add a minimal set of features to RHCOS nodes.

Currently, the following extensions are available:

- **usbguard**: The `usbguard` extension protects RHCOS systems from attacks by intrusive USB devices. For more information, see link:https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html-single/security_hardening/index#usbguard_protecting-systems-against-intrusive-usb-devices[USBGuard] for details.

- **kerberos**: The `kerberos` extension provides a mechanism that allows both users and machines to identify themselves to the network to receive defined, limited access to the areas and services that an administrator has configured. For more information, see link:https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/system-level_authentication_guide/using_kerberos[Using Kerberos] for details, including how to set up a Kerberos client and mount a Kerberized NFS share.

- **sandboxed-containers**: The `sandboxed-containers` extension contains RPMs for Kata, QEMU, and its dependencies. For more information, see https://docs.redhat.com/en/documentation/openshift_sandboxed_containers/latest[OpenShift Sandboxed Containers].

- **ipsec**: The `ipsec` extension contains RPMs for libreswan and NetworkManager-libreswan.

- **wasm**: The `wasm` extension enables Developer Preview functionality in OpenShift Container Platform for users who want to use WASM-supported workloads.   

- **sysstat**: Adding the `sysstat` extension provides additional performance monitoring for OpenShift Container Platform nodes, including the system activity reporter (`sar`) command for collecting and reporting information.

- **kernel-devel**: The `kernel-devel` extension provides kernel headers and makefiles sufficient to build modules against the kernel package.

The following procedure describes how to use a machine config to add one or more extensions to your RHCOS nodes.

.Prerequisites
- Have a running OpenShift Container Platform cluster (version 4.6 or later).
- Log in to the cluster as a user with administrative privileges.

.Procedure

1. Create a machine config for extensions: Create a YAML file (for example, `80-extensions.yaml`) that contains a `MachineConfig` `extensions` object. This example tells the cluster to add the `usbguard` extension.
```bash
$ cat << EOF > 80-extensions.yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  labels:
    machineconfiguration.openshift.io/role: worker
  name: 80-worker-extensions
spec:
  config:
    ignition:
      version: 3.5.0
  extensions:
    - usbguard
EOF
```

1. Add the machine config to the cluster. Type the following to add the machine config to the cluster:
```bash
$ oc create -f 80-extensions.yaml
```
This sets all worker nodes to have rpm packages for `usbguard` installed.

1. Check that the extensions were applied:
```bash
$ oc get machineconfig 80-worker-extensions
```
.Example output
```bash
NAME                 GENERATEDBYCONTROLLER IGNITIONVERSION AGE
80-worker-extensions                       3.5.0           57s
```

1. Check that the new machine config is now applied and that the nodes are not in a degraded state. It may take a few minutes. The worker pool will show the updates in progress, as each machine successfully has the new machine config applied:
```bash
$ oc get machineconfigpool
```
.Example output
```bash
NAME   CONFIG             UPDATED UPDATING DEGRADED MACHINECOUNT READYMACHINECOUNT UPDATEDMACHINECOUNT DEGRADEDMACHINECOUNT AGE
master rendered-master-35 True    False    False    3            3                 3                   0                    34m
worker rendered-worker-d8 False   True     False    3            1                 1                   0                    34m
```

1. Check the extensions. To check that the extension was applied, run:
```bash
$ oc get node | grep worker
```
.Example output
```bash
NAME                                        STATUS  ROLES    AGE   VERSION
ip-10-0-169-2.us-east-2.compute.internal    Ready   worker   102m  v1.34.2
```
```bash
$ oc debug node/ip-10-0-169-2.us-east-2.compute.internal
```
.Example output
```bash
...
To use host binaries, run `chroot /host`
sh-4.4# chroot /host
sh-4.4# rpm -q usbguard
usbguard-0.7.4-4.el8.x86_64.rpm
```