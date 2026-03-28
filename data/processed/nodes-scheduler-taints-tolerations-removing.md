# Removing taints and tolerations

You can remove taints from nodes and tolerations from pods as needed. You should add the toleration to the pod first, then add the taint to the node to avoid pods being removed from the node before you can add the toleration.

.Procedure

To remove taints and tolerations:

1. To remove a taint from a node:
```bash
$ oc adm taint nodes <node-name> <key>-
```
For example:
```bash
$ oc adm taint nodes ip-10-0-132-248.ec2.internal key1-
```
.Example output
```bash
node/ip-10-0-132-248.ec2.internal untainted
```

1. To remove a toleration from a pod, edit the `Pod` spec to remove the toleration:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
#...
spec:
  tolerations:
  - key: "key2"
    operator: "Exists"
    effect: "NoExecute"
    tolerationSeconds: 3600
#...
```