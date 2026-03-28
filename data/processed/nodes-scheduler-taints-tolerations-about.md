# Understanding taints and tolerations

A _taint_ allows a node to refuse a pod to be scheduled unless that pod has a matching _toleration_.

You apply taints to a node through the `Node` specification (`NodeSpec`) and apply tolerations to a pod through the `Pod` specification (`PodSpec`). When you apply a taint to a node, the scheduler cannot place a pod on that node unless the pod can tolerate the taint.

.Example taint in a node specification
```yaml
apiVersion: v1
kind: Node
metadata:
  name: my-node
#...
spec:
  taints:
  - effect: NoExecute
    key: key1
    value: value1
#...
```

.Example toleration in a `Pod` spec
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
#...
spec:
  tolerations:
  - key: "key1"
    operator: "Equal"
    value: "value1"
    effect: "NoExecute"
    tolerationSeconds: 3600
#...
```

Taints and tolerations consist of a key, value, and effect.

.Taint and toleration components
[cols="3a,8a",options="header"]
|===

|Parameter |Description

|`key`
|The `key` is any string, up to 253 characters. The key must begin with a letter or number, and may contain letters, numbers, hyphens, dots, and underscores.

|`value`
| The `value` is any string, up to 63 characters. The value must begin with a letter or number, and may contain letters, numbers, hyphens, dots, and underscores.

|`effect`

|The effect is one of the following:
[frame=none]
[cols="2a,3a"]
!====
!`NoSchedule` ^[1]^
!* New pods that do not match the taint are not scheduled onto that node.
- Existing pods on the node remain.
!`PreferNoSchedule`
!* New pods that do not match the taint might be scheduled onto that node, but the scheduler tries not to.
- Existing pods on the node remain.
!`NoExecute`
!* New pods that do not match the taint cannot be scheduled onto that node.
- Existing pods on the node that do not have a matching toleration  are removed.
!====

|`operator`
|[frame=none]
[cols="2,3"]
!====
!`Equal`
!The `key`/`value`/`effect` parameters must match. This is the default.
!`Exists`
!The `key`/`effect` parameters must match. You must leave a blank `value` parameter, which matches any.
!====

|===
[.small]
--
1. If you add a `NoSchedule` taint to a control plane node, the node must have the `node-role.kubernetes.io/master=:NoSchedule` taint, which is added by default.
For example:
```yaml
apiVersion: v1
kind: Node
metadata:
  annotations:
    machine.openshift.io/machine: openshift-machine-api/ci-ln-62s7gtb-f76d1-v8jxv-master-0
    machineconfiguration.openshift.io/currentConfig: rendered-master-cdc1ab7da414629332cc4c3926e6e59c
  name: my-node
#...
spec:
  taints:
  - effect: NoSchedule
    key: node-role.kubernetes.io/master
#...
```
--

A toleration matches a taint:

- If the `operator` parameter is set to `Equal`:
- the `key` parameters are the same;
- the `value` parameters are the same;
- the `effect` parameters are the same.

- If the `operator` parameter is set to `Exists`:
- the `key` parameters are the same;
- the `effect` parameters are the same.

The following taints are built into OpenShift Container Platform:

- `node.kubernetes.io/not-ready`: The node is not ready. This corresponds to the node condition `Ready=False`.
- `node.kubernetes.io/unreachable`: The node is unreachable from the node controller. This corresponds to the node condition `Ready=Unknown`.
- `node.kubernetes.io/memory-pressure`: The node has memory pressure issues. This corresponds to the node condition `MemoryPressure=True`.
- `node.kubernetes.io/disk-pressure`: The node has disk pressure issues. This corresponds to the node condition `DiskPressure=True`.
- `node.kubernetes.io/network-unavailable`: The node network is unavailable.
- `node.kubernetes.io/unschedulable`: The node is unschedulable.
- `node.cloudprovider.kubernetes.io/uninitialized`: When the node controller is started with an external cloud provider, this taint is set on a node to mark it as unusable. After a controller from the cloud-controller-manager initializes this node, the kubelet removes this taint.
- `node.kubernetes.io/pid-pressure`: The node has pid pressure. This corresponds to the node condition `PIDPressure=True`.
> **IMPORTANT:** OpenShift Container Platform does not set a default pid.available `evictionHard`.