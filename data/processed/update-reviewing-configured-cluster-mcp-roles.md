# Reviewing configured cluster MachineConfigPool roles

Review the currently configured `MachineConfigPool` roles in the cluster.

.Procedure

1. Get the currently configured `mcp` groups in the cluster:
```bash
$ oc get mcp
```
.Example output
```bash
NAME     CONFIG                   UPDATED   UPDATING   DEGRADED   MACHINECOUNT   READYMACHINECOUNT   UPDATEDMACHINECOUNT   DEGRADEDMACHINECOUNT   AGE
master   rendered-master-bere83   True      False      False      3              3                   3                     0                      25d
worker   rendered-worker-245c4f   True      False      False      2              2                   2                     0                      25d
```

1. Compare the list of `mcp` roles to list of nodes in the cluster:
```bash
$ oc get nodes
```
.Example output
```bash
NAME           STATUS   ROLES                  AGE   VERSION
ctrl-plane-0   Ready    control-plane,master   39d   v1.27.15+6147456
ctrl-plane-1   Ready    control-plane,master   39d   v1.27.15+6147456
ctrl-plane-2   Ready    control-plane,master   39d   v1.27.15+6147456
worker-0       Ready    worker                 39d   v1.27.15+6147456
worker-1       Ready    worker                 39d   v1.27.15+6147456
```
> **NOTE:** When you apply an `mcp` group change, the node roles are updated.
Determine how you want to separate the worker nodes into `mcp` groups.