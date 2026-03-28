# Enabling Accelerated Networking on an existing Microsoft Azure cluster

You can enable Accelerated Networking on Azure by adding `acceleratedNetworking` to your machine set YAML file.

.Prerequisites

- Have an existing Microsoft Azure cluster where the Machine API is operational.

.Procedure
////
//Trying to move towards a more streamlined approach, but leaving this in in case needed
1. List the compute machine sets in your cluster by running the following command:
```bash
$ oc get machinesets -n openshift-machine-api
```
The compute machine sets are listed in the form of `<cluster-id>-worker-<region>`.
.Example output
```bash
NAME                                DESIRED   CURRENT   READY   AVAILABLE   AGE
jmywbfb-8zqpx-worker-centralus1     1         1         1       1           15m
jmywbfb-8zqpx-worker-centralus2     1         1         1       1           15m
jmywbfb-8zqpx-worker-centralus3     1         1         1       1           15m
```

1. For each compute machine set:

.. Edit the custom resource (CR) by running the following command:
```bash
$ oc edit machineset <machine-set-name>
```

.. Add the following to the `providerSpec` field:
////
- Add the following to the `providerSpec` field:
```yaml
providerSpec:
  value:
    acceleratedNetworking: true <1>
    vmSize: <azure-vm-size> <2>
```
<1> This line enables Accelerated Networking.
<2> Specify an Azure VM size that includes at least four vCPUs. For information about VM sizes, see [Microsoft Azure documentation](https://docs.microsoft.com/en-us/azure/virtual-machines/sizes).

.Verification

- On the Microsoft Azure portal, review the *Networking* settings page for a machine provisioned by the machine set, and verify that the `Accelerated networking` field is set to `Enabled`.