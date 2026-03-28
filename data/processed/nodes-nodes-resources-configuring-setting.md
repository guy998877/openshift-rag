# Manually allocating resources for nodes

As an administrator, you can manually set `system-reserved` CPU and memory resources for your nodes. Setting these values ensures that your cluster is running efficiently and prevents node failure due to resource starvation of system components.

By default, OpenShift Container Platform uses a script on each worker node to automatically determine the optimal `system-reserved` CPU and memory resources for nodes associated with a specific machine config pool and update the nodes with those values. The script runs on node start up.

> **IMPORTANT:** If you updated your cluster from a version earlier than 4.21, automatic allocation of system resources is disabled by default. To enable the feature, delete the `50-worker-auto-sizing-disabled` machine config.

However, you can manually set these values by using a `KubeletConfig` custom resource (CR) that includes a set of `<resource_type>=<resource_quantity>` pairs (for example, `cpu=200m,memory=512Mi`). You must use the `spec.autoSizingReserved: false` parameter in the `KubeletConfig` CR to override the default OpenShift Container Platform behavior of automatically setting the `systemReserved` values.

For `memory` and `ephemeral-storage`, you specify the resource quantity in units of bytes, such as `200Ki`, `50Mi`, or `5Gi`. By default, the `system-reserved` CPU is `500m` and `system-reserved` memory is `1Gi`. For the `cpu` type, you specify the resource quantity in units of cores, such as `200m`, `0.5`, or `1`. Note that 1000 millicores is equal to 1CPU/vCPU.

> **IMPORTANT:** * For details on the recommended `system-reserved` values, refer to the link:https://access.redhat.com/solutions/5843241[recommended system-reserved values]. * To manually set resource values, you must use a kubelet configuration. You cannot use a machine config.

.Prerequisites

- Obtain the label associated with the static `MachineConfigPool` CRD for the type of node you want to configure by entering the following command:

.Procedure

1. Create a custom resource (CR) for your configuration change.
.Sample configuration for a resource allocation CR
```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: KubeletConfig
metadata:
  name: set-allocatable
spec:
  autoSizingReserved: false
  machineConfigPoolSelector:
    matchLabels:
      pools.operator.machineconfiguration.openshift.io/worker: ""
  kubeletConfig:
    systemReserved:
      cpu: 1000m
      memory: 4Gi
      ephemeral-storage: 50Mi
#...
```
--
`metadata.name`:: Specifies a name for the CR.
`spec.autoSizingReserved`:: Specify `false` to override the default OpenShift Container Platform behavior of automatically setting the `systemReserved` values.
`spec.machineConfigPoolSelector.matchLabels`:: Specifies a label from the machine config pool.
`spec.kubeletConfig.systemReserved`:: Specifies the resources to reserve for the node components and system components.
--

1. Run the following command to create the CR:
```bash
$ oc create -f <file_name>.yaml
```

.Verification

1. Log in to a node you configured by entering the following command:
```bash
$ oc debug node/<node_name>
```

1. Set `/host` as the root directory within the debug shell:
```bash
# chroot /host
```

1. View the `/etc/node-sizing.env` file:
.Example output
```bash
SYSTEM_RESERVED_MEMORY=4Gi
SYSTEM_RESERVED_CPU=1000m
SYSTEM_RESERVED_ES=50Mi
```
The kubelet uses the `system-reserved` values in the `/etc/node-sizing.env` file.