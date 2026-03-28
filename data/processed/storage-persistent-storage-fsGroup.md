# Reduce pod timeouts by using fsGroup

To reduce pod timeouts when using a storage volume with many files, configure the `fsGroup` field. By specifying this field, you can manage how file ownership and permissions are applied, preventing delays caused by the default recursive permission changes on large volumes.

This can occur because, by default, OpenShift Container Platform recursively changes ownership and permissions for the contents of each volume to match the `fsGroup` specified in the `securityContext` of the pod when that volume is mounted. For volumes with many files, checking and changing ownership and permissions can be time consuming, slowing pod startup. You can use the `fsGroupChangePolicy` field inside a `securityContext` to control the way that OpenShift Container Platform checks and manages ownership and permissions for a volume.

`fsGroupChangePolicy` defines behavior for changing ownership and permission of the volume before being exposed inside a pod. This field only applies to volume types that support `fsGroup`-controlled ownership and permissions. This field has two possible values:

- `OnRootMismatch`: Only change permissions and ownership if permission and ownership of root directory does not match with expected permissions of the volume. This can help shorten the time it takes to change ownership and permission of a volume to reduce pod timeouts.

- `Always`: (Default) Always change permission and ownership of the volume when a volume is mounted.

> **NOTE:** The `fsGroupChangePolicy` field has no effect on ephemeral volume types, such as secret, configMap, and emptydir.

You can set `fsGroupChangePolicy` at either the namespace or pod level.