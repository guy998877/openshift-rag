# Understanding how to mark nodes as unschedulable or schedulable

You can mark a node as unschedulable in order to block any new pods from being scheduled on the node. 

When you mark a node as unschedulable, existing pods on the node are not affected.

By default, healthy nodes with a `Ready` status are
marked as schedulable, which means that you can place new pods on the
node.

- The following command marks a node or nodes as unschedulable:
.Example output
```bash
$ oc adm cordon <node>
```
For example:
```bash
$ oc adm cordon node1.example.com
```
.Example output
```bash
node/node1.example.com cordoned

NAME                 LABELS                                        STATUS
node1.example.com    kubernetes.io/hostname=node1.example.com      Ready,SchedulingDisabled
```

- The following command marks a currently unschedulable node or nodes as schedulable:
```bash
$ oc adm uncordon <node1>
```
Instead of specifying specific node names (for example, `<node>`), you can use the `--selector=<node_selector>` option to mark selected
nodes as schedulable or unschedulable.