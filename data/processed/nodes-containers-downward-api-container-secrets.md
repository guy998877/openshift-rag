# Consuming secrets using the Downward API

When creating pods, you can use the downward API to inject secrets
so image and application authors can create an image
for specific environments.

.Procedure

1. Create a secret to inject:

.. Create a `secret.yaml` file similar to the following:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
data:
  password: <password>
  username: <username>
type: kubernetes.io/basic-auth
```

.. Create the secret object from the `secret.yaml` file by using the following command:
```bash
$ oc create -f secret.yaml
```

1. Create a pod that references the `username` field from the above `Secret` object:

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
        - name: MY_SECRET_USERNAME
          valueFrom:
            secretKeyRef:
              name: mysecret
              key: username
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop: [ALL]
  restartPolicy: Never
# ...
```

.. Create the pod from the `pod.yaml` file by using the following command:
```bash
$ oc create -f pod.yaml
```

.Verification

- Check the container logs for the `MY_SECRET_USERNAME` value by using the following command:
```bash
$ oc logs -p dapi-env-test-pod
```