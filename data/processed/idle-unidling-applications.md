# Unidling applications

Application services become active again when they receive network traffic and
are scaled back up their previous state. This includes both traffic to the
services and traffic passing through routes.

Applications can also be manually unidled by scaling up the resources.

.Procedure

1. To scale up a DeploymentConfig, run:
```bash
$ oc scale --replicas=1 dc <dc_name>
```

> **NOTE:** Automatic unidling by a router is currently only supported by the default HAProxy router.