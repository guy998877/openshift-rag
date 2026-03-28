# Copying files to and from pods and containers

You can copy files to and from a pod to test configuration changes or gather diagnostic information.

.Prerequisites

- You have access to the cluster as a user with the `cluster-admin` role.
- Your API service is still functional.
- You have installed the OpenShift CLI (`oc`).

.Procedure

1. Copy a file to a pod:
```bash
$ oc cp <local_path> <pod_name>:/<path> -c <container_name>
```
`-c <container_name>` refers to the desired container in a pod. If you do not specify a container with the `-c` option, then the first container in a pod is selected.

1. Copy a file from a pod:
```bash
$ oc cp <pod_name>:/<path> -c <container_name> <local_path>
```
`-c <container_name>` refers to the desired container in a pod. If you do not specify a container with the `-c` option, then the first container in a pod is selected.
> **NOTE:** For `oc cp` to function, the `tar` binary must be available within the container.