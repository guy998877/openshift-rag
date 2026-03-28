# Recreate strategy

The recreate strategy has basic rollout behavior and supports lifecycle hooks for injecting code into the deployment process.

.Example recreate strategy definition
```yaml
kind: Deployment
apiVersion: apps/v1
metadata:
  name: hello-openshift
# ...
spec:
# ...
  strategy:
    type: Recreate
    recreateParams: <1>
      pre: {} <2>
      mid: {}
      post: {}
```

<1> `recreateParams` are optional.
<2> `pre`, `mid`, and `post` are lifecycle hooks.

The recreate strategy:

1. Executes any `pre` lifecycle hook.
1. Scales down the previous deployment to zero.
1. Executes any `mid` lifecycle hook.
1. Scales up the new deployment.
1. Executes any `post` lifecycle hook.

> **IMPORTANT:** During scale up, if the replica count of the deployment is greater than one, the first replica of the deployment will be validated for readiness before fully scaling up the deployment. If the validation of the first replica fails, the deployment will be considered a failure.

*When to use a recreate deployment:*

- When you must run migrations or other data transformations before your new code starts.
- When you do not support having new and old versions of your application code running at the same time.
- When you want to use a RWO volume, which is not supported being shared between multiple replicas.

A recreate deployment incurs downtime because, for a brief period, no instances of your application are running. However, your old code and new code do not run at the same time.