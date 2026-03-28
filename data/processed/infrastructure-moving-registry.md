# Moving the default registry

You configure the registry Operator to deploy its pods to different nodes.

.Prerequisites

- Configure additional compute machine sets in your OpenShift Container Platform cluster.

.Procedure

1. View the `config/instance` object:
```bash
$ oc get configs.imageregistry.operator.openshift.io/cluster -o yaml
```
.Example output
```yaml
apiVersion: imageregistry.operator.openshift.io/v1
kind: Config
metadata:
  creationTimestamp: 2019-02-05T13:52:05Z
  finalizers:
  - imageregistry.operator.openshift.io/finalizer
  generation: 1
  name: cluster
  resourceVersion: "56174"
  selfLink: /apis/imageregistry.operator.openshift.io/v1/configs/cluster
  uid: 36fd3724-294d-11e9-a524-12ffeee2931b
spec:
  httpSecret: d9a012ccd117b1e6616ceccb2c3bb66a5fed1b5e481623
  logging: 2
  managementState: Managed
  proxy: {}
  replicas: 1
  requests:
    read: {}
    write: {}
  storage:
    s3:
      bucket: image-registry-us-east-1-c92e88cad85b48ec8b312344dff03c82-392c
      region: us-east-1
status:
...
```

1. Edit the `config/instance` object:
```bash
$ oc edit configs.imageregistry.operator.openshift.io/cluster
```
```yaml
apiVersion: imageregistry.operator.openshift.io/v1
kind: Config
metadata:
  name: cluster
# ...
spec:
  logLevel: Normal
  managementState: Managed
  nodeSelector: <1>
    node-role.kubernetes.io/infra: ""
  tolerations:
  - effect: NoSchedule
    key: node-role.kubernetes.io/infra
    value: reserved
```
<1> Add a `nodeSelector` parameter with the appropriate value to the component you want to move. You can use a `nodeSelector` parameter in the format shown or use `<key>: <value>` pairs, based on the value specified for the node. If you added a taint to the infrasructure node, also add a matching toleration.

1. Verify the registry pod has been moved to the infrastructure node.
.. Run the following command to identify the node where the registry pod is located:
```bash
$ oc get pods -o wide -n openshift-image-registry
```
.. Confirm the node has the label you specified:
```bash
$ oc describe node <node_name>
```
Review the command output and confirm that `node-role.kubernetes.io/infra` is in the `LABELS` list.