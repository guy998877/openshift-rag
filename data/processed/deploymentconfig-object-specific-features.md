# DeploymentConfig object-specific features

## Automatic rollbacks

Currently, deployments do not support automatically rolling back to the last successfully deployed replica set in case of a failure.

## Triggers

Deployments have an implicit config change trigger in that every change in the pod template of a deployment automatically triggers a new rollout.
If you do not want new rollouts on pod template changes, pause the deployment:

```bash
$ oc rollout pause deployments/<name>
```

## Lifecycle hooks

Deployments do not yet support any lifecycle hooks.

## Custom strategies

Deployments do not support user-specified custom deployment strategies.