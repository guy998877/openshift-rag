# About Kopia repository maintenance

There are two types of Kopia repository maintenance:

Quick maintenance::
- Runs every hour to keep the number of index blobs (n) low. A high number of indexes negatively affects the performance of Kopia operations.
- Does not delete any metadata from the repository without ensuring that another copy of the same metadata exists.

Full maintenance::
- Runs every 24 hours to perform garbage collection of repository contents that are no longer needed.
- `snapshot-gc`, a full maintenance task, finds all files and directory listings that are no longer accessible from snapshot manifests and marks them as deleted.
- A full maintenance is a resource-costly operation, as it requires scanning all directories in all snapshots that are active in the cluster.

## Kopia maintenance in OADP

The `repo-maintain-job` jobs are executed in the namespace where OADP is installed, as shown in the following example:

```bash
pod/repo-maintain-job-173...2527-2nbls                             0/1     Completed   0          168m
pod/repo-maintain-job-173....536-fl9tm                             0/1     Completed   0          108m
pod/repo-maintain-job-173...2545-55ggx                             0/1     Completed   0          48m
```

You can check the logs of the `repo-maintain-job` for more details about the cleanup and the removal of artifacts in the backup object storage. You can find a note, as shown in the following example, in the `repo-maintain-job` when the next full cycle maintenance is due:

```bash
not due for full maintenance cycle until 2024-00-00 18:29:4
```

> **IMPORTANT:** Three successful executions of a full maintenance cycle are required for the objects to be deleted from the backup object storage. This means you can expect up to 72 hours for all the artifacts in the backup object storage to be deleted.