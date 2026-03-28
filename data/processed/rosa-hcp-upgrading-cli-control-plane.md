// NOTE: This module is included several times in the same upgrade assembly.

// HCP-ONLY: Conditions for upgrading the hosted control plane WITHOUT upgrading any machine pools
//END HCP-ONLY conditions

// WHOLE CLUSTER: Condition for upgrading hosted control plane as part of upgrading the whole cluster in sequence

.Prerequisites
- You have installed and configured the latest version of the ROSA CLI.
- No machine pool upgrades are in progress or scheduled to take place at the same time as the hosted control plane upgrade.

//END WHOLE CLUSTER conditions

.Procedure

1. Verify the current version of your cluster by running the following command:
```bash
$ rosa describe cluster --cluster=<cluster_name_or_id>
```
Replace `<cluster_name_or_id>` with the cluster name or the cluster ID.

1. List the versions that you can upgrade your control plane to by running the following command:
```bash
$ rosa list upgrade --cluster=<cluster_name_or_id>
```
The command returns a list of available updates, including the recommended version.
*Example output*
```bash
VERSION  NOTES
4.14.8   recommended
4.14.7
4.14.6
```

1. Upgrade the cluster's hosted control plane by running the following command:
```bash
$ rosa upgrade cluster -c <cluster_name_or_id> [--schedule-date=<yyyy-mm-dd> --schedule-time=<HH:mm>] --version <version_number>
```

- To schedule an immediate upgrade to the specified version, run the following command:
```bash
$ rosa upgrade cluster -c <cluster_name_or_id> --version <version_number>
```
Your hosted control plane is scheduled for an immediate upgrade.

- To schedule an upgrade to the specified version at a future date, run the following command:
```bash
$ rosa upgrade cluster -c <cluster_name_or_id> --schedule-date=<yyyy-mm-dd> --schedule-time=<HH:mm> --version=<version_number>
```
Your hosted control plane is scheduled for an upgrade at the specified time in Coordinated Universal Time (UTC).