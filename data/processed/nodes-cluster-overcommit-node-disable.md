# Disabling overcommitment for a node

When overcommitment is enabled on a node, you can disable overcommitment on that node. Disabling overcommit can help ensure predictability, stability, and high performance in your cluster.

.Procedure

- Run the following command on a node to disable overcommitment on that node:
```bash
$ sysctl -w vm.overcommit_memory=0
```