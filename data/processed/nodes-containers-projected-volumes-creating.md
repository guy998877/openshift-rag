# Configuring a Projected Volume for a Pod

When creating projected volumes, consider the volume file path situations described in _Understanding projected volumes_.

The following example shows how to use a projected volume to mount an existing secret volume source. The steps can be used to create a user name and password secrets from local files. You then create a pod that runs one container, using a projected volume to mount the secrets into the same shared directory.

The user name and password values can be any valid string that is *base64* encoded.

The following example shows `admin` in base64:

```bash
$ echo -n "admin" | base64
```

.Example output
```bash
YWRtaW4=
```

The following example shows the password `1f2d1e2e67df` in base64:

```bash
$ echo -n "1f2d1e2e67df" | base64
```

.Example output
```bash
MWYyZDFlMmU2N2Rm
```

.Procedure

To use a projected volume to mount an existing secret volume source.

1. Create the secret:

.. Create a YAML file similar to the following, replacing the password and user information as appropriate:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  pass: MWYyZDFlMmU2N2Rm
  user: YWRtaW4=
```
.. Use the following command to create the secret:
```bash
$ oc create -f <secrets-filename>
```
For example:
```bash
$ oc create -f secret.yaml
```
.Example output
```bash
secret "mysecret" created
```

.. You can check that the secret was created using the following commands:
```bash
$ oc get secret <secret-name>
```
For example:
```bash
$ oc get secret mysecret
```
.Example output
```bash
NAME       TYPE      DATA      AGE
mysecret   Opaque    2         17h
```
```bash
$ oc get secret <secret-name> -o yaml
```
For example:
```bash
$ oc get secret mysecret -o yaml
```
```yaml
apiVersion: v1
data:
  pass: MWYyZDFlMmU2N2Rm
  user: YWRtaW4=
kind: Secret
metadata:
  creationTimestamp: 2017-05-30T20:21:38Z
  name: mysecret
  namespace: default
  resourceVersion: "2107"
  selfLink: /api/v1/namespaces/default/secrets/mysecret
  uid: 959e0424-4575-11e7-9f97-fa163e4bd54c
type: Opaque
```

1. Create a pod with a projected volume.

.. Create a YAML file similar to the following, including a `volumes` section:
```yaml
kind: Pod
metadata:
  name: test-projected-volume
spec:
  securityContext:
    runAsNonRoot: true
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: test-projected-volume
    image: busybox
    args:
    - sleep
    - "86400"
    volumeMounts:
    - name: all-in-one
      mountPath: "/projected-volume"
      readOnly: true
    securityContext:
      allowPrivilegeEscalation: false
      capabilities:
        drop: [ALL]
  volumes:
  - name: all-in-one
    projected:
      sources:
      - secret:
          name: mysecret <1>
```
<1> The name of the secret you created.

.. Create the pod from the configuration file:
```bash
$ oc create -f <your_yaml_file>.yaml
```
For example:
```bash
$ oc create -f secret-pod.yaml
```
.Example output
```bash
pod "test-projected-volume" created
```

1. Verify that the pod container is running, and then watch for changes to
the pod:
```bash
$ oc get pod <name>
```
For example:
```bash
$ oc get pod test-projected-volume
```
The output should appear similar to the following:
.Example output
```bash
NAME                    READY     STATUS    RESTARTS   AGE
test-projected-volume   1/1       Running   0          14s
```

1. In another terminal, use the `oc exec` command to open a shell to the running container:
```bash
$ oc exec -it <pod> <command>
```
For example:
```bash
$ oc exec -it test-projected-volume -- /bin/sh
```

1. In your shell, verify that the `projected-volumes` directory contains your projected sources:
```bash
/ # ls
```
.Example output
```bash
bin               home              root              tmp
dev               proc              run               usr
etc               projected-volume  sys               var
```