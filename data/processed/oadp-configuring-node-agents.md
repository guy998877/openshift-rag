# Configuring node agents and node labels

The Data Protection Application (DPA) uses the `nodeSelector` field to select which nodes can run the node agent. The `nodeSelector` field is the recommended form of node selection constraint.

.Procedure

1. Run the node agent on any node that you choose by adding a custom label:
```bash
$ oc label node/<node_name> node-role.kubernetes.io/nodeAgent=""
```
> **NOTE:** Any label specified must match the labels on each node.

1. Use the same custom label in the `DPA.spec.configuration.nodeAgent.podConfig.nodeSelector` field, which you used for labeling nodes:
```bash
configuration:
  nodeAgent:
    enable: true
    podConfig:
      nodeSelector:
        node-role.kubernetes.io/nodeAgent: ""
```
The following example is an anti-pattern of `nodeSelector` and does not work unless both labels, `node-role.kubernetes.io/infra: ""` and `node-role.kubernetes.io/worker: ""`, are on the node:
```bash
    configuration:
      nodeAgent:
        enable: true
        podConfig:
          nodeSelector:
            node-role.kubernetes.io/infra: ""
            node-role.kubernetes.io/worker: ""
```