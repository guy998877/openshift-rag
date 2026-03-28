# Deleting a OpenShift Container Platform cluster upgrade with the ROSA CLI

You can use either the {rosa-cli-first} or OpenShift Cluster Manager console to delete a scheduled upgrade. This procedure uses the {rosa-cli}.

.Procedure

1. Verify the cluster update has not started using the following command:
```bash
$ rosa list upgrades --cluster=<cluster_name|cluster_id>
```
.Example output
```bash
VERSION  NOTES
4.15.14  recommended - scheduled for 2024-06-02 15:00 UTC
4.15.13
```

1. Delete a scheduled update by running the following command:
```bash
$ rosa delete upgrade --cluster=<cluster_name|cluster_id>
```
1. Confirm the deletion by entering `Yes` at the confirmation prompt.
.Example output
```bash
I: Successfully canceled scheduled upgrade on cluster 'my-cluster'
```

You will receive an email notification confirming that the scheduled upgrade has been canceled.