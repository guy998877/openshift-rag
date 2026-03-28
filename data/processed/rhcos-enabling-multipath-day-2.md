# Enabling multipathing with kernel arguments on RHCOS

> **IMPORTANT:** Enabling multipathing during installation is supported and recommended for nodes provisioned in OpenShift Container Platform. In setups where any I/O to non-optimized paths results in I/O system errors, you must enable multipathing at installation time. For more information about enabling multipathing during installation time, see "Enabling multipathing post installation" in the _Installing on bare metal_ documentation.

Red Hat Enterprise Linux CoreOS (RHCOS) supports multipathing on the primary disk, allowing stronger resilience to hardware failure to achieve higher host availability. Postinstallation support is available by activating multipathing via the machine config.

> **IMPORTANT:** On IBM Z(R) and IBM(R) LinuxONE, you can enable multipathing only if you configured your cluster for it during installation. For more information, see "Installing RHCOS and starting the OpenShift Container Platform bootstrap process" in _Installing a cluster with z/VM on IBM Z(R) and IBM(R) LinuxONE_.
// Add xref once it's allowed.

> **IMPORTANT:** When an OpenShift Container Platform cluster is installed or configured as a postinstallation activity on a single VIOS host with "vSCSI" storage on IBM Power(R) with multipath configured, the CoreOS nodes with multipath enabled fail to boot. This behavior is expected, as only one path is available to the node.

.Prerequisites
- You have a running OpenShift Container Platform cluster.
- You are logged in to the cluster as a user with administrative privileges.
- You have confirmed that the disk is enabled for multipathing. Multipathing is only supported on hosts that are connected to a SAN via an HBA adapter.

.Procedure

1. To enable multipathing postinstallation on control plane nodes:

- Create a machine config file, such as `99-master-kargs-mpath.yaml`, that instructs the cluster to add the `master` label and that identifies the multipath kernel argument, for example:
```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  labels:
    machineconfiguration.openshift.io/role: "master"
  name: 99-master-kargs-mpath
spec:
  kernelArguments:
    - 'rd.multipath=default'
    - 'root=/dev/disk/by-label/dm-mpath-root'
```

1. To enable multipathing postinstallation on worker nodes:

- Create a machine config file, such as `99-worker-kargs-mpath.yaml`, that instructs the cluster to add the `worker` label and that identifies the multipath kernel argument, for example:
```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
metadata:
  labels:
    machineconfiguration.openshift.io/role: "worker"
  name: 99-worker-kargs-mpath
spec:
  kernelArguments:
    - 'rd.multipath=default'
    - 'root=/dev/disk/by-label/dm-mpath-root'
```

1. Create the new machine config by using either the master or worker YAML file you previously created:
```bash
$ oc create -f ./99-worker-kargs-mpath.yaml
```

1. Check the machine configs to see that the new one was added:
```bash
$ oc get MachineConfig
```
.Example output
```bash
NAME                                               GENERATEDBYCONTROLLER                      IGNITIONVERSION   AGE
00-master                                          52dd3ba6a9a527fc3ab42afac8d12b693534c8c9   3.5.0             33m
00-worker                                          52dd3ba6a9a527fc3ab42afac8d12b693534c8c9   3.5.0             33m
01-master-container-runtime                        52dd3ba6a9a527fc3ab42afac8d12b693534c8c9   3.5.0             33m
01-master-kubelet                                  52dd3ba6a9a527fc3ab42afac8d12b693534c8c9   3.5.0             33m
01-worker-container-runtime                        52dd3ba6a9a527fc3ab42afac8d12b693534c8c9   3.5.0             33m
01-worker-kubelet                                  52dd3ba6a9a527fc3ab42afac8d12b693534c8c9   3.5.0             33m
99-master-generated-registries                     52dd3ba6a9a527fc3ab42afac8d12b693534c8c9   3.5.0             33m
99-master-ssh                                                                                 3.2.0             40m
99-worker-generated-registries                     52dd3ba6a9a527fc3ab42afac8d12b693534c8c9   3.5.0             33m
99-worker-kargs-mpath                              52dd3ba6a9a527fc3ab42afac8d12b693534c8c9   3.5.0             105s
99-worker-ssh                                                                                 3.2.0             40m
rendered-master-23e785de7587df95a4b517e0647e5ab7   52dd3ba6a9a527fc3ab42afac8d12b693534c8c9   3.5.0             33m
rendered-worker-5d596d9293ca3ea80c896a1191735bb1   52dd3ba6a9a527fc3ab42afac8d12b693534c8c9   3.5.0             33m
```

1. Check the nodes:
```bash
$ oc get nodes
```
.Example output
```bash
NAME                           STATUS                     ROLES    AGE   VERSION
ip-10-0-136-161.ec2.internal   Ready                      worker   28m   v1.34.2
ip-10-0-136-243.ec2.internal   Ready                      master   34m   v1.34.2
ip-10-0-141-105.ec2.internal   Ready,SchedulingDisabled   worker   28m   v1.34.2
ip-10-0-142-249.ec2.internal   Ready                      master   34m   v1.34.2
ip-10-0-153-11.ec2.internal    Ready                      worker   28m   v1.34.2
ip-10-0-153-150.ec2.internal   Ready                      master   34m   v1.34.2
```
You can see that scheduling on each worker node is disabled as the change is being applied.

1. Check that the kernel argument worked by going to one of the worker nodes and listing
the kernel command-line arguments (in `/proc/cmdline` on the host):
```bash
$ oc debug node/ip-10-0-141-105.ec2.internal
```
.Example output
```bash
Starting pod/ip-10-0-141-105ec2internal-debug ...
To use host binaries, run `chroot /host`

sh-4.2# cat /host/proc/cmdline
...
rd.multipath=default root=/dev/disk/by-label/dm-mpath-root
...

sh-4.2# exit
```
You should see the added kernel arguments.