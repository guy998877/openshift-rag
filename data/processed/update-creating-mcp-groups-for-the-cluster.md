# Creating MachineConfigPool groups for the cluster

Creating `mcp` groups is a 2-step process:

1. Add an `mcp` label to the nodes in the cluster
1. Apply an `mcp` CR to the cluster that organizes the nodes based on their labels

.Procedure
1. Label the nodes so that they can be put into `mcp` groups.
Run the following commands:
```bash
$ oc label node worker-0 node-role.kubernetes.io/mcp-1=
```
```bash
$ oc label node worker-1 node-role.kubernetes.io/mcp-2=
```
The `mcp-1` and `mcp-2` labels are applied to the nodes.
For example:
.Example output
```bash
NAME           STATUS   ROLES                  AGE   VERSION
ctrl-plane-0   Ready    control-plane,master   39d   v1.27.15+6147456
ctrl-plane-1   Ready    control-plane,master   39d   v1.27.15+6147456
ctrl-plane-2   Ready    control-plane,master   39d   v1.27.15+6147456
worker-0       Ready    mcp-1,worker           39d   v1.27.15+6147456
worker-1       Ready    mcp-2,worker           39d   v1.27.15+6147456
```

1. Create YAML custom resources (CRs) that apply the labels as `mcp` CRs in the cluster.
Save the following YAML in the `mcps.yaml` file:
```yaml
---
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfigPool
metadata:
  name: mcp-2
spec:
  machineConfigSelector:
    matchExpressions:
      - {
         key: machineconfiguration.openshift.io/role,
         operator: In,
         values: [worker,mcp-2]
        }
  nodeSelector:
    matchLabels:
      node-role.kubernetes.io/mcp-2: ""
---
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfigPool
metadata:
  name: mcp-1
spec:
  machineConfigSelector:
    matchExpressions:
      - {
         key: machineconfiguration.openshift.io/role,
         operator: In,
         values: [worker,mcp-1]
        }
  nodeSelector:
    matchLabels:
      node-role.kubernetes.io/mcp-1: ""
```

1. Create the `MachineConfigPool` resources:
```bash
$ oc apply -f mcps.yaml
```
.Example output
```bash
machineconfigpool.machineconfiguration.openshift.io/mcp-2 created
```

.Verification

Monitor the `MachineConfigPool` resources as they are applied in the cluster.
After you apply the `mcp` resources, the nodes are added into the new machine config pools.
This takes a few minutes.

> **NOTE:** The nodes do not reboot while being added into the `mcp` groups. The original worker and master `mcp` groups remain unchanged.

- Check the status of the new `mcp` resources:
```bash
$ oc get mcp
```
.Example output
```bash
NAME     CONFIG                   UPDATED   UPDATING   DEGRADED   MACHINECOUNT   READYMACHINECOUNT UPDATEDMACHINECOUNT   DEGRADEDMACHINECOUNT   AGE
master   rendered-master-be3e83   True      False      False      3              3                 3                     0                      25d
mcp-1    rendered-mcp-1-2f4c4f    False     True       True       1              0                 0                     0                      10s
mcp-2    rendered-mcp-2-2r4s1f    False     True       True       1              0                 0                     0                      10s
worker   rendered-worker-23fc4f   False     True       True       0              0                 0                     2                      25d
```
Eventually, the resources are fully applied:
```bash
NAME     CONFIG                   UPDATED   UPDATING   DEGRADED   MACHINECOUNT   READYMACHINECOUNT UPDATEDMACHINECOUNT   DEGRADEDMACHINECOUNT   AGE
master   rendered-master-be3e83   True      False      False      3              3                 3                     0                      25d
mcp-1    rendered-mcp-1-2f4c4f    True      False      False      1              1                 1                     0                      7m33s
mcp-2    rendered-mcp-2-2r4s1f    True      False      False      1              1                 1                     0                      51s
worker   rendered-worker-23fc4f   True      False      False      0              0                 0                     0                      25d
```