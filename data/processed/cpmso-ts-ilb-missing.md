# Adding a missing Azure internal load balancer

The `internalLoadBalancer` parameter is required in both the `ControlPlaneMachineSet` and control plane `Machine` custom resources (CRs) for Azure. If this parameter is not preconfigured on your cluster, you must add it to both CRs.

For more information about where this parameter is located in the Azure provider specification, see the sample Azure provider specification. The placement in the control plane `Machine` CR is similar.

.Procedure

1. List the control plane machines in your cluster by running the following command:
```bash
$ oc get machines \
  -l machine.openshift.io/cluster-api-machine-role==master \
  -n openshift-machine-api
```

1. For each control plane machine, edit the CR by running the following command:
```bash
$ oc edit machine <control_plane_machine_name>
```

1. Add the `internalLoadBalancer` parameter with the correct details for your cluster and save your changes.

1. Edit your control plane machine set CR by running the following command:
```bash
$ oc edit controlplanemachineset.machine.openshift.io cluster \
  -n openshift-machine-api
```

1. Add the `internalLoadBalancer` parameter with the correct details for your cluster and save your changes.

.Next steps

- For clusters that use the default `RollingUpdate` update strategy, the Operator automatically propagates the changes to your control plane configuration.

- For clusters that are configured to use the `OnDelete` update strategy, you must replace your control plane machines manually.