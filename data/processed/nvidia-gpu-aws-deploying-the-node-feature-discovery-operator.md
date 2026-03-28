# Deploying the Node Feature Discovery Operator

After the GPU-enabled node is created, you need to discover the GPU-enabled node so it can be scheduled. To do this, install the Node Feature Discovery (NFD) Operator.

The NFD Operator identifies hardware device features in nodes. It solves the general problem of identifying and cataloging hardware resources in the infrastructure nodes so they can be made available to OpenShift Container Platform.

.Procedure

1. Install the Node Feature Discovery Operator from the software catalog in the OpenShift Container Platform console.

1. After installing the NFD Operator, select *Node Feature Discovery* from the installed Operators list and select *Create instance*. This installs the `nfd-master` and `nfd-worker` pods, one `nfd-worker` pod for each compute node, in the `openshift-nfd` namespace.

1. Verify that the Operator is installed and running by running the following command:
```bash
$ oc get pods -n openshift-nfd
```
.Example output
```bash
NAME                                       READY    STATUS     RESTARTS   AGE

nfd-controller-manager-8646fcbb65-x5qgk    2/2      Running 7  (8h ago)   1d
```

1. Browse to the installed Operator in the console and select *Create Node Feature Discovery*.

1. Select *Create* to build a NFD custom resource. This creates NFD pods in the `openshift-nfd` namespace that poll the OpenShift Container Platform nodes for hardware resources and catalog them.

.Verification

1. After a successful build, verify that a NFD pod is running on each nodes by running the following command:
```bash
$ oc get pods -n openshift-nfd
```
.Example output
```bash
NAME                                       READY   STATUS      RESTARTS        AGE
nfd-controller-manager-8646fcbb65-x5qgk    2/2     Running     7 (8h ago)      12d
nfd-master-769656c4cb-w9vrv                1/1     Running     0               12d
nfd-worker-qjxb2                           1/1     Running     3 (3d14h ago)   12d
nfd-worker-xtz9b                           1/1     Running     5 (3d14h ago)   12d
```
The NFD Operator uses vendor PCI IDs to identify hardware in a node. NVIDIA uses the PCI ID `10de`.

1. View the NVIDIA GPU discovered by the NFD Operator by running the following command:
```bash
$ oc describe node ip-10-0-132-138.us-east-2.compute.internal | egrep 'Roles|pci'
```
.Example output
```bash
Roles: worker

feature.node.kubernetes.io/pci-1013.present=true

feature.node.kubernetes.io/pci-10de.present=true

feature.node.kubernetes.io/pci-1d0f.present=true
```
`10de` appears in the node feature list for the GPU-enabled node. This mean the NFD Operator correctly identified the node from the GPU-enabled MachineSet.