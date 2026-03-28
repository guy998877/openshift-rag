// NOTE: This module is included several times in the same upgrade assembly.

// POOL-ONLY: Conditions for upgrading machine pools WITHOUT upgrading hosted control planes
//END POOL-ONLY condition

// WHOLE CLUSTER: Conditions for upgrading machine pools as part of upgrading the whole cluster in sequence
//END WHOLE CLUSTER condition

> **NOTE:** Machine pool configurations such as node drain timeout, max-unavailable, and max-surge can affect the timing and success of upgrades.

.Procedure
1. Verify the current version of your cluster by running the following command:
```bash
$ rosa describe cluster --cluster=<cluster_name_or_id>
```
Replace `<cluster_name_or_id>` with the cluster name or the cluster ID.

1. List the versions that you can upgrade your machine pools to by running the following command:
```bash
$ rosa list upgrade --cluster <cluster-name> --machinepool <machinepool_name>
```
The command returns a list of available updates, including the recommended version.
*Example output*
```bash
VERSION  NOTES
4.14.5   recommended
4.14.4
4.14.3
```
> **IMPORTANT:** Do not upgrade your machine pool to a version higher than your control plane. If you want to move to a higher version, upgrade the control plane to that version first.
//Is it even possible to do this? Will a higher version display? Can you specify a higher version even if it doesn't display?

1. Verify the upgrade behavior of the machine pools you intend to upgrade by running the following command:
```bash
$ rosa describe machinepool --cluster=<cluster_name_or_id> <machinepool_name>
```
*Example output*
```bash
Replicas: 5
Node drain grace period:   30 minutes

Management upgrade:
- Type: Replace
- Max surge: 20%
- Max unavailable: 20%
```
In the example, these settings allow the machine pool to provision one excess node (`max-surge` of 20% of `replicas`) and to have up to one node unavailable (`max-unavailable` of 20% of `replicas`) during an upgrade. This machine pool can therefore upgrade two nodes at a time, by provisioning one new node in excess of the replica count, and by making one node unavailable and replacing it. Node upgrades may be delayed by up to 30 minutes (`node-drain-grace-period` of 30 minutes) if necessary to protect workloads that have a pod disruption budget.

1. Upgrade a machine pool by running the following command:
```bash
$ rosa upgrade machinepool -c <cluster_name> <machinepool_name> [--schedule-date=<yyyy-mm-dd> --schedule-time=<HH:mm>] --version <version_number>
```
You can upgrade multiple machine pools concurrently by running this command for each machine pool you want to upgrade.

- To schedule the immediate upgrade of a machine pool, run the following command:
```bash
$ rosa upgrade machinepool -c <cluster_name> <machinepool_name> --version <version_number>
```
The machine pool is scheduled for immediate upgrade, which initiates a rolling replacement of all nodes in the specified machine pool.

- To schedule an upgrade to start at a future time, run the following command:
```bash
$ rosa upgrade machinepool -c <cluster_name> <machinepool_name> --schedule-date=<yyyy-mm-dd> --schedule-time=<HH:mm> --version <version_number>
```
The machine pool is scheduled to begin an upgrade at the specified time and date in Coordinated Universal Time (UTC). This will initiate a rolling replacement of all nodes in the specified machine pool, beginning at the specified time.