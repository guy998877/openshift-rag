# Scaling manually

In addition to rollbacks, you can exercise fine-grained control over the number of replicas by manually scaling them.

> **NOTE:** Pods can also be auto-scaled using the `oc autoscale` command.

.Procedure

1. To manually scale a `DeploymentConfig` object, use the `oc scale` command. For example, the following command sets the replicas in the `frontend` `DeploymentConfig` object to `3`.
```bash
$ oc scale dc frontend --replicas=3
```
The number of replicas eventually propagates to the desired and current state of the deployment configured by the `DeploymentConfig` object `frontend`.