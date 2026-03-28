# Obtaining information about a failed cluster

If a cluster deployment fails, the cluster is put into an "error" state.

.Procedure

- Run the following command to get more information:
```bash
$ rosa describe cluster -c <my_cluster_name> --debug
```