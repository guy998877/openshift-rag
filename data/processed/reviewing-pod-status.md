# Reviewing pod status

You can query pod status and error states. You can also query a pod's associated deployment configuration and review base image availability.

.Prerequisites

- You have access to the cluster as a user with the `cluster-admin` role.
- You have installed the OpenShift CLI (`oc`).
- `skopeo` is installed.

.Procedure

1. Switch into a project:
```bash
$ oc project <project_name>
```

1. List pods running within the namespace, as well as pod status, error states, restarts, and age:
```bash
$ oc get pods
```

1. Determine whether the namespace is managed by a deployment configuration:
```bash
$ oc status
```
If the namespace is managed by a deployment configuration, the output includes the deployment configuration name and a base image reference.

1. Inspect the base image referenced in the preceding command's output:
```bash
$ skopeo inspect docker://<image_reference>
```

1. If the base image reference is not correct, update the reference in the deployment configuration:
```bash
$ oc edit deployment/my-deployment
```

1. When deployment configuration changes on exit, the configuration will automatically redeploy. Watch pod status as the deployment progresses, to determine whether the issue has been resolved:
```bash
$ oc get pods -w
```

1. Review events within the namespace for diagnostic information relating to pod failures:
```bash
$ oc get events
```