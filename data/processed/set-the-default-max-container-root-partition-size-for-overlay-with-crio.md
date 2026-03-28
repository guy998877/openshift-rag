# Setting the default maximum container root partition size for Overlay with CRI-O

The root partition of each container shows all of the available disk space of the underlying host. Follow this guidance to set a maximum partition size for the root disk of all containers.

To configure the maximum Overlay size, as well as other CRI-O options like the log level, you can create the following `ContainerRuntimeConfig` custom resource definition (CRD):

```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: ContainerRuntimeConfig
metadata:
 name: overlay-size
spec:
 machineConfigPoolSelector:
   matchLabels:
     custom-crio: overlay-size
 containerRuntimeConfig:
   logLevel: debug
   overlaySize: 8G
```

.Procedure

1. Create the configuration object:
```bash
$ oc apply -f overlaysize.yml
```

1. To apply the new CRI-O configuration to your worker nodes, edit the worker machine config pool:
```bash
$ oc edit machineconfigpool worker
```

1. Add the `custom-crio` label based on the `matchLabels` name you set in the `ContainerRuntimeConfig` CRD:
```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfigPool
metadata:
  creationTimestamp: "2020-07-09T15:46:34Z"
  generation: 3
  labels:
    custom-crio: overlay-size
    machineconfiguration.openshift.io/mco-built-in: ""
```

1. Save the changes, then view the machine configs:
```bash
$ oc get machineconfigs
```
New `99-worker-generated-containerruntime` and `rendered-worker-xyz` objects are created:
.Example output
```bash
99-worker-generated-containerruntime  4173030d89fbf4a7a0976d1665491a4d9a6e54f1   3.5.0             7m42s
rendered-worker-xyz                   4173030d89fbf4a7a0976d1665491a4d9a6e54f1   3.5.0             7m36s
```

1. After those objects are created, monitor the machine config pool for the changes to be applied:
```bash
$ oc get mcp worker
```
The worker nodes show `UPDATING` as `True`, as well as the number of machines, the number updated, and other details:
.Example output
```bash
NAME   CONFIG              UPDATED   UPDATING   DEGRADED  MACHINECOUNT  READYMACHINECOUNT  UPDATEDMACHINECOUNT   DEGRADEDMACHINECOUNT   AGE
worker rendered-worker-xyz False True False     3             2                   2                    0                      20h
```
When complete, the worker nodes transition back to `UPDATING` as `False`, and the `UPDATEDMACHINECOUNT` number matches the `MACHINECOUNT`:
.Example output
```bash
NAME   CONFIG              UPDATED   UPDATING   DEGRADED  MACHINECOUNT  READYMACHINECOUNT  UPDATEDMACHINECOUNT   DEGRADEDMACHINECOUNT   AGE
worker   rendered-worker-xyz   True      False      False      3         3            3             0           20h
```
Looking at a worker machine, you see that the new 8 GB max size configuration is applied to all of the workers:
.Example output
```bash
head -n 7 /etc/containers/storage.conf
[storage]
  driver = "overlay"
  runroot = "/var/run/containers/storage"
  graphroot = "/var/lib/containers/storage"
  [storage.options]
    additionalimagestores = []
    size = "8G"
```
Looking inside a container, you see that the root partition is now 8 GB:
.Example output
```bash
~ $ df -h
Filesystem                Size      Used Available Use% Mounted on
overlay                   8.0G      8.0K      8.0G   0% /
```