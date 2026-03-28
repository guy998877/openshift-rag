[id=storage-ephemeral-storage-types_{context}]
# Types of ephemeral storage

To provision ephemeral local storage, you can create the primary partition by using either root or runtime methods. This storage is always made available in the primary partition, providing temporary space for your workloads.

## Root

This partition holds the kubelet root directory, `/var/lib/kubelet/` by default, and `/var/log/` directory. This partition can be shared between user pods, the OS, and Kubernetes system daemons. This partition can be consumed by pods through `EmptyDir` volumes, container logs, image layers, and container-writable layers. Kubelet manages shared access and isolation of this partition. This partition is ephemeral, and applications cannot expect any performance SLAs, such as disk IOPS, from this partition.

## Runtime

This is an optional partition that runtimes can use for overlay file systems. OpenShift Container Platform attempts to identify and provide shared access along with isolation to this partition. Container image layers and writable layers are stored here. If the runtime partition exists, the `root` partition does not hold any image layer or other writable storage.