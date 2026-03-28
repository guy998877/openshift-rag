# Upgrading with the ROSA CLI

You can use the {rosa-cli-first} to upgrade a OpenShift Container Platform cluster either immediately within one hour or at a future time.

.Prerequisites

- You have installed and configured the latest ROSA CLI on your installation host.
- Your OpenShift Container Platform cluster is in a `Ready` state.

.Procedure

1. To verify the current version of your cluster, enter the following command:
```bash
$ rosa describe cluster --cluster=<cluster_name|cluster_id> <1>
```
<1> Replace `<cluster_name|cluster_id>` with the cluster name or the ID of the cluster.

1. To verify that an upgrade is available, enter the following command:
```bash
$ rosa list upgrade --cluster=<cluster_name|cluster_id>
```
The command returns a list of versions to which the cluster can be upgraded, including a recommended version. The recommendation is based on the conditional update risks. Each known risk might apply to all clusters or only clusters matching certain conditions. Refer to the OpenShift release notes to evaluate, validate and determine the appropriate version to upgrade to.

1. To upgrade the cluster to a specified version immediately within the next hour, enter the following command:
> **NOTE:** If you are upgrading an AWS Security Token Service (STS) cluster, this command starts an interactive IAM Roles/policies upgrade mode process that verifies the account and operator role policies for the chosen cluster are compatible with the target version of the upgrade. If the policies are not compatible with the chosen upgrade version, the CLI automatically upgrades them in auto mode.
The cluster is scheduled for an immediate upgrade as denoted by the _Scheduled Time_. The upgrade will begin within one hour from the scheduled time.
1. Alternatively, to upgrade the cluster at a future time in UTC, enter the following command:
```bash
$ rosa upgrade cluster --cluster=<cluster_name|cluster_id>   \
          --version <version-id>   \
          --schedule-date yyyy-mm-dd \
          --schedule-time HH:mm
```
1. To customize the grace period for every node to be drained during the cluster upgrade, enter the following command:
```bash
$ rosa upgrade cluster --cluster=<cluster_name|cluster_id>   \
          --version <version-id>   \
          --node-drain-grace-period 15 minutes
```

.Verification

1. You can view the status of the upgrade by entering the following command, which shows both the status (scheduled or started) and the scheduled time.
```bash
$ rosa list upgrade --cluster=<cluster_name|cluster_id>
```
.Example output
```bash
VERSION  NOTES
4.15.14  recommended - scheduled for 2024-06-02 15:00 UTC
4.15.13
```

You will receive email notifications confirming the scheduling, beginning, and completion of the cluster upgrade.

.Troubleshooting
- Sometimes a scheduled upgrade does not trigger. See link:https://access.redhat.com/solutions/6648291[Upgrade maintenance cancelled] for more information.