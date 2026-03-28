# GPU-enabled machine options

You can deploy GPU-enabled compute machines on Amazon Web Services (AWS).
The following sample configuration uses an [AWS G4dn instance type](https://aws.amazon.com/ec2/instance-types/#Accelerated_Computing), which includes an NVIDIA Tesla T4 Tensor Core GPU, as an example.

For more information about supported instance types, see the following pages in the NVIDIA documentation:

- link:https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/platform-support.html[NVIDIA GPU Operator Community support matrix]

- link:https://docs.nvidia.com/ai-enterprise/latest/product-support-matrix/index.html[NVIDIA AI Enterprise support matrix]

// Cluster API machine template spec
.Sample GPU-enabled machine template configuration
```yaml
apiVersion: infrastructure.cluster.x-k8s.io/v1beta2
kind: AWSMachineTemplate
# ...
spec:
  template:
    spec:
      instanceType: g4dn.xlarge <1>
# ...
```
<1> Specifies a G4dn instance type.

// Cluster API machine set spec
.Sample GPU-enabled machine set configuration
```yaml
apiVersion: cluster.x-k8s.io/v1beta1
kind: MachineSet
metadata:
  name: <cluster_name>-gpu-<region> <1>
  namespace: openshift-cluster-api
  labels:
    cluster.x-k8s.io/cluster-name: <cluster_name>
spec:
  clusterName: <cluster_name>
  replicas: 1
  selector:
    matchLabels:
      test: example
      cluster.x-k8s.io/cluster-name: <cluster_name>
      cluster.x-k8s.io/set-name: <cluster_name>-gpu-<region> <2>
  template:
    metadata:
      labels:
        test: example
        cluster.x-k8s.io/cluster-name: <cluster_name>
        cluster.x-k8s.io/set-name: <cluster_name>-gpu-<region> <3>
        node-role.kubernetes.io/<role>: ""
# ...
```
<1> Specifies a name that includes the `gpu` role. The name includes the cluster ID as a prefix and the region as a suffix.
<2> Specifies a selector label that matches the machine set name.
<3> Specifies a template label that matches the machine set name.