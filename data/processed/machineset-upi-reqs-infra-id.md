# Obtaining the infrastructure ID

To ensure the Machine API correctly identifies and manages virtual machines (VMs) that belong to a specific cluster, you must add the unique infrastructure ID to the `MachineSet` YAML file to label and link resources. To create compute machine sets, you must be able to supply the infrastructure ID for your cluster.

.Procedure

- To obtain the infrastructure ID for your cluster, run the following command:
```bash
$ oc get infrastructure cluster -o jsonpath='{.status.infrastructureName}'
```