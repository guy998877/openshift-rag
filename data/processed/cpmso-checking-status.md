# Checking the control plane machine set custom resource state

You can verify the existence and state of the `ControlPlaneMachineSet` custom resource (CR).

.Procedure

- Determine the state of the CR by running the following command:
```bash
$ oc get controlplanemachineset.machine.openshift.io cluster \
  --namespace openshift-machine-api
```

- A result of `Active` indicates that the `ControlPlaneMachineSet` CR exists and is activated. No administrator action is required.

- A result of `Inactive` indicates that a `ControlPlaneMachineSet` CR exists but is not activated.

- A result of `NotFound` indicates that there is no existing `ControlPlaneMachineSet` CR.