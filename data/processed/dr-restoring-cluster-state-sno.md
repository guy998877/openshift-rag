# Restoring to a previous cluster state for a single node

You can use a saved etcd backup to restore a previous cluster state on a single node.

> **IMPORTANT:** When you restore your cluster, you must use an etcd backup that was taken from the same z-stream release. For example, an OpenShift Container Platform 4.21.2 cluster must use an etcd backup that was taken from 4.21.2.

.Prerequisites

- Access to the cluster as a user with the `cluster-admin` role through a certificate-based `kubeconfig` file, like the one that was used during installation.
- You have SSH access to control plane hosts.
- A backup directory containing both the etcd snapshot and the resources for the static pods, which were from the same backup. The file names in the directory must be in the following formats: `snapshot_<datetimestamp>.db` and `static_kuberesources_<datetimestamp>.tar.gz`.

.Procedure

1. Use SSH to connect to the single node and copy the etcd backup to the `/home/core` directory by running the following command:
```bash
$ cp <etcd_backup_directory> /home/core
```

1. Run the following command in the single node to restore the cluster from a previous backup:
```bash
$ sudo -E /usr/local/bin/cluster-restore.sh /home/core/<etcd_backup_directory>
```

1. Exit the SSH session.

1. Monitor the recovery progress of the control plane by running the following command:
```bash
$ oc adm wait-for-stable-cluster
```
> **NOTE:** It can take up to 15 minutes for the control plane to recover.