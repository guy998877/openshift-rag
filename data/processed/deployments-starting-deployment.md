# Starting a deployment

You can start a rollout to begin the deployment process of your application.

.Procedure

1. To start a new deployment process from an existing `DeploymentConfig` object, run the following command:
```bash
$ oc rollout latest dc/<name>
```
> **NOTE:** If a deployment process is already in progress, the command displays a message and a new replication controller will not be deployed.