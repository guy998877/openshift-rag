# Adjusting Ceph CPU and memory requirements based on collected data

The following recommendations are based on observations of performance made in the scale and performance lab. The changes are specifically related to Red Hat OpenShift Data Foundation (ODF). If working with ODF, consult the appropriate tuning guides for official recommendations.

## CPU and memory requirement for configurations

Backup and restore operations require large amounts of CephFS `PersistentVolumes` (PVs). To avoid Ceph MDS pods restarting with an `out-of-memory` (OOM) error, the following configuration is suggested:

|===
| Configuration types | Request | Max limit

| CPU
| Request changed to 3
| Max limit to 3

| Memory
| Request changed to 8 Gi
| Max limit to 128 Gi
|===