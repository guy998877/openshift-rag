# Consuming container values using environment variables

When using environment variables in a container, you can specify that the variable's value should come from a `FieldRef` source instead of the literal value specified.

Only constant attributes of the pod can be consumed this way, because environment
variables cannot be updated after a process is started in a way that allows the
process to be notified that the value of a variable has changed. The following fields
are supported for using with environment variables:

- Pod name
- Pod project/namespace

.Procedure

1. Create a new pod spec that contains the environment variables you want the container to consume:

.. Create a `pod.yaml` file similar to the following:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: dapi-env-test-pod
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: env-test-container
      image: gcr.io/google_containers/busybox
      command: [ "/bin/sh", "-c", "env" ]
      env:
        - name: MY_POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: MY_POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop: [ALL]
  restartPolicy: Never
# ...
```
where:

`spec.containers.env.valueFrom.fieldRef.fieldPath`:: Specifies that the environment variable gets its value from the specified pod value, either `metadata.name` for the pod name or `metadata.namespace` for the pod namespace, instead of a literal value specified by a `value` field.

.. Create the pod from the `pod.yaml` file by using the following command:
```bash
$ oc create -f pod.yaml
```

.Verification

- Check the container logs for the `MY_POD_NAME` and `MY_POD_NAMESPACE`
values:
```bash
$ oc logs -p dapi-env-test-pod
```