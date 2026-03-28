# About incremental back up support

OADP supports incremental backups of `block` and `Filesystem` persistent volumes for both containerized, and OpenShift Virtualization workloads. The following table summarizes the support for File System Backup (FSB), Container Storage Interface (CSI), and CSI Data Mover:

[cols="5", options="header"]
.OADP backup support matrix for containerized workloads
|===
| Volume mode |FSB - Restic  |FSB - Kopia | CSI | CSI Data Mover
| Filesystem | S ^[1]^, I ^[2]^ | S ^[1]^, I ^[2]^ | S ^[1]^ | S ^[1]^, I ^[2]^
| Block | N ^[3]^ | N ^[3]^ | S ^[1]^ | S ^[1]^, I ^[2]^
|===

[cols="5", options="header"]
.OADP backup support matrix for OpenShift Virtualization workloads
|===
| Volume mode |FSB - Restic  |FSB - Kopia | CSI | CSI Data Mover
| Filesystem | N ^[3]^ | N ^[3]^ | S ^[1]^ | S ^[1]^, I ^[2]^
| Block | N ^[3]^ | N ^[3]^ | S ^[1]^ | S ^[1]^, I ^[2]^
|===
[.small]
--
1. Backup supported
1. Incremental backup supported
1. Not supported
--

> **NOTE:** The CSI Data Mover backups use Kopia regardless of `uploaderType`.

// end of module. Need to add this comment because the level offset attribute does not get unset at the end of this module due to the continuation plus symbol. Causing the level offset from this module to stack on to the next module. This causes build failures or deeply nested modules.