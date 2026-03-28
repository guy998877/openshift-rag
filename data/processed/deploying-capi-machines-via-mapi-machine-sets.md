# Deploying Cluster API compute machines by using a Machine API compute machine set

You can configure a Machine API compute machine set to deploy Cluster API compute machines.
With this process, you can test the Cluster API compute machine creation workflow without creating and scaling a Cluster API compute machine set.

A Machine API compute machine set with this configuration creates nonauthoritative Machine API compute machines that use the Cluster API as authoritative.
The two-way synchronization controller then creates corresponding authoritative Cluster API machines that provision on the underlying infrastructure.

:FeatureName: Deploying Cluster API compute machines by using a Machine API compute machine set

.Prerequisites

- You have deployed an OpenShift Container Platform cluster on a supported infrastructure type.

- You have enabled the use of the Cluster API.

- You have enabled the `MachineAPIMigration` feature gate in the `TechPreviewNoUpgrade` feature set.

- You have access to the cluster using an account with `cluster-admin` permissions.

- You have installed the pass:quotes[OpenShift CLI (`oc`)].

.Procedure

1. List the Machine API compute machine sets in your cluster by running the following command:
```bash
$ oc get machineset.machine.openshift.io -n openshift-machine-api
```

1. Edit the resource specification by running the following command:
```bash
$ oc edit machineset.machine.openshift.io <machine_set_name> \
  -n openshift-machine-api
```
where `<machine_set_name>` is the name of the Machine API compute machine set that you want to configure to deploy Cluster API compute machines.

1. In the resource specification, update the value of the `spec.template.spec.authoritativeAPI` field:
```yaml
apiVersion: machine.openshift.io/v1beta1
kind: MachineSet
metadata:
  [...]
  name: <machine_set_name>
  [...]
spec:
  authoritativeAPI: MachineAPI <1>
  [...]
  template:
    [...]
    spec:
      authoritativeAPI: ClusterAPI <2>
status:
  authoritativeAPI: MachineAPI <3>
  [...]
```
<1> The unconverted value for the Machine API compute machine set.
Do not change the value in this part of the specification.
<2> Specify `ClusterAPI` to configure the compute machine set to deploy Cluster API compute machines.
<3> The current value for the Machine API compute machine set.
Do not change the value in this part of the specification.

.Verification 

1. List the machines that are managed by the updated compute machine set by running the following command:
```bash
$ oc get machines.machine.openshift.io \
  -n openshift-machine-api \
  -l machine.openshift.io/cluster-api-machineset=<machine_set_name>
```

1. To verify that a machine created by the updated machine set has the correct configuration, examine the `status.authoritativeAPI` field in the CR for one of the new machines by running the following command:
```bash
$ oc describe machines.machine.openshift.io <machine_name> \
  -n openshift-machine-api
```
For a Cluster API compute machine, the value of the field is `ClusterAPI`.