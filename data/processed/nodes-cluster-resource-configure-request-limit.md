# Finding the memory request and limit from within a pod

You can configure your container to use the Downward API to dynamically discover its memory request and limit from within a pod. This allows your applications to better manage these resources without needing to use the API server.  

.Procedure

- Configure the pod to add the `MEMORY_REQUEST` and `MEMORY_LIMIT` stanzas:

.. Create a YAML file similar to the following:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test
spec:
  securityContext:
    runAsNonRoot: false
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: test
    image: fedora:latest
    command:
    - sleep
    - "3600"
    env:
    - name: MEMORY_REQUEST
      valueFrom:
        resourceFieldRef:
          containerName: test
          resource: requests.memory
    - name: MEMORY_LIMIT
      valueFrom:
        resourceFieldRef:
          containerName: test
          resource: limits.memory
    resources:
      requests:
        memory: 384Mi
      limits:
        memory: 512Mi
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop: [ALL]
```
where:
--
`spec.consinters.env.name.MEMORY_REQUEST`:: This stanza discovers the application memory request value.

`spec.consinters.env.name.MEMORY_LIMIT`:: This stanza discovers the application memory limit value.
--

.. Create the pod by running the following command:
```bash
$ oc create -f <file_name>.yaml
```

.Verification

1. Access the pod using a remote shell:
```bash
$ oc rsh test
```

1. Check that the requested values were applied:
```bash
$ env | grep MEMORY | sort
```
.Example output
```bash
MEMORY_LIMIT=536870912
MEMORY_REQUEST=402653184
```

> **NOTE:** The memory limit value can also be read from inside the container by the `/sys/fs/cgroup/memory/memory.limit_in_bytes` file.