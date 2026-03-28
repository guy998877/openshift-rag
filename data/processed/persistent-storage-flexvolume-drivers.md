# About FlexVolume drivers

A FlexVolume driver is an executable file that resides in a well-defined directory on all nodes in the cluster. OpenShift Container Platform calls the FlexVolume driver whenever it needs to mount or unmount a volume represented by a `PersistentVolume` object with `flexVolume` as the source.

> **IMPORTANT:** Attach and detach operations are not supported in OpenShift Container Platform for FlexVolume.