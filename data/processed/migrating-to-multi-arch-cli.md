# Migrating to a cluster with multi-architecture compute machines using the CLI

.Prerequisites

- You have access to the cluster as a user with the `cluster-admin` role.
- Your OpenShift Container Platform version is up to date to at least version 4.13.0.
For more information on how to update your cluster version, see _Updating a cluster using the web console_ or _Updating a cluster using the CLI_.
- You have installed the OpenShift CLI (`oc`) that matches the version for your current cluster.
- Your `oc` client is updated to at least verion 4.13.0.
- Your OpenShift Container Platform cluster is installed on AWS, Azure, Google Cloud, bare metal or IBM P/Z platforms.
For more information on selecting a supported platform for your cluster installation, see _Selecting a cluster installation type_.

.Procedure
1. Verify that the `RetrievedUpdates` condition is `True` in the Cluster Version Operator (CVO) by running the following command:
```bash
$ oc get clusterversion/version -o=jsonpath="{.status.conditions[?(.type=='RetrievedUpdates')].status}"
```
If the `RetrievedUpates` condition is `False`, you can find supplemental information regarding the failure by using the following command:
```bash
$ oc adm upgrade
```
For more information about cluster version condition types, see _Understanding cluster version condition types_.

1. If the condition `RetrievedUpdates` is `False`, change the channel to `stable-<4.y>` or `fast-<4.y>` with the following command:
```bash
$ oc adm upgrade channel <channel>
```
After setting the channel, verify if `RetrievedUpdates` is `True`.
For more information about channels, see _Understanding update channels and releases_.

1. Migrate to the multi-architecture payload with following command:
```bash
$ oc adm upgrade --to-multi-arch
```

.Verification

- You can monitor the migration by running the following command:
```bash
$ oc adm upgrade
```
.Example output

```bash
working towards ${VERSION}: 106 of 841 done (12% complete), waiting on machine-config
```
> **IMPORTANT:** Machine launches may fail as the cluster settles into the new state. To notice and recover when machines fail to launch, we recommend deploying machine health checks. For more information about machine health checks and how to deploy them, see _About machine health checks_.
1. Optional: To retrieve more detailed information about the status of your update, monitor the migration by running the following command:
```bash
$ oc adm upgrade status
```
For more information about how to use the `oc adm upgrade status` command, see _Gathering cluster update status using oc adm upgrade status (Technology Preview)_.

The migrations must be complete and all the cluster operators must be stable before you can add compute machine sets with different architectures to your cluster.