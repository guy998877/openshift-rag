# SELinux

Red Hat Enterprise Linux (RHEL) and Red Hat Enterprise Linux CoreOS (RHCOS) systems are configured to use SELinux on remote NFS servers by default.

For non-RHEL and non-RHCOS systems, SELinux does not allow writing from a pod to a remote NFS server. The NFS volume mounts correctly but it is read-only. You will need to enable the correct SELinux permissions by using the following procedure.

.Prerequisites

- The `container-selinux` package must be installed. This package provides the `virt_use_nfs` SELinux boolean.

.Procedure

- Enable the `virt_use_nfs` boolean using the following command. The `-P` option makes this boolean persistent across reboots.
```bash
# setsebool -P virt_use_nfs 1
```