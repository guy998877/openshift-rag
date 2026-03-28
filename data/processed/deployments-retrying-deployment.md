# Retrying a deployment

If the current revision of your `DeploymentConfig` object failed to deploy, you can restart the deployment process.

.Procedure

1. To restart a failed deployment process:
```bash
$ oc rollout retry dc/<name>
```
If the latest revision of it was deployed successfully, the command displays a message and the deployment process is not retried.
> **NOTE:** Retrying a deployment restarts the deployment process and does not create a new deployment revision. The restarted replication controller has the same configuration it had when it failed.