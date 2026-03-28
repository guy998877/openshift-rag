# Disabling the Machine Config Operator from automatically rebooting by using the console

To avoid unwanted disruptions from changes made by the Machine Config Operator (MCO), you can use the OpenShift Container Platform web console to modify the machine config pool (MCP) to prevent the MCO from making any changes to nodes in that pool. This prevents any reboots that would normally be part of the MCO update process.

.Prerequisites

- You have access to the cluster as a user with the `cluster-admin` role.

.Procedure

1. Log in to the OpenShift Container Platform web console as a user with the `cluster-admin` role.

1. Click *Compute* -> *MachineConfigPools*.

1. On the *MachineConfigPools* page, click either *master* or *worker*, depending upon which nodes you want to pause rebooting for.

1. On the *master* or *worker* page, click *YAML*.

1. In the YAML, update the `spec.paused` field to `true`.
.Sample MachineConfigPool object
```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfigPool
# ...
spec:
# ...
  paused: true
# ...
```
Update the `spec.paused` field to `true` to pause rebooting.

1. To verify that the MCP is paused, return to the *MachineConfigPools* page.
On the *MachineConfigPools* page, the *Paused* column reports *True* for the MCP you modified.
If the MCP has pending changes while paused, the *Updated* column is *False* and *Updating* is *False*. When *Updated* is *True* and *Updating* is *False*, there are no pending changes.
> **IMPORTANT:** If there are pending changes (where both the *Updated* and *Updating* columns are *False*), it is recommended to schedule a maintenance window for a reboot as early as possible. Use the following steps for unpausing the autoreboot process to apply the changes that were queued since the last reboot.

- Unpause the autoreboot process:

1. Log in to the OpenShift Container Platform web console as a user with the `cluster-admin` role.

1. Click *Compute* -> *MachineConfigPools*.

1. On the *MachineConfigPools* page, click either *master* or *worker*, depending upon which nodes you want to pause rebooting for.

1. On the *master* or *worker* page, click *YAML*.

1. In the YAML, update the `spec.paused` field to `false`.
.Sample MachineConfigPool object
```yaml
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfigPool
# ...
spec:
# ...
  paused: false
# ...
```
Update the `spec.paused` field to `false` to allow rebooting.
> **NOTE:** By unpausing an MCP, the MCO applies all paused changes reboots Red Hat Enterprise Linux CoreOS (RHCOS) as needed.

1. To verify that the MCP is paused, return to the *MachineConfigPools* page.
On the *MachineConfigPools* page, the *Paused* column reports *False* for the MCP you modified.
If the MCP is applying any pending changes, the *Updated* column is *False* and the *Updating* column is *True*. When *Updated* is *True* and *Updating* is *False*, there are no further changes being made.