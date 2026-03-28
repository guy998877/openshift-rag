# Connecting to a bare-metal node in your cluster

You can connect to bare-metal cluster nodes for general maintenance tasks.

> **NOTE:** Configuring the cluster node from the host operating system is not recommended or supported.

To troubleshoot your nodes, you can do the following tasks:

- Retrieve logs from a node
- Use debugging
- Use SSH to connect to a node

> **IMPORTANT:** Use SSH only if you cannot connect to the node with the `oc debug` command.

.Procedure

1. Retrieve the logs from a node by running the following command:
```bash
$ oc adm node-logs <node_name> -u crio
```

1. Use debugging by running the following command:
```bash
$ oc debug node/<node_name>
```

1. Set `/host` as the root directory within the debug shell. The debug pod mounts the host’s root file system in `/host` within the pod. By changing the root directory to `/host`, you can run binaries contained in the host’s executable paths:
--
```bash
# chroot /host
```

.Output
```bash
You are now logged in as root on the node
```
--

1. Optional: Use SSH to connect to the node by running the following command:
```bash
$ ssh core@<node_name>
```