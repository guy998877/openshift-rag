# Configuring control plane nodes as schedulable

[role="_abstract"] 
You can configure control plane nodes to be schedulable, meaning that new pods are allowed for placement on the control plane nodes.

By default, control plane nodes are not schedulable. You can set the control plane nodes to be schedulable, but you must retain the compute nodes.

> **NOTE:** You can deploy OpenShift Container Platform with no compute nodes on a bare-metal cluster. In this case, the control plane nodes are marked schedulable by default.

You can allow or disallow control plane nodes to be schedulable by configuring the `mastersSchedulable` field.

> **IMPORTANT:** When you configure control plane nodes from the default unschedulable to schedulable, additional subscriptions are required. This is because control plane nodes then become compute nodes.

.Procedure

1. Edit the `schedulers.config.openshift.io` resource.
```bash
$ oc edit schedulers.config.openshift.io cluster
```

1. Configure the `mastersSchedulable` field.
```yaml
apiVersion: config.openshift.io/v1
kind: Scheduler
metadata:
  creationTimestamp: "2019-09-10T03:04:05Z"
  generation: 1
  name: cluster
  resourceVersion: "433"
  selfLink: /apis/config.openshift.io/v1/schedulers/cluster
  uid: a636d30a-d377-11e9-88d4-0a60097bee62
spec:
  mastersSchedulable: false
status: {}
#...
```
where:
`spec.mastersSchedulable`:: Specifies whether the control plane nodes are schedulable. Set to `true` to allow control plane nodes to be schedulable, or `false` to disallow control plane nodes from being schedulable.

1. Save the file to apply the changes.