# Adding a real-time kernel to nodes

If your OpenShift Container Platform workloads require real-time operating system characteristics, you can switch your machines to the Linux real-time kernel. Switching to the real-time kernel provides a higher degree of determinism for your OpenShift Container Platform workloads. 

Even though Linux is not a real-time operating system, the Linux real-time
kernel includes a preemptive scheduler that provides the operating system with real-time characteristics. For OpenShift Container Platform, 4.21 you can make the switch to real-time kernel by using a `MachineConfig` object. 

Although making the change is as simple as changing a machine config `kernelType` setting to `realtime`, there are a few other considerations before making the change:

- Currently, real-time kernel is supported only on worker nodes, and only for radio access network (RAN) use.
- The following procedure is fully supported with bare metal installations that use systems that are certified for Red Hat Enterprise Linux for Real Time 8.
- Real-time support in OpenShift Container Platform is limited to specific subscriptions.
- The following procedure is also supported for use with Google Cloud.

.Prerequisites
- Have a running OpenShift Container Platform cluster (version 4.4 or later).
- Log in to the cluster as a user with administrative privileges.

.Procedure

1. Create a machine config for the real-time kernel: Create a YAML file (for example, `99-worker-realtime.yaml`) that contains a `MachineConfig`
object for the `realtime` kernel type. This example tells the cluster to use a real-time kernel for all worker nodes:
```bash
$ cat << EOF > 99-worker-realtime.yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  labels:
    machineconfiguration.openshift.io/role: "worker"
  name: 99-worker-realtime
spec:
  kernelType: realtime
EOF
```

1. Add the machine config to the cluster. Type the following to add the machine config to the cluster:
```bash
$ oc create -f 99-worker-realtime.yaml
```

1. Check the real-time kernel: Once each impacted node reboots, log in to the cluster and run the following commands to make sure that the real-time kernel has replaced the regular kernel for the set of nodes you configured:
```bash
$ oc get nodes
```
.Example output
```bash
NAME                                        STATUS  ROLES    AGE   VERSION
ip-10-0-143-147.us-east-2.compute.internal  Ready   worker   103m  v1.34.2
ip-10-0-146-92.us-east-2.compute.internal   Ready   worker   101m  v1.34.2
ip-10-0-169-2.us-east-2.compute.internal    Ready   worker   102m  v1.34.2
```
```bash
$ oc debug node/ip-10-0-143-147.us-east-2.compute.internal
```
.Example output
```bash
Starting pod/ip-10-0-143-147us-east-2computeinternal-debug ...
To use host binaries, run `chroot /host`

sh-4.4# uname -a
Linux <worker_node> 4.18.0-147.3.1.rt24.96.el8_1.x86_64 #1 SMP PREEMPT RT
        Wed Nov 27 18:29:55 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
```
The kernel name contains `rt` and text “PREEMPT RT” indicates that this is a real-time kernel.

1. To go back to the regular kernel, delete the `MachineConfig` object:
```bash
$ oc delete -f 99-worker-realtime.yaml
```