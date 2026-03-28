# Creating a ContainerRuntimeConfig CR to edit CRI-O parameters

You can change some of the settings associated with the OpenShift Container Platform CRI-O runtime for the nodes associated with a specific machine config pool (MCP). Using a `ContainerRuntimeConfig` custom resource (CR), you set the configuration values and add a label to match the MCP. The MCO then rebuilds the `crio.conf` and `storage.conf` configuration files on the associated nodes with the updated values.

> **NOTE:** To revert the changes implemented by using a `ContainerRuntimeConfig` CR, you must delete the CR. Removing the label from the machine config pool does not revert the changes.

You can modify the following settings by using a `ContainerRuntimeConfig` CR:

- **Log level**: The `logLevel` parameter sets the CRI-O `log_level` parameter, which is the level of verbosity for log messages. The default is `info` (`log_level = info`). Other options include `fatal`, `panic`, `error`, `warn`, `debug`, and `trace`.
- **Overlay size**: The `overlaySize` parameter sets the CRI-O Overlay storage driver `size` parameter, which is the maximum size of a container image.
- **Container runtime**: The `defaultRuntime` parameter sets the container runtime to either `crun` or `runc`. The default is `crun`.

You should have one `ContainerRuntimeConfig` CR for each machine config pool with all the config changes you want for that pool. If you are applying the same content to all the pools, you only need one `ContainerRuntimeConfig` CR for all the pools.

You should edit an existing `ContainerRuntimeConfig` CR to modify existing settings or add new settings instead of creating a new CR for each change. It is recommended to create a new `ContainerRuntimeConfig` CR only to modify a different machine config pool, or for changes that are intended to be temporary so that you can revert the changes.

You can create multiple `ContainerRuntimeConfig` CRs, as needed, with a limit of 10 per cluster. For the first `ContainerRuntimeConfig` CR, the MCO creates a machine config appended with `containerruntime`. With each subsequent CR, the controller creates a new `containerruntime` machine config with a numeric suffix. For example, if you have a `containerruntime` machine config with a `-2` suffix, the next `containerruntime` machine config is appended with `-3`.

If you want to delete the machine configs, you should delete them in reverse order to avoid exceeding the limit. For example, you should delete the `containerruntime-3` machine config before deleting the `containerruntime-2` machine config.

> **NOTE:** If you have a machine config with a `containerruntime-9` suffix, and you create another `ContainerRuntimeConfig` CR, a new machine config is not created, even if there are fewer than 10 `containerruntime` machine configs.

.Example showing multiple `ContainerRuntimeConfig` CRs
```bash
$ oc get ctrcfg
```

.Example output
```bash
NAME         AGE
ctr-overlay  15m
ctr-level    5m45s
```

.Example showing multiple `containerruntime` machine configs
```bash
$ oc get mc | grep container
```

.Example output
```bash
...
01-master-container-runtime                        b5c5119de007945b6fe6fb215db3b8e2ceb12511   3.5.0             57m
...
01-worker-container-runtime                        b5c5119de007945b6fe6fb215db3b8e2ceb12511   3.5.0             57m
...
99-worker-generated-containerruntime               b5c5119de007945b6fe6fb215db3b8e2ceb12511   3.5.0             26m
99-worker-generated-containerruntime-1             b5c5119de007945b6fe6fb215db3b8e2ceb12511   3.5.0             17m
99-worker-generated-containerruntime-2             b5c5119de007945b6fe6fb215db3b8e2ceb12511   3.5.0             7m26s
...
```

The following example sets the `log_level` field to `debug`, sets the overlay size to 8 GB, and configures runC as the container runtime:

.Example `ContainerRuntimeConfig` CR
```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: ContainerRuntimeConfig
metadata:
 name: overlay-size
spec:
 machineConfigPoolSelector:
   matchLabels:
     pools.operator.machineconfiguration.openshift.io/worker: '' <1>
 containerRuntimeConfig:
   logLevel: debug <2>
   overlaySize: 8G <3>
   defaultRuntime: "runc" <4>
```
<1> Specifies the machine config pool label. For a container runtime config, the role must match the name of the associated machine config pool.
<2> Optional: Specifies the level of verbosity for log messages.
<3> Optional: Specifies the maximum size of a container image.
<4> Optional: Specifies the container runtime to deploy to new containers, either `crun` or `runc`. The default value is `crun`.

.Procedure

To change CRI-O settings using the `ContainerRuntimeConfig` CR:

1. Create a YAML file for the `ContainerRuntimeConfig` CR:
```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: ContainerRuntimeConfig
metadata:
 name: overlay-size
spec:
 machineConfigPoolSelector:
   matchLabels:
     pools.operator.machineconfiguration.openshift.io/worker: '' <1>
 containerRuntimeConfig: <2>
   logLevel: debug
   overlaySize: 8G
   defaultRuntime: "runc"
```
<1> Specify a label for the machine config pool that you want you want to modify.
<2> Set the parameters as needed.

1. Create the `ContainerRuntimeConfig` CR:
```bash
$ oc create -f <file_name>.yaml
```

1. Verify that the CR is created:
```bash
$ oc get ContainerRuntimeConfig
```
.Example output
```bash
NAME           AGE
overlay-size   3m19s
```

1. Check that a new `containerruntime` machine config is created:
```bash
$ oc get machineconfigs | grep containerrun
```
.Example output
```bash
99-worker-generated-containerruntime   2c9371fbb673b97a6fe8b1c52691999ed3a1bfc2  3.5.0  31s
```

1. Monitor the machine config pool until all are shown as ready:
```bash
$ oc get mcp worker
```
.Example output
```bash
NAME    CONFIG               UPDATED  UPDATING  DEGRADED  MACHINECOUNT  READYMACHINECOUNT  UPDATEDMACHINECOUNT  DEGRADEDMACHINECOUNT  AGE
worker  rendered-worker-169  False    True      False     3             1                  1                    0                     9h
```

1. Verify that the settings were applied in CRI-O:

.. Open an `oc debug` session to a node in the machine config pool and run `chroot /host`.
```bash
$ oc debug node/<node_name>
```
```bash
sh-4.4# chroot /host
```

.. Verify the changes in the `crio.conf` file:
```bash
sh-4.4# crio config | grep 'log_level'
```
.Example output
```bash
log_level = "debug"
```

.. Verify the changes in the `storage.conf` file:
```bash
sh-4.4# head -n 7 /etc/containers/storage.conf
```
.Example output
```bash
[storage]
  driver = "overlay"
  runroot = "/var/run/containers/storage"
  graphroot = "/var/lib/containers/storage"
  [storage.options]
    additionalimagestores = []
    size = "8G"
```

.. Verify the changes in the `crio/crio.conf.d/01-ctrcfg-defaultRuntime` file:
```bash
sh-5.1# cat /etc/crio/crio.conf.d/01-ctrcfg-defaultRuntime
```
.Example output
```bash
[crio]
  [crio.runtime]
    default_runtime = "runc"
```