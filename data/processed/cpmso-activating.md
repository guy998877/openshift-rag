# Activating the control plane machine set custom resource

To use the control plane machine set, you must ensure that a `ControlPlaneMachineSet` custom resource (CR) with the correct settings for your cluster exists. On a cluster with a generated CR, you must verify that the configuration in the CR is correct for your cluster and activate it.

> **NOTE:** For more information about the parameters in the CR, see "Control plane machine set configuration".

.Procedure

1. View the configuration of the CR by running the following command:
```bash
$ oc --namespace openshift-machine-api edit controlplanemachineset.machine.openshift.io cluster
```

1. Change the values of any fields that are incorrect for your cluster configuration.

1. When the configuration is correct, activate the CR by setting the `.spec.state` field to `Active` and saving your changes.
> **IMPORTANT:** To activate the CR, you must change the `.spec.state` field to `Active` in the same `oc edit` session that you use to update the CR configuration. If the CR is saved with the state left as `Inactive`, the control plane machine set generator resets the CR to its original settings.